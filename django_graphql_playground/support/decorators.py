import functools
import logging
import time
from functools import wraps

logger = logging.getLogger(__name__)


def measure_it(func):
    @wraps(func)
    def timed(*args, **kw):
        start = time.perf_counter()
        try:
            return func(*args, **kw)
        finally:
            elapsed = time.perf_counter() - start
            logger.info(f"{func.__name__} from {func.__module__} with args {args} took {elapsed:0.2f} seconds")

    return timed


def auto_str(cls):
    def __str__(self):
        return f"{type(self).__name__}" f"({', '.join('%s=%s' % item for item in vars(self).items())})"

    cls.__str__ = __str__
    return cls


def slow_down(_func=None, *, before=1, after=1):
    """Sleep given amount of seconds before calling the function"""

    def decorator_slow_down(func):
        @functools.wraps(func)
        def wrapper_slow_down(*args, **kwargs):
            time.sleep(before)
            value = func(*args, **kwargs)
            time.sleep(after)
            return value

        return wrapper_slow_down

    if _func is None:
        return decorator_slow_down
    else:
        return decorator_slow_down(_func)
