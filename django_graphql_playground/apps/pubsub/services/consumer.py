import json
import logging
import time
import uuid
from dataclasses import dataclass
from enum import Enum
from typing import Callable
from typing import Dict
from typing import Optional

import stomp
from stomp.connect import StompConnection11
from stomp.listener import TestListener

logger = logging.getLogger(__name__)


class Acknowledgements(Enum):
    """
    See more details at:
        - https://stomp.github.io/stomp-specification-1.2.html#SUBSCRIBE_ack_Header
        - https://jasonrbriggs.github.io/stomp.py/api.html#acks-and-nacks
    """

    CLIENT = "client"
    CLIENT_INDIVIDUAL = "client-individual"
    AUTO = "auto"


@dataclass(frozen=True)
class Payload:
    ack: Callable
    nack: Callable
    headers: Dict
    body: Dict


class _Listener(stomp.ConnectionListener):
    def __init__(
        self,
        connection: StompConnection11,
        callback: callable,
        subscription_configuration: Dict,
        connection_configuration: Dict,
    ) -> None:
        self._subscription_configuration = subscription_configuration
        self._connection_configuration = connection_configuration
        self._connection = connection
        self._callback = callback
        self._subscription_id = str(uuid.uuid4())
        self._listener_id = str(uuid.uuid4())
        self.test_listener: Optional[TestListener] = None

    def on_message(self, headers, message):
        message_id = headers["message-id"]
        logger.info(f"Message ID: {message_id}")
        logger.debug("Received headers: %s", headers)
        logger.debug("Received message: %s", message)

        # https://jasonrbriggs.github.io/stomp.py/api.html#acks-and-nacks
        def ack_logic():
            self._connection.ack(message_id, self._subscription_id)

        def nack_logic():
            self._connection.nack(message_id, self._subscription_id)

        self._callback(Payload(ack_logic, nack_logic, headers, json.loads(message)))

    def is_open(self):
        return self._connection.is_connected()

    def start(self, block=True, testing=False):
        logger.info(f"Starting listener with name: {self._listener_id}")
        logger.info(f"Subscribe/Listener auto-generated ID: {self._subscription_id}")

        if testing:
            self.test_listener = TestListener()
            self._connection.set_listener(self._listener_id, self.test_listener)
        else:
            self._connection.set_listener(self._listener_id, TestListener() if testing else self)

        self._connection.start()
        self._connection.connect(**self._connection_configuration)
        self._connection.subscribe(id=self._subscription_id, **self._subscription_configuration)

        if block:
            while True:
                # https://stackoverflow.com/a/529052/3899136
                time.sleep(1)

    def close(self):
        self._connection.disconnect()


def build_listener(destination_name, callback, ack_type=Acknowledgements.CLIENT, **connection_params) -> _Listener:
    logger.debug("Building listener for %s...", destination_name)
    hosts = [(connection_params.get("host"), connection_params.get("port"))]
    # http://stomp.github.io/stomp-specification-1.2.html#Heart-beating
    conn = stomp.Connection(hosts, heartbeats=(10000, 10000))
    client_id = connection_params.get("client_id", uuid.uuid4())
    subscription_configuration = {"destination": destination_name, "ack": ack_type.value}
    connection_configuration = {"wait": True, "headers": {"client-id": f"{client_id}-listener"}}
    listener = _Listener(conn, callback, subscription_configuration, connection_configuration)
    return listener
