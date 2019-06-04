[![Build Status](https://travis-ci.org/ddmee/polling2.svg?branch=master)](https://travis-ci.org/ddmee/polling2)
[![PyPI](https://img.shields.io/pypi/dm/polling2.svg)]()
[![PyPI](https://img.shields.io/pypi/v/polling2.svg)]()

polling2
=============

Polling2 is a powerful python utility used to wait for a function to return a certain expected condition.
Some possible uses cases include:

- Wait for API response to return with code 200
- Wait for a file to exist (or not exist)
- Wait for a thread lock on a resource to expire

Polling2 is a fork of the original [polling](https://github.com/justiniso/polling). It was forked when the original maintainer failed to respond to issues or PRs. 

# Installation

```
pip install polling2
```

# Development installation

```
# installs lib and test dependencies, probably advisable to use a virtualenv
python setup.py install
# run the tests
pytest tests
```

# Examples

### Example: Poll every minute until a url returns 200 status code

```python
import requests
polling2.poll(
    lambda: requests.get('http://google.com').status_code == 200,
    step=60,
    poll_forever=True)
```

If you are creating a new cloud provider instance (e.g. waiting for an EC2 instance to come online), you can continue to poll despite getting ConnectionErrors:

```python
import requests
polling2.poll(
    lambda: requests.get('your.instance.ip').status_code == 200,
    step=60,
    ignore_exceptions=(requests.exceptions.ConnectionError,),
    poll_forever=True)
```

### Example: Poll for a file to exist

```python
# This call will wait until the file exists, checking every 0.1 seconds and stopping after 3 seconds have elapsed
file_handle = polling2.poll(
    lambda: open('/tmp/myfile.txt'),
    ignore_exceptions=(IOError,),
    timeout=3,
    step=0.1)

# Polling will return the value of your polling function, so you can now interact with it
file_handle.close()
```
    
### Example: Polling for Selenium WebDriver elements

```python
from selenium import webdriver
driver = webdriver.Firefox()

driver.get('http://google.com')
search_box = polling2.poll(
    lambda: driver.find_element_by_id('search'),
    step=0.5,
    timeout=7)

search_box.send_keys('python polling')
```

### Example: Using the polling timeout exception

```python
# An exception will be raised by the polling function on timeout (or the maximum number of calls is exceeded).
# This exception will have a 'values' attribute. This is a queue with all values that did not meet the condition.
# You can access them in the except block.

import random
try:
    polling2.poll(lambda: random.choice([0, (), False]), step=0.5, timeout=1)
except polling2.TimeoutException, te:
    while not te.values.empty():
        # Print all of the values that did not meet the exception
        print te.values.get()
```


### Example: Using a custom condition callback function

```python
import requests

def is_correct_response(response):
    """Check that the response returned 'success'"""
    return response == 'success'

polling2.poll(
    lambda: requests.put('http://mysite.com/api/user', data={'username': 'Jill'},
    check_success=is_correct_response,
    step=1,
    timeout=10)
```

# Release notes

## 0.4.0
- No longer testing on python 2.6
- Creation of polling2, forked from polling as previous maintainer seems to be ignoring issues and pull-requests.
- Remove ```*a, **k``` from poll signature. This allows Type errors to be raised if caller spells arguments into correctly, making bugs easier to find.

## 0.3.0

- Support Python 3.4+

## 0.2.0

- Allow users to access a "last" attribute on the exceptions. This should hold the last evaluated value, which is the more common use case than getting the first value. 
- Fix a bug that actually ran 1 more time than value specified by max_tries

## 0.1.0

- First version

# Contributors
- Justin Iso (original creator)
- Donal Mee