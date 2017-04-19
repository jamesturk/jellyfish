import unicodedata
from functools import wraps

from .compat import IS_PY3


def _normalize(s):
    return unicodedata.normalize('NFKD', s)


def _check_type(s):
    if IS_PY3 and not isinstance(s, str):
        raise TypeError('expected str or unicode, got %s' % type(s).__name__)
    elif not IS_PY3 and not isinstance(s, unicode):
        raise TypeError('expected unicode, got %s' % type(s).__name__)


def compare_decorator(func):

    @wraps(func)
    def wrapper(s1, s2, *args, **kwargs):

        if isinstance(s1, (list)) and isinstance(s1, (list)):
            if len(s1) != len(s2):
                raise ValueError("length of list s1 has to be equal to the"
                                 "length of list s2")

            return [func(s1i, s2j, *args, **kwargs) for s1i, s2j in zip(s1, s2)]
        else:
            return func(s1, s2, *args, **kwargs)
    return wrapper


def phonetic_decorator(func):

    @wraps(func)
    def wrapper(s, *args, **kwargs):

        if isinstance(s, (list)):

            return [func(si, *args, **kwargs) for si in s]

        else:
            return func(s, *args, **kwargs)
    return wrapper


