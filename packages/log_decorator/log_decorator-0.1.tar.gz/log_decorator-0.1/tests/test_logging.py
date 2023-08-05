from log_decorator import timed, add_handler
import time
from logging import Handler


class LogTestHandler(Handler):
    def __init__(self):
        super().__init__()
        self.messages = []

    def emit(self, record):
        self.messages.append(self.format(record))


@timed()
def slow_function(run):
    time.sleep(run * 0.01)


@timed()
def fast_function(run):
    time.sleep(run * 0.0001)


@timed(False)
def untimed():
    time.sleep(0.001)


def test_logging():
    handler = LogTestHandler()
    add_handler(handler)
    for i in range(5):
        slow_function(i)
        assert handler.messages[-2] == f"slow_function ran in 0.0{i}s"
        fast_function(i)

    slow_function(0)
    assert handler.messages[-1] == f"slow_function ran on average over 6 runs in 0.02s"


def test_untimed():
    handler = LogTestHandler()
    add_handler(handler)
    untimed()
    assert handler.messages == []