import unittest
from mock import patch

import polling


class TestPoll(unittest.TestCase):

    def test_import(self):
        """Test that you can import via correct usage"""
        import polling
        from polling import poll

        assert poll
        assert polling

    def test_arg_validation(self):
        """Tests various permutations of calling with invalid args"""

        # No function
        try:
            polling.poll()
        except TypeError:
            pass
        else:
            assert False, 'No error raised with no args'

        try:
            polling.poll(lambda: True)
        except TypeError:
            pass
        else:
            assert False, 'No error raised with no step'

        try:
            polling.poll(lambda: True, step=1)
        except AssertionError:
            pass
        else:
            assert False, 'No error raised without specifying poll_forever or a timeout/max_tries'

        try:
            polling.poll(lambda: True, step=1, timeout=1, max_tries=1, poll_forever=True)
        except AssertionError:
            pass
        else:
            assert False, 'No error raised when specifying poll_forever with timeout/max_tries'

        # Valid options
        polling.poll(lambda: True, step=1, poll_forever=True)
        polling.poll(lambda: True, step=1, timeout=1)
        polling.poll(lambda: True, step=1, max_tries=1)
        polling.poll(lambda: True, step=1, timeout=1, max_tries=1)

    @patch('time.sleep', return_value=None)
    @patch('time.time', return_value=0)
    def test_timeout_exception(self, patch_sleep, patch_time):

        # Since the timeout is < 0, the first iteration of polling should raise the error if max timeout < 0
        try:
            polling.poll(lambda: False, step=10, timeout=-1)
        except polling.TimeoutException as e:
            assert e.values.qsize() == 1, 'There should have been 1 value pushed to the queue of values'
            assert e.last is False, 'The last value was incorrect'
        else:
            assert False, 'No timeout exception raised'

        # Test happy path timeout
        val = polling.poll(lambda: True, step=0, timeout=0)
        assert val is True, 'Val was: {} != {}'.format(val, True)

    def test_max_call_exception(self):
        """
        Test that a MaxCallException will be raised 
        """
        tries = 100
        try:
            polling.poll(lambda: False, step=0, max_tries=tries)
        except polling.MaxCallException as e:
            assert e.values.qsize() == tries, 'Poll function called the incorrect number of times'
            assert e.last is False, 'The last value was incorrect'
        else:
            assert False, 'No MaxCallException raised'
