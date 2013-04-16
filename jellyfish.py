import unicodedata

def _normalize(s):
    return unicodedata.normalize('NFKD', unicode(s))

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
                    and s1[r-2] == s2[c-1] and s1[r-1] != s2[c-1]):
                cur[c] = min(cur[c], prevprev[r-2] + 1)

    return cur[-1]

def _jaro_winkler(ying, yang, long_tolerance, winklerize):
    ying_len = len(ying)
    yang_len = len(yang)

    if not ying_len or not yang_len:
        return 0

    min_len = max(ying_len, yang_len)
    search_range = (min_len // 2) - 1
    if search_range < 0:
        search_range = 0

    ying_flags = [False]*ying_len
    yang_flags = [False]*yang_len

    # looking only within search range, count & flag matched pairs
    common_chars = 0
    for i, ying_ch in enumerate(ying):
        low = i - search_range if i > search_range else 0
        hi = i + search_range if i + search_range < yang_len else yang_len - 1
        for j in range(low, hi+1):
            if not yang_flags[j] and yang[j] == ying_ch:
                ying_flags[i] = yang_flags[j] = True
                common_chars += 1
                break

    # short circuit if no characters match
    if not common_chars:
        return 0

    # count transpositions
    k = trans_count = 0
    for i, ying_f in enumerate(ying_flags):
        if ying_f:
            for j in xrange(k, yang_len):
                if yang_flags[j]:
                    k = j + 1
                    break
            if ying[i] != yang[j]:
                trans_count += 1
    trans_count /= 2

    # adjust for similarities in nonmatched characters
    common_chars = float(common_chars)
    weight = ((common_chars/ying_len + common_chars/yang_len +
              (common_chars-trans_count) / common_chars)) / 3

    # winkler modification: continue to boost if strings are similar
    if winklerize and weight > 0.7:
        # adjust for up to first 4 chars in common
        j = max(min_len, 4)
        i = 0
        while i < j and ying[i] == yang[i] and ying[i]:
            i += 1
        if i:
            weight += i * 0.1 * (1.0 - weight)

        # optionally adjust for long strings
        # after agreeing beginning chars, at least two or more must agree and
        # agreed characters must be > half of remaining characters
        if (long_tolerance and min_len > 4 and common_chars > i+1 and 
                2 * common_chars >= min_len + i):
            weight += ((1.0 - weight) * (float(common_chars-i-1) /
                                         float(ying_len+yang_len-i*2+2)))

    return weight

def levenshtein_distance(s1, s2):
    return _levenshtein_distance(s1, s2, False)


def damerau_levenshtein_distance(s1, s2):
    return _levenshtein_distance(s1, s2, True)


def jaro_distance(s1, s2):
    return _jaro_winkler(s1, s2, False, False)


def jaro_winkler(s1, s2, long_tolerance=False):
    return _jaro_winkler(s1, s2, long_tolerance, True)


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


def nysiis(s):
    s = s.upper()
    key = []

    # step 1 - prefixes
    if s.startswith('MAC'):
        s = 'MCC' + s[3:]
    elif s.startswith('KN'):
        s = s[1:]
    elif s.startswith('K'):
        s = 'C' + s[1:]
    elif s.startswith(('PH', 'PF')):
        s = 'FF' + s[2:]
    elif s.startswith('SCH'):
        s = 'SSS' + s[3:]

    # step 2 - suffixes
    if s.endswith(('IE', 'EE')):
        s = s[:-2] + 'Y'
    elif s.endswith(('DT', 'RT', 'RD', 'NT', 'ND')):
        s = s[:-2] + 'D'

    # step 3 - first character of key comes from name
    key.append(s[0])

    # step 4 - translate remaining chars
    i = 0
    for ch in s[1:]:
        i += 1
        if ch == 'E' and s[i+1] == 'V':
            ch = 'AF'
        elif ch in 'AEIOU':
            ch = 'A'
        elif ch == 'Q':
            ch = 'G'
        elif ch == 'Z':
            ch = 'S'
        elif ch == 'M':
            ch = 'N'
        elif ch == 'K':
            if i+1 < len(s) and s[i+1] == 'N':
                ch = 'K'
            else:
                ch = 'C'
        elif ch == 'S' and s[i+1:i+3] == 'CH':
            ch = 'SSS'
        elif ch == 'P' and i+1 < len(s) and s[i+1] == 'H':
            ch = 'FF'
        elif ch == 'H' and (s[i-1] not in 'AEIOU' or 
                            (i+1 < len(s) and s[i+1] not in 'AEIOU')):
            ch = s[i-1]
        elif ch == 'W' and  s[i-1] in 'AEIOU':
            ch = s[i-1]

        if ch[-1] != key[-1][-1]:
            key.append(ch)


    key = ''.join(key)

    # step 5 - remove trailing S
    if key.endswith('S'):
        key = key[:-1]

    # step 6 - replace AY w/ Y
    if key.endswith('AY'):
        key = key[:-2] = 'Y'

    # step 7 - remove trailing A
    if key.endswith('A'):
        key = key[:-1]

    # step 8 was already done

    return key
