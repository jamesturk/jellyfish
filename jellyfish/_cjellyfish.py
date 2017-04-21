from . import cjellyfish
from .cjellyfish import porter_stem   # noqa
from .utils import phonetic_decorator, compare_decorator


@compare_decorator
def levenshtein_distance(*args, **kwargs):
    """Compute the Levenshtein distance."""
    return cjellyfish.levenshtein_distance(*args, **kwargs)


@compare_decorator
def damerau_levenshtein_distance(*args, **kwargs):
    """Compute the Damerau-Levenshtein distance."""
    return cjellyfish.damerau_levenshtein_distance(*args, **kwargs)


@compare_decorator
def jaro_distance(*args, **kwargs):
    """Compute the Jaro distance."""
    return cjellyfish.jaro_distance(*args, **kwargs)


@compare_decorator
def jaro_winkler(*args, **kwargs):
    """Compute the Jaro-Winkler distance."""
    return cjellyfish.jaro_winkler(*args, **kwargs)


@compare_decorator
def hamming_distance(*args, **kwargs):
    """Compute the Hamming distance."""
    return cjellyfish.hamming_distance(*args, **kwargs)


@compare_decorator
def match_rating_comparison(*args, **kwargs):
    """Compute the Match Rating Approach."""
    return cjellyfish.match_rating_comparison(*args, **kwargs)


@phonetic_decorator
def soundex(*args, **kwargs):
    """Compute the Soundex code."""
    return cjellyfish.soundex(*args, **kwargs)


@phonetic_decorator
def nysiis(*args, **kwargs):
    """Compute the NYSIIS code."""
    return cjellyfish.nysiis(*args, **kwargs)


@phonetic_decorator
def match_rating_codex(*args, **kwargs):
    """Compute the Match Rating Approach code."""
    return cjellyfish.match_rating_codex(*args, **kwargs)


@phonetic_decorator
def metaphone(*args, **kwargs):
    """"Compute the Metaphone code."""
    return cjellyfish.metaphone(*args, **kwargs)
