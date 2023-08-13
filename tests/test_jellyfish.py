import csv
import platform
import pytest

open_kwargs = {"encoding": "utf8"}


def assertAlmostEqual(a, b, places=3):
    assert abs(a - b) < (0.1**places)


implementations = ["python", "rust"]


@pytest.fixture(params=implementations)
def jf(request):
    if request.param == "python":
        import jellyfish._jellyfish as jf
    elif request.param == "rust":
        from jellyfish import _rustyfish as jf
    return jf


def _load_data(name):
    with open("testdata/{}.csv".format(name), **open_kwargs) as f:
        yield from csv.reader(f)


@pytest.mark.parametrize("s1,s2,value", _load_data("jaro_winkler"), ids=str)
def test_jaro_winkler_similarity(jf, s1, s2, value):
    value = float(value)
    assertAlmostEqual(jf.jaro_winkler_similarity(s1, s2), value, places=3)


@pytest.mark.parametrize("s1,s2,value", _load_data("jaro_winkler_longtol"), ids=str)
def test_jaro_winkler_similarity_longtol(jf, s1, s2, value):
    value = float(value)
    assertAlmostEqual(jf.jaro_winkler_similarity(s1, s2, True), value, places=3)


@pytest.mark.parametrize("s1,s2,value", _load_data("jaro_distance"), ids=str)
def test_jaro_similarity(jf, s1, s2, value):
    value = float(value)
    assertAlmostEqual(jf.jaro_similarity(s1, s2), value, places=3)


@pytest.mark.parametrize("s1,s2,value", _load_data("hamming"), ids=str)
def test_hamming_distance(jf, s1, s2, value):
    value = int(value)
    assert jf.hamming_distance(s1, s2) == value


@pytest.mark.parametrize("s1,s2,value", _load_data("levenshtein"), ids=str)
def test_levenshtein_distance(jf, s1, s2, value):
    value = int(value)
    assert jf.levenshtein_distance(s1, s2) == value


@pytest.mark.parametrize("s1,s2,value", _load_data("damerau_levenshtein"), ids=str)
def test_damerau_levenshtein_distance(jf, s1, s2, value):
    value = int(value)
    assert jf.damerau_levenshtein_distance(s1, s2) == value


@pytest.mark.parametrize("s1,code", _load_data("soundex"), ids=str)
def test_soundex(jf, s1, code):
    assert jf.soundex(s1) == code


@pytest.mark.parametrize("s1,code", _load_data("metaphone"), ids=str)
def test_metaphone(jf, s1, code):
    assert jf.metaphone(s1) == code


@pytest.mark.parametrize("s1,s2", _load_data("nysiis"), ids=str)
def test_nysiis(jf, s1, s2):
    assert jf.nysiis(s1) == s2


@pytest.mark.parametrize("s1,s2", _load_data("match_rating_codex"), ids=str)
def test_match_rating_codex(jf, s1, s2):
    assert jf.match_rating_codex(s1) == s2


@pytest.mark.parametrize("s1,s2,value", _load_data("match_rating_comparison"), ids=str)
def test_match_rating_comparison(jf, s1, s2, value):
    value = {"True": True, "False": False, "None": None}[value]
    assert jf.match_rating_comparison(s1, s2) is value


def test_jaro_winkler_long_tolerance(jf):
    no_lt = jf.jaro_winkler_similarity(
        "two long strings", "two long stringz", long_tolerance=False
    )
    with_lt = jf.jaro_winkler_similarity(
        "two long strings", "two long stringz", long_tolerance=True
    )
    # make sure long_tolerance does something
    assertAlmostEqual(no_lt, 0.975)
    assertAlmostEqual(with_lt, 0.984)


def test_damerau_levenshtein_distance_type(jf):
    jf.damerau_levenshtein_distance("abc", "abc")
    with pytest.raises(TypeError) as exc:
        jf.damerau_levenshtein_distance(b"abc", b"abc")


def test_levenshtein_distance_type(jf):
    assert jf.levenshtein_distance("abc", "abc") == 0
    with pytest.raises(TypeError) as exc:
        jf.levenshtein_distance(b"abc", b"abc")


def test_jaro_similarity_type(jf):
    assert jf.jaro_similarity("abc", "abc") == 1
    with pytest.raises(TypeError) as exc:
        jf.jaro_similarity(b"abc", b"abc")


def test_jaro_winkler_type(jf):
    assert jf.jaro_winkler_similarity("abc", "abc") == 1
    with pytest.raises(TypeError) as exc:
        jf.jaro_winkler_similarity(b"abc", b"abc")


def test_mra_comparison_type(jf):
    assert jf.match_rating_comparison("abc", "abc") is True
    with pytest.raises(TypeError) as exc:
        jf.match_rating_comparison(b"abc", b"abc")


def test_hamming_type(jf):
    assert jf.hamming_distance("abc", "abc") == 0
    with pytest.raises(TypeError) as exc:
        jf.hamming_distance(b"abc", b"abc")


def test_soundex_type(jf):
    assert jf.soundex("ABC") == "A120"
    with pytest.raises(TypeError) as exc:
        jf.soundex(b"ABC")


def test_metaphone_type(jf):
    assert jf.metaphone("abc") == "ABK"
    with pytest.raises(TypeError) as exc:
        jf.metaphone(b"abc")


def test_nysiis_type(jf):
    assert jf.nysiis("abc") == "ABC"
    with pytest.raises(TypeError) as exc:
        jf.nysiis(b"abc")


def test_mr_codex_type(jf):
    assert jf.match_rating_codex("abc") == "ABC"
    with pytest.raises(TypeError) as exc:
        jf.match_rating_codex(b"abc")
