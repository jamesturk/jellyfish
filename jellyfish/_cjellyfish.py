from . import cjellyfish
from .cjellyfish import porter_stem   # noqa
from .utils import phonetic_decorator, compare_decorator


@compare_decorator
def levenshtein_distance(*args, **kwargs):
    return cjellyfish.levenshtein_distance(*args, **kwargs)


@compare_decorator
def damerau_levenshtein_distance(*args, **kwargs):
    return cjellyfish.damerau_levenshtein_distance(*args, **kwargs)


@compare_decorator
def jaro_distance(*args, **kwargs):
    return cjellyfish.jaro_distance(*args, **kwargs)


@compare_decorator
def jaro_winkler(*args, **kwargs):
    return cjellyfish.jaro_winkler(*args, **kwargs)


@compare_decorator
def hamming_distance(*args, **kwargs):
    return cjellyfish.hamming_distance(*args, **kwargs)


@compare_decorator
def match_rating_comparison(*args, **kwargs):
    return cjellyfish.match_rating_comparison(*args, **kwargs)


@phonetic_decorator
def soundex(*args, **kwargs):
    return cjellyfish.soundex(*args, **kwargs)


@phonetic_decorator
def nysiis(*args, **kwargs):
    return cjellyfish.nysiis(*args, **kwargs)


@phonetic_decorator
def match_rating_codex(*args, **kwargs):
    return cjellyfish.match_rating_codex(*args, **kwargs)


@phonetic_decorator
def metaphone(*args, **kwargs):
    return cjellyfish.metaphone(*args, **kwargs)
