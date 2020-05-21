import warnings
try:
    from .cjellyfish import *   # noqa
    library = "C"
except ImportError:
    from ._jellyfish import *   # noqa
    library = "Python"


def jaro_winkler(s1, s2, long_tolerance=False):
    warnings.warn("the name 'jaro_winkler' is deprecated and will be removed in jellyfish 1.0, "
                  "please refer to this function as jaro_winkler_distance ", DeprecationWarning)
    return jaro_winkler_distance(s1, s2, long_tolerance)
