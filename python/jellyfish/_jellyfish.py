import unicodedata
from collections import defaultdict
from itertools import zip_longest
import warnings


def _normalize(s):
    return unicodedata.normalize("NFKD", s)


def _check_type(s):
    # warn here since each function will call this
    warnings.warn(
        "The jellyfish._jellyfish module is deprecated and will be removed in jellyfish 1.0.",
        DeprecationWarning,
    )
    if not isinstance(s, str):
        raise TypeError("expected str or unicode, got %s" % type(s).__name__)


def levenshtein_distance(s1, s2):
    _check_type(s1)
    _check_type(s2)

    if s1 == s2:
        return 0
    rows = len(s1) + 1
    cols = len(s2) + 1

    if not s1:
        return cols - 1
    if not s2:
        return rows - 1

    prev = None
    cur = range(cols)
    for r in range(1, rows):
        prev, cur = cur, [r] + [0] * (cols - 1)
        for c in range(1, cols):
            deletion = prev[c] + 1
            insertion = cur[c - 1] + 1
            edit = prev[c - 1] + (0 if s1[r - 1] == s2[c - 1] else 1)
            cur[c] = min(edit, deletion, insertion)

    return cur[-1]


def _jaro_winkler(s1, s2, long_tolerance, winklerize):
    _check_type(s1)
    _check_type(s2)

    s1_len = len(s1)
    s2_len = len(s2)

    if not s1_len or not s2_len:
        return 0.0

    min_len = min(s1_len, s2_len)
    search_range = max(s1_len, s2_len)
    search_range = (search_range // 2) - 1
    if search_range < 0:
        search_range = 0

    s1_flags = [False] * s1_len
    s2_flags = [False] * s2_len

    # looking only within search range, count & flag matched pairs
    common_chars = 0
    for i, s1_ch in enumerate(s1):
        low = max(0, i - search_range)
        hi = min(i + search_range, s2_len - 1)
        for j in range(low, hi + 1):
            if not s2_flags[j] and s2[j] == s1_ch:
                s1_flags[i] = s2_flags[j] = True
                common_chars += 1
                break

    # short circuit if no characters match
    if not common_chars:
        return 0.0

    # count transpositions
    k = trans_count = 0
    for i, s1_f in enumerate(s1_flags):
        if s1_f:
            for j in range(k, s2_len):
                if s2_flags[j]:
                    k = j + 1
                    break
            if s1[i] != s2[j]:
                trans_count += 1
    trans_count //= 2

    # adjust for similarities in nonmatched characters
    common_chars = float(common_chars)
    weight = (
        (
            common_chars / s1_len
            + common_chars / s2_len
            + (common_chars - trans_count) / common_chars
        )
    ) / 3

    # winkler modification: continue to boost if strings are similar
    if winklerize and weight > 0.7:
        # adjust for up to first 4 chars in common
        j = min(min_len, 4)
        i = 0
        while i < j and s1[i] == s2[i]:
            i += 1
        if i:
            weight += i * 0.1 * (1.0 - weight)

        # optionally adjust for long strings
        # after agreeing beginning chars, at least two or more must agree and
        # agreed characters must be > half of remaining characters
        if (
            long_tolerance
            and min_len > 4
            and common_chars > i + 1
            and 2 * common_chars >= min_len + i
        ):
            weight += (1.0 - weight) * (
                float(common_chars - i - 1) / float(s1_len + s2_len - i * 2 + 2)
            )

    return weight


def jaro_similarity(s1, s2):
    return _jaro_winkler(s1, s2, False, False)  # noqa


def jaro_winkler_similarity(s1, s2, long_tolerance=False):
    return _jaro_winkler(s1, s2, long_tolerance, True)  # noqa


def damerau_levenshtein_distance(s1, s2):
    _check_type(s1)
    _check_type(s2)

    len1 = len(s1)
    len2 = len(s2)
    infinite = len1 + len2

    # character array
    da = defaultdict(int)

    # distance matrix
    score = [[0] * (len2 + 2) for x in range(len1 + 2)]

    score[0][0] = infinite
    for i in range(0, len1 + 1):
        score[i + 1][0] = infinite
        score[i + 1][1] = i
    for i in range(0, len2 + 1):
        score[0][i + 1] = infinite
        score[1][i + 1] = i

    for i in range(1, len1 + 1):
        db = 0
        for j in range(1, len2 + 1):
            i1 = da[s2[j - 1]]
            j1 = db
            cost = 1
            if s1[i - 1] == s2[j - 1]:
                cost = 0
                db = j

            score[i + 1][j + 1] = min(
                score[i][j] + cost,
                score[i + 1][j] + 1,
                score[i][j + 1] + 1,
                score[i1][j1] + (i - i1 - 1) + 1 + (j - j1 - 1),
            )
        da[s1[i - 1]] = i

    return score[len1 + 1][len2 + 1]


def soundex(s):
    _check_type(s)

    if not s:
        return ""

    s = _normalize(s)
    s = s.upper()

    replacements = (
        ("BFPV", "1"),
        ("CGJKQSXZ", "2"),
        ("DT", "3"),
        ("L", "4"),
        ("MN", "5"),
        ("R", "6"),
    )
    result = [s[0]]
    count = 1

    # find would-be replacement for first character
    for lset, sub in replacements:
        if s[0] in lset:
            last = sub
            break
    else:
        last = None

    for letter in s[1:]:
        for lset, sub in replacements:
            if letter in lset:
                if sub != last:
                    result.append(sub)
                    count += 1
                last = sub
                break
        else:
            if letter != "H" and letter != "W":
                # leave last alone if middle letter is H or W
                last = None
        if count == 4:
            break

    result += "0" * (4 - count)
    return "".join(result)


def hamming_distance(s1, s2):
    _check_type(s1)
    _check_type(s2)

    # ensure length of s1 >= s2
    if len(s2) > len(s1):
        s1, s2 = s2, s1

    # distance is difference in length + differing chars
    distance = len(s1) - len(s2)
    for i, c in enumerate(s2):
        if c != s1[i]:
            distance += 1

    return distance


def nysiis(s):
    _check_type(s)

    if not s:
        return ""

    s = s.upper()
    key = []

    # step 1 - prefixes
    if s.startswith("MAC"):
        s = "MCC" + s[3:]
    elif s.startswith("KN"):
        s = s[1:]
    elif s.startswith("K"):
        s = "C" + s[1:]
    elif s.startswith(("PH", "PF")):
        s = "FF" + s[2:]
    elif s.startswith("SCH"):
        s = "SSS" + s[3:]

    # step 2 - suffixes
    if s.endswith(("IE", "EE")):
        s = s[:-2] + "Y"
    elif s.endswith(("DT", "RT", "RD", "NT", "ND")):
        s = s[:-2] + "D"

    # step 3 - first character of key comes from name
    key.append(s[0])

    # step 4 - translate remaining chars
    i = 1
    len_s = len(s)
    while i < len_s:
        ch = s[i]
        if ch == "E" and i + 1 < len_s and s[i + 1] == "V":
            ch = "AF"
            i += 1
        elif ch in "AEIOU":
            ch = "A"
        elif ch == "Q":
            ch = "G"
        elif ch == "Z":
            ch = "S"
        elif ch == "M":
            ch = "N"
        elif ch == "K":
            if i + 1 < len(s) and s[i + 1] == "N":
                ch = "N"
            else:
                ch = "C"
        elif ch == "S" and s[i + 1 : i + 3] == "CH":
            ch = "SS"
            i += 2
        elif ch == "P" and i + 1 < len(s) and s[i + 1] == "H":
            ch = "F"
            i += 1
        elif ch == "H" and (
            s[i - 1] not in "AEIOU"
            or (i + 1 < len(s) and s[i + 1] not in "AEIOU")
            or (i + 1 == len(s))
        ):
            if s[i - 1] in "AEIOU":
                ch = "A"
            else:
                ch = s[i - 1]
        elif ch == "W" and s[i - 1] in "AEIOU":
            ch = s[i - 1]

        if ch[-1] != key[-1][-1]:
            key.append(ch)

        i += 1

    key = "".join(key)

    # step 5 - remove trailing S
    if key.endswith("S") and key != "S":
        key = key[:-1]

    # step 6 - replace AY w/ Y
    if key.endswith("AY"):
        key = key[:-2] + "Y"

    # step 7 - remove trailing A
    if key.endswith("A") and key != "A":
        key = key[:-1]

    # step 8 was already done

    return key


def match_rating_codex(s):
    _check_type(s)

    # we ignore spaces
    s = s.upper().replace(" ", "")
    # any remaining non-alphabetic characters are invalid
    if not s.isalpha():
        raise ValueError("string must be alphabetic")

    codex = []

    prev = None
    first = True
    for c in s:
        # starting character
        # or consonant not preceded by same consonant
        if first or (c not in "AEIOU" and c != prev):
            codex.append(c)

        prev = c
        first = False

    # just use first/last 3
    if len(codex) > 6:
        return "".join(codex[:3] + codex[-3:])
    else:
        return "".join(codex)


def match_rating_comparison(s1, s2):
    codex1 = match_rating_codex(s1)
    codex2 = match_rating_codex(s2)
    len1 = len(codex1)
    len2 = len(codex2)
    res1 = []
    res2 = []

    # length differs by 3 or more, no result
    if abs(len1 - len2) >= 3:
        return None

    # get minimum rating based on sums of codexes
    lensum = len1 + len2
    if lensum <= 4:
        min_rating = 5
    elif lensum <= 7:
        min_rating = 4
    elif lensum <= 11:
        min_rating = 3
    else:
        min_rating = 2

    # strip off common prefixes
    for c1, c2 in zip_longest(codex1, codex2):
        if c1 != c2:
            if c1:
                res1.append(c1)
            if c2:
                res2.append(c2)

    unmatched_count1 = unmatched_count2 = 0
    for c1, c2 in zip_longest(reversed(res1), reversed(res2)):
        if c1 != c2:
            if c1:
                unmatched_count1 += 1
            if c2:
                unmatched_count2 += 1

    return (6 - max(unmatched_count1, unmatched_count2)) >= min_rating


def metaphone(s):
    _check_type(s)

    result = []

    s = _normalize(s.lower())

    # skip first character if s starts with these
    if s.startswith(("kn", "gn", "pn", "wr", "ae")):
        s = s[1:]

    i = 0

    while i < len(s):
        c = s[i]
        next = s[i + 1] if i < len(s) - 1 else "*****"
        nextnext = s[i + 2] if i < len(s) - 2 else "*****"

        # skip doubles except for cc
        if c == next and c != "c":
            i += 1
            continue

        if c in "aeiou":
            if i == 0 or s[i - 1] == " ":
                result.append(c)
        elif c == "b":
            if (not (i != 0 and s[i - 1] == "m")) or next:
                result.append("b")
        elif c == "c":
            if next == "i" and nextnext == "a" or next == "h":
                result.append("x")
                i += 1
            elif next in "iey":
                result.append("s")
                i += 1
            else:
                result.append("k")
        elif c == "d":
            if next == "g" and nextnext in "iey":
                result.append("j")
                i += 2
            else:
                result.append("t")
        elif c in "fjlmnr":
            result.append(c)
        elif c == "g":
            if next in "iey":
                result.append("j")
            elif next == "h" and nextnext and nextnext not in "aeiou":
                i += 1
            elif next == "n" and not nextnext:
                i += 1
            else:
                result.append("k")
        elif c == "h":
            if i == 0 or next in "aeiou" or s[i - 1] not in "aeiou":
                result.append("h")
        elif c == "k":
            if i == 0 or s[i - 1] != "c":
                result.append("k")
        elif c == "p":
            if next == "h":
                result.append("f")
                i += 1
            else:
                result.append("p")
        elif c == "q":
            result.append("k")
        elif c == "s":
            if next == "h":
                result.append("x")
                i += 1
            elif next == "i" and nextnext in "oa":
                result.append("x")
                i += 2
            else:
                result.append("s")
        elif c == "t":
            if next == "i" and nextnext in "oa":
                result.append("x")
            elif next == "h":
                result.append("0")
                i += 1
            elif next != "c" or nextnext != "h":
                result.append("t")
        elif c == "v":
            result.append("f")
        elif c == "w":
            if i == 0 and next == "h":
                i += 1
                result.append("w")
            elif next in "aeiou":
                result.append("w")
        elif c == "x":
            if i == 0:
                if next == "h" or (next == "i" and nextnext in "oa"):
                    result.append("x")
                else:
                    result.append("s")
            else:
                result.append("k")
                result.append("s")
        elif c == "y":
            if next in "aeiou":
                result.append("y")
        elif c == "z":
            result.append("s")
        elif c == " ":
            if len(result) > 0 and result[-1] != " ":
                result.append(" ")

        i += 1

    return "".join(result).upper()
