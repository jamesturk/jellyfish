import warnings

from ._rustyfish import *
from . import _jellyfish


def jaro_winkler(s1, s2, long_tolerance=False):
    warnings.warn(
        "the name 'jaro_winkler' is deprecated and will be removed in jellyfish 1.0, "
        "for the same functionality please use jaro_winkler_similarity",
        DeprecationWarning,
    )
    return jaro_winkler_similarity(s1, s2, long_tolerance)  # noqa


def jaro_distance(s1, s2):
    warnings.warn(
        "the jaro_distance function incorrectly returns the jaro similarity, "
        "replace your usage with jaro_similarity before 1.0",
        DeprecationWarning,
    )
    return jaro_similarity(s1, s2)  # noqa
