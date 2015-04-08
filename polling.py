"""

"""
from Queue import Queue
import time
from datetime import timedelta


class PollingException(Exception):
    """TODO"""
    def __init__(self, values):
        self.values = values


class TimeoutException(PollingException):
    """Exception raised if polling function times out"""


class MaxCallException(PollingException):
    """Exception raised if maximum number of iterations is exceeded"""


def step_constant(step):
    return step


def step_linear_double(step):
    return step * 2


def is_truthy(val):
    return bool(val)


def poll(target, step, args=(), kwargs=None, timeout=None, max_tries=None, check_success=is_truthy,
         step_function=step_constant, ignore_exceptions=(), poll_forever=False, collect_values=None, *a, **k):
    """


    :param timeout: ...... NOTE that the actual execution time of the function *can* exceed the time specified in the
    timeout

    >>> def my_step_function(step):
    >>>     step += 10
    >>>     return max(step, 100)
    """

    assert (timeout or max_tries) or poll_forever, \
        ('You did not specify a maximum number of tries or a timeout. Without either of these set, the polling '
         'function will poll forever. If this is the behavior you want, pass "poll_forever=True"')

    kwargs = kwargs or dict()
    values = collect_values or Queue()

    max_time = time.time() + timeout if timeout else None
    tries = 0

    while True:

        try:
            val = target(*args, **kwargs)
            values.put(val)
        except ignore_exceptions, e:
            values.put(e)
        else:
            # Condition passes, this is the only "successful" exit from the polling function
            if check_success(val):
                return val

        # Check the "failure" exit conditions
        if max_time is not None and time.time() >= max_time:
            raise TimeoutException(values)
        elif max_tries is not None and tries >= max_tries:
            raise MaxCallException(values)

        tries += 1

        time.sleep(step)
        step = step_function(step)
