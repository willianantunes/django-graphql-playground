import json
import logging
import ssl
import uuid
from contextlib import contextmanager
from typing import Callable
from typing import Dict

import stomp
import tenacity
from django.core.serializers.json import DjangoJSONEncoder
from stomp.connect import StompConnection11

from django_graphql_playground.support.decorators import slow_down

logger = logging.getLogger(__name__)


class _Publisher:
    def __init__(self, connection: StompConnection11, connection_configuration: Dict, destination_name: str) -> None:
        self._connection_configuration = connection_configuration
        self._connection = connection
        self._destination_name = destination_name
        # TODO: Make Content-Type dynamic
        self._default_content_type = "application/json;charset=utf-8"

    def is_open(self):
        return self._connection.is_connected()

    @slow_down
    def start(self):
        self._connection.start()
        self._connection.connect(**self._connection_configuration)
        logger.info("Connected")

    def close(self):
        self._connection.disconnect()
        logger.info("Disconnected")

    def send(self, body, headers=None, attempt=10):
        send_params = {
            "destination": self._destination_name,
            "body": json.dumps(body, cls=DjangoJSONEncoder),
            "headers": headers,
            "content_type": self._default_content_type,
            "transaction": getattr(self, "_tmp_transaction_id", None),
        }
        send_params = {k: v for k, v in send_params.items() if v is not None}

        def _internal_send_logic():
            if not self.is_open():
                logger.info("It is not open. Starting...")
                self.start()
            self._connection.send(**send_params)

        self._retry_send(_internal_send_logic, attempt=attempt)

    def _retry_send(self, function: Callable, attempt=10, *args, **kwargs):
        retry_configuration = tenacity.Retrying(
            stop=tenacity.stop_after_attempt(attempt),
            wait=tenacity.wait_fixed(3) + tenacity.wait_random(0, 2),
            after=tenacity.after_log(logger, logger.level) if logger else None,
            reraise=True,
        )
        return retry_configuration(function, *args, **kwargs)


def build_publisher(destination_name, **connection_params) -> _Publisher:
    logger.info("Building publisher...")
    hosts = [(connection_params.get("host"), connection_params.get("port"))]
    use_ssl = connection_params.get("use_ssl", False)
    ssl_version = connection_params.get("ssl_version", ssl.PROTOCOL_TLS)
    logger.info(f"Use SSL? {use_ssl}. Version: {ssl_version}")
    client_id = connection_params.get("client_id", uuid.uuid4())
    connection_configuration = {
        "username": connection_params.get("username"),
        "passcode": connection_params.get("password"),
        "wait": True,
        "headers": {"client-id": f"{client_id}-publisher"},
    }
    conn = stomp.Connection(hosts, ssl_version=ssl_version, use_ssl=use_ssl)
    publisher = _Publisher(conn, connection_configuration, destination_name)
    return publisher


@contextmanager
def auto_open_close_connection(publisher: _Publisher):
    try:
        publisher.start()
        yield
    finally:
        if publisher.is_open():
            publisher.close()


@contextmanager
def do_inside_transaction(publisher: _Publisher):
    with auto_open_close_connection(publisher):
        try:
            transaction_id = publisher._connection.begin()
            setattr(publisher, "_tmp_transaction_id", transaction_id)
            yield
            publisher._connection.commit(getattr(publisher, "_tmp_transaction_id"))
        finally:
            try:
                publisher._connection.abort(getattr(publisher, "_tmp_transaction_id"))
            finally:
                if hasattr(publisher, "_tmp_transaction_id"):
                    delattr(publisher, "_tmp_transaction_id")
