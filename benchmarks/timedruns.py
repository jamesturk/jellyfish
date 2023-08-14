import sys
import timeit
import csv

open_kwargs = {"encoding": "utf8"}


def _load_data(name):
    with open("./testdata/{}.csv".format(name), **open_kwargs) as f:
        yield from csv.reader(f)


def _load_n(name, n):
    data = []
    iterator = _load_data(name)
    while n > 0:
        try:
            data.append(next(iterator))
            n -= 1
        except StopIteration:
            iterator = _load_data(name)

    return data


def time_func(funcname, name, params, ftype):
    TEST_N = 100
    TEST_ITERATIONS = 10000
    if params == 1:
        run = "[{}(x) for x, y in data]".format(funcname)
    elif params == 2:
        run = "[{}(x, y) for x, y, z in data]".format(funcname)

    if ftype == "python":
        path = "_jellyfish"
    elif ftype == "c":
        path = "cjellyfish"
    elif ftype == "rust":
        path = "_rustyfish"

    return (
        timeit.timeit(
            run,
            setup="""from __main__ import _load_n
from jellyfish.{} import {}
data = _load_n('{}', {})
""".format(
                path, funcname, name, TEST_N
            ),
            number=TEST_ITERATIONS,
        )
        / (TEST_N * TEST_ITERATIONS)
    )


testing = [
    ("damerau_levenshtein_distance", "damerau_levenshtein", 2),
    ("hamming_distance", "hamming", 2),
    ("jaro_similarity", "jaro_distance", 2),
    ("jaro_winkler_similarity", "jaro_winkler", 2),
    ("levenshtein_distance", "levenshtein", 2),
    ("match_rating_codex", "match_rating_codex", 1),
    ("match_rating_comparison", "match_rating_comparison", 2),
    ("metaphone", "metaphone", 1),
    ("nysiis", "nysiis", 1),
    ("soundex", "soundex", 1),
]


def main():
    py_version = "{}.{}.{}".format(*sys.version_info[0:3])
    if sys.argv[1] == "old":
        jf_version = "0.10"
        ftypes = ("c", "python")
    elif sys.argv[1] == "new":
        jf_version = "dev"
        ftypes = ("rust",)

    for ftype in ftypes:
        for funcname, name, params in testing:
            result = time_func(funcname, name, params, ftype)
            print(f"{py_version},{jf_version},{ftype},{funcname},{result}")


if __name__ == "__main__":
    main()
