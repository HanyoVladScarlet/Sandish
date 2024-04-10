from typing import Callable

def extension_method(func: Callable):
    def wrapper(self, *args, **kargs):
        return func(self, *args, **kargs)
    return wrapper