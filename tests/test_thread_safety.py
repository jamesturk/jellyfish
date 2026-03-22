import concurrent.futures
import jellyfish


ITERATIONS = 500
WORKERS = 8


def _run_parallel(fn, *args):
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = [pool.submit(fn, *args) for _ in range(ITERATIONS)]
        return [f.result() for f in futures]


def test_levenshtein_distance_threaded():
    results = _run_parallel(jellyfish.levenshtein_distance, "hello", "world")
    assert all(r == 4 for r in results)


def test_damerau_levenshtein_distance_threaded():
    results = _run_parallel(jellyfish.damerau_levenshtein_distance, "hello", "world")
    assert all(r == 4 for r in results)


def test_hamming_distance_threaded():
    results = _run_parallel(jellyfish.hamming_distance, "hello", "world")
    assert all(r == 4 for r in results)


def test_jaro_similarity_threaded():
    results = _run_parallel(jellyfish.jaro_similarity, "hello", "world")
    expected = results[0]
    assert all(r == expected for r in results)


def test_jaro_winkler_similarity_threaded():
    results = _run_parallel(jellyfish.jaro_winkler_similarity, "hello", "world")
    expected = results[0]
    assert all(r == expected for r in results)


def test_soundex_threaded():
    results = _run_parallel(jellyfish.soundex, "Robert")
    assert all(r == "R163" for r in results)


def test_metaphone_threaded():
    results = _run_parallel(jellyfish.metaphone, "Robert")
    expected = results[0]
    assert all(r == expected for r in results)


def test_nysiis_threaded():
    results = _run_parallel(jellyfish.nysiis, "Robert")
    expected = results[0]
    assert all(r == expected for r in results)


def test_match_rating_codex_threaded():
    results = _run_parallel(jellyfish.match_rating_codex, "Robert")
    expected = results[0]
    assert all(r == expected for r in results)


def test_match_rating_comparison_threaded():
    results = _run_parallel(jellyfish.match_rating_comparison, "Robert", "Rupert")
    assert all(r is True for r in results)


def test_jaccard_similarity_threaded():
    results = _run_parallel(jellyfish.jaccard_similarity, "hello", "world")
    expected = results[0]
    assert all(r == expected for r in results)
