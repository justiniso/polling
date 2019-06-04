import unittest
from mock import patch

import polling2


class TestPoll(unittest.TestCase):

    def test_import(self):
        """Test that you can import via correct usage"""
        import polling2
        from polling2 import poll

        assert poll
        assert polling2

    def test_arg_validation(self):
        """Tests various permutations of calling with invalid args"""

        # No function
        try:
            polling2.poll()
        except TypeError:
            pass
        else:
            assert False, 'No error raised with no args'

        try:
            polling2.poll(lambda: True)
        except TypeError:
            pass
        else:
            assert False, 'No error raised with no step'

        try:
            polling2.poll(lambda: True, step=1)
        except AssertionError:
            pass
        else:
            assert False, 'No error raised without specifying poll_forever or a timeout/max_tries'

        try:
            polling2.poll(lambda: True, step=1, timeout=1, max_tries=1, poll_forever=True)
        except AssertionError:
            pass
        else:
            assert False, 'No error raised when specifying poll_forever with timeout/max_tries'

        # Valid options
        polling2.poll(lambda: True, step=1, poll_forever=True)
        polling2.poll(lambda: True, step=1, timeout=1)
        polling2.poll(lambda: True, step=1, max_tries=1)
        polling2.poll(lambda: True, step=1, timeout=1, max_tries=1)

    @patch('time.sleep', return_value=None)
    @patch('time.time', return_value=0)
    def test_timeout_exception(self, patch_sleep, patch_time):

        # Since the timeout is < 0, the first iteration of polling should raise the error if max timeout < 0
        try:
            polling2.poll(lambda: False, step=10, timeout=-1)
        except polling2.TimeoutException as e:
            assert e.values.qsize() == 1, 'There should have been 1 value pushed to the queue of values'
            assert e.last is False, 'The last value was incorrect'
        else:
            assert False, 'No timeout exception raised'

        # Test happy path timeout
        val = polling2.poll(lambda: True, step=0, timeout=0)
        assert val is True, 'Val was: {} != {}'.format(val, True)

    def test_max_call_exception(self):
        """
        Test that a MaxCallException will be raised 
        """
        tries = 100
        try:
            polling2.poll(lambda: False, step=0, max_tries=tries)
        except polling2.MaxCallException as e:
            assert e.values.qsize() == tries, 'Poll function called the incorrect number of times'
            assert e.last is False, 'The last value was incorrect'
        else:
            assert False, 'No MaxCallException raised'
