from __future__ import print_function

import sys
import timeit
if sys.version_info[0] < 3:
    import unicodecsv as csv
    open_kwargs = {}
else:
    import csv
    open_kwargs = {'encoding': 'utf8'}

def _load_data(name):
    with open('testdata/{}.csv'.format(name), **open_kwargs) as f:
        for data in csv.reader(f):
            yield data

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
        run = '[{}(x) for x, y in data]'.format(funcname)
    elif params == 2:
        run = '[{}(x, y) for x, y, z in data]'.format(funcname)

    return timeit.timeit(run,
                         setup='''from __main__ import _load_n
from jellyfish.{}jellyfish import {}
data = _load_n('{}', {})
'''.format('_' if ftype == 'python' else 'c', funcname, name, TEST_N), number=TEST_ITERATIONS) / (TEST_N * TEST_ITERATIONS)


testing = [
    ('damerau_levenshtein_distance', 'damerau_levenshtein', 2),
    ('hamming_distance', 'hamming', 2),
    ('jaro_distance', 'jaro_distance', 2),
    ('jaro_winkler', 'jaro_winkler', 2),
    ('levenshtein_distance', 'levenshtein', 2),
    ('match_rating_codex', 'match_rating_codex', 1),
    ('match_rating_comparison', 'match_rating_comparison', 2),
    ('metaphone', 'metaphone', 1),
    ('nysiis', 'nysiis', 1),
    ('porter_stem', 'porter', 1),
    ('soundex', 'soundex', 1),
]


version = '{}.{}.{}'.format(*sys.version_info[0:3])

for ftype in ('python', 'C'):
    for funcname, name, params in testing:
        result = time_func(funcname, name, params, ftype)
        print('{},{},{},{}'.format(version, ftype, funcname, result))
