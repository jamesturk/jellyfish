import unicodedata

def _normalize(s):
    return unicodedata.normalize('NFKD', unicode(s))

def levenshtein_distance(s1, s2):
    return _levenshtein_distance(s1, s2, False)

def damerau_levenshtein_distance(s1, s2):
    return _levenshtein_distance(s1, s2, True)

def _levenshtein_distance(s1, s2, damerau=False):
    if s1 == s2:
        return 0
    rows = len(s1)+1
    cols = len(s2)+1

    if not s1:
        return cols-1
    if not s2:
        return rows-1

    prev = None
    cur = range(cols)
    for r in range(1, rows):
        prevprev, prev, cur = prev, cur, [r] + [0]*(cols-1)
        for c in range(1, cols):
            deletion = prev[c] + 1
            insertion = cur[c-1] + 1
            edit = prev[c-1] + (0 if s1[r-1] == s2[c-1] else 1)
            cur[c] = min(edit, deletion, insertion)

            # damerau
            if (damerau and r > 1 and c > 1 and s1[r-1] == s2[c-2]
                    and s1[r-2] == s2[c-1]):
                cur[c] = min(cur[c], prevprev[r-2] + edit)

    return cur[-1]


def soundex(s):
    if not s:
        return s

    s = _normalize(s)

    replacements = (('bfpv', '1'),
                    ('cgjkqsxz', '2'),
                    ('dt', '3'),
                    ('l', '4'),
                    ('mn', '5'),
                    ('r', '6')
                   )
    result = [s[0]]
    count = 1

    # find would-be replacment for first character
    for lset, sub in replacements:
        if s[0].lower() in lset:
            last = sub
            break
    else:
        last = None

    for letter in s[1:]:
        for lset, sub in replacements:
            if letter.lower() in lset:
                if sub != last:
                    result.append(sub)
                    count += 1
                last = sub
                break
        else:
            last = None
        if count == 4:
            break

    result += '0'*(4-count)
    return ''.join(result)


def hamming_distance(s1, s2):
    # ensure length of s1 >= s2
    if len(s2) > len(s1):
        s1, s2 = s2, s1

    # distance is difference in length + differing chars
    distance = len(s1) - len(s2)
    for i, c in enumerate(s2):
        if c != s1[i]:
            distance += 1

    return distance
