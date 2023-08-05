import logging
import time

from functools import wraps

logger = logging.getLogger(__name__)


logger.setLevel("DEBUG")
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(levelname)s -- %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

avg_runtime = {}
count_runs = {}


def add_handler(handler):
    logger.addHandler(handler)


def timed(active=True):
    """This decorator prints the execution time for the decorated function."""

    def wrap(func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if active:
                f_name = func.__name__
                start = time.time()
                result = func(*args, **kwargs)
                runtime = time.time() - start
                logger.debug(f"{f_name} ran in {runtime:.2f}s")

                old_count = count_runs.get(f_name, 0)
                old_avg_runtime = avg_runtime.get(f_name, 0)
                avg_runtime[f_name] = (runtime + old_count * old_avg_runtime) / (
                    old_count + 1
                )
                count_runs[f_name] = old_count + 1
                logger.info(
                    f"{f_name} ran on average over {count_runs[f_name]} runs in {avg_runtime[f_name]:.2f}s"
                )
                return result
            else:
                return func(*args, **kwargs)

        return wrapped_func

    return wrap