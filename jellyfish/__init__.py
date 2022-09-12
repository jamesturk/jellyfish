import warnings

try:
    from .cjellyfish import (
        damerau_levenshtein_distance,
        hamming_distance,
        jaro_similarity,
        jaro_winkler_similarity,
        levenshtein_distance,
        match_rating_codex,
        match_rating_comparison,
        metaphone,
        nysiis,
        porter_stem,
        soundex,
    )

    library = "C"
except ImportError:
    from ._jellyfish import (
        damerau_levenshtein_distance,
        hamming_distance,
        jaro_similarity,
        jaro_winkler_similarity,
        levenshtein_distance,
        match_rating_codex,
        match_rating_comparison,
        metaphone,
        nysiis,
        porter_stem,
        soundex,
    )

    library = "Python"


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
