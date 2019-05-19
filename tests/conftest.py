import pytest


@pytest.yield_fixture
def caplog(caplog):
    import logging

    restore = []
    for logger in logging.Logger.manager.loggerDict.values():
        try:
            if not logger.propagate:
                logger.propagate = True
                restore += [logger]
        except AttributeError:
            pass
    yield caplog
    for logger in restore:
        logger.propagate = False


def pytest_assertrepr_compare(config, op, left, right):
    """
    More details at: https://stackoverflow.com/a/50625086/3899136
    """
    if op in ("==", "!="):
        return ["{0} {1} {2}".format(left, op, right)]
