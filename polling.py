"""

"""
from Queue import Queue
import time


class PollingException(Exception):
    """TODO"""
    def __init__(self, values):
        self.values = values


class TimeoutException(PollingException):
    """Exception raised if polling function times out"""


class MaxCallException(PollingException):
    """Exception raised if maximum number of iterations is exceeded"""


def step_constant(step):
    """Use this function when you want the step to remain fixed in every iteration (typically good for
    instances when you know approximately how long the function should poll for)"""
    return step


def step_linear_double(step):
    """Use this function when you want the step to double each iteration (e.g. like the way ArrayList works in
    Java). Note that this can result in very long poll times after a few iterations"""
    return step * 2


def is_truthy(val):
    """Use this function to test if a return value is truthy"""
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

    assert (timeout is not None or max_tries is not None) or poll_forever, \
        ('You did not specify a maximum number of tries or a timeout. Without either of these set, the polling '
         'function will poll forever. If this is the behavior you want, pass "poll_forever=True"')

    assert not ((timeout is not None or max_tries is not None) and poll_forever), \
        'You cannot specify both the option to poll_forever and max_tries/timeout.'

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
