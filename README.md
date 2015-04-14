polling
=============

Polling is a powerful python utility used to wait for a function to return a certain expected condition.
Some possible uses cases include:

- Wait for API response to return with code 200
- Wait for a file to exist (or not exist)
- Wait for a thread lock on a resource to expire

### Example: Poll every minute until a url returns 200 status code

    import requests
    polling.poll(
        lambda: requests.get('http://google.com').status_code == 200,
        step=60,
        poll_forever=True
    )

### Example: Poll for a file to exist

    # This call will wait until the file exists, checking every 0.1 seconds and stopping after 3 seconds have elapsed
    polling.poll(
        lambda: open('/tmp/myfile.txt'),
        ignore_exceptions=(IOError,),
        timeout=3,
        step=0.1
    )

### Example: Using the polling timeout exception

    # An exception will be raised by the polling function on timeout (or the maximum number of calls is exceeded).
    # This exception will have a 'values' attribute. This is a queue with all values that did not meet the condition.
    # You can access them in the except block.

    import random
    try:
        polling.poll(lambda: random.choice([0, (), False]), step=0.5, timeout=1)
    except polling.TimeoutException, te:
        while not te.values.empty():
            # Print all of the values that did not meet the exception
            print te.values.get()


### Example: Using a custom condition callback function

    import requests

    def is_correct_response(response):
        """Check that the response returned 'success'"""
        return response == 'success'

    polling.poll(
        lambda: requests.put('http://mysite.com/api/user', data={'username': 'Jill'},
        check_success=is_correct_response,
        step=1,
        timeout=10
    )

