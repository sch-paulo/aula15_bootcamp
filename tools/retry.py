import time 
from functools import wraps

def retry(exception_to_check, tries=3, delay=1, backoff=2):
    '''
    Decorator that retries the function several times in case of exception
    
    :param exception_to_check: The exception (or tuple of exceptions) that should be caught
    :param tries: The number max of tries
    :param delay: The initial wait time between tries
    :param backoff: The factor by which the delay should increase after each attempt
    '''
    def decorator_retry(func):
        @wraps(func)
        def wrapper_retry(*args, **kwargs):
            _tries, _delay = tries, delay
            while _tries > 1:
                try:
                    return func(*args, **kwargs)
                except exception_to_check as e:
                    print(f'{func.__name__} failed, trying again in {_delay} seconds. Remaining tries: {_tries -1}')
                    time.sleep(_delay)
                    _tries -= 1
                    _delay *= backoff
                return func(*args, **kwargs)
            return wrapper_retry
        return decorator_retry