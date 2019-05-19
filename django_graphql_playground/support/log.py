import logging.config
import threading
from contextlib import contextmanager
from uuid import uuid4

local_threading = threading.local()


class ContextFilter(logging.Filter):
    """
    This is a filter which injects contextual information into the log.
    """

    def filter(self, record):
        record.correlation_id = getattr(local_threading, "correlation_id", None)
        return True


def _generated_correlation_id(custom_correlation_id=None) -> None:
    local_threading.correlation_id = str(uuid4()) if custom_correlation_id is None else custom_correlation_id


def _unset_correlation_id() -> None:
    del local_threading.correlation_id


@contextmanager
def do_log_with_correlation_id(custom_correlation_id=None):
    try:
        _generated_correlation_id(custom_correlation_id)
        yield
    finally:
        _unset_correlation_id()
