use crate::common::FastVec;
use ahash::AHashMap;
use smallvec::smallvec;
use std::cmp;
use unicode_segmentation::UnicodeSegmentation;

fn range_vec(size: usize) -> FastVec<usize> {
    let mut vec = FastVec::new();
    let mut p: usize = 0;
    vec.resize_with(size, || {
        p += 1;
        p - 1
    });
    vec
}

pub fn vec_levenshtein_distance<T: PartialEq>(v1: &FastVec<T>, v2: &FastVec<T>) -> usize {
    let rows = v1.len() + 1;
    let cols = v2.len() + 1;

    if rows == 1 {
        return cols - 1;
    } else if cols == 1 {
        return rows - 1;
    }

    let mut cur = range_vec(cols);

    for r in 1..rows {
        // make a copy of the previous row so we can edit cur
        let prev = cur.clone();
        cur = smallvec![0; cols];
        cur[0] = r;
        for c in 1..cols {
            // deletion cost or insertion cost
            let del_or_ins = cmp::min(prev[c] + 1, cur[c - 1] + 1);
            let edit = prev[c - 1] + (if v1[r - 1] == v2[c - 1] { 0 } else { 1 });
            cur[c] = cmp::min(del_or_ins, edit);
        }
    }

    // last element of bottom row
    cur[cols - 1]
}

pub fn vec_damerau_levenshtein_distance<T: Eq + std::hash::Hash>(
    v1: &FastVec<T>,
    v2: &FastVec<T>,
) -> usize {
    let len1 = v1.len();
    let len2 = v2.len();
    let infinite = len1 + len2;

    let mut item_position = AHashMap::with_capacity(cmp::max(len1, len2));
    // distance matrix
    // try using a flat array instead of a 2d vec for speed
    let mut score: Vec<usize> = vec![0; (len1 + 2) * (len2 + 2)];
    let idx = |i: usize, j: usize| (len2 + 2) * i + j;
    //let mut score: FastVec<FastVec<usize>> = smallvec![smallvec![0; len2 + 2]; len1 + 2];

    score[0] = infinite;
    for i in 0..=len1 {
        score[idx(i + 1, 0)] = infinite;
        score[idx(i + 1, 1)] = i;
    }
    for i in 0..=len2 {
        score[idx(0, i + 1)] = infinite;
        score[idx(1, i + 1)] = i;
    }

    for i in 1..len1 + 1 {
        let mut db = 0;
        for j in 1..len2 + 1 {
            let i1 = item_position.entry(&v2[j - 1]).or_insert(0);
            let j1 = db;
            let mut cost = 1;
            if v1[i - 1] == v2[j - 1] {
                cost = 0;
                db = j;
            }

            // min of the four options
            score[idx(i + 1, j + 1)] = cmp::min(
                // substitution & insertion
                cmp::min(score[idx(i, j)] + cost, score[idx(i + 1, j)] + 1),
                cmp::min(
                    // deletion & transposition
                    score[idx(i, j + 1)] + 1,
                    score[idx(*i1, j1)] + (i - *i1 - 1) + 1 + (j - j1 - 1),
                ),
            )
        }
        // store the position of this character for transpositions
        item_position.insert(&v1[i - 1], i);
    }

    score[idx(len1 + 1, len2 + 1)]
}

pub fn levenshtein_distance(s1: &str, s2: &str) -> usize {
    if s1 == s2 {
        return 0;
    }

    let us1 = UnicodeSegmentation::graphemes(s1, true).collect::<FastVec<&str>>();
    let us2 = UnicodeSegmentation::graphemes(s2, true).collect::<FastVec<&str>>();

    vec_levenshtein_distance(&us1, &us2)
}

pub fn damerau_levenshtein_distance(s1: &str, s2: &str) -> usize {
    if s1 == s2 {
        return 0;
    }

    let us1 = UnicodeSegmentation::graphemes(s1, true).collect::<FastVec<&str>>();
    let us2 = UnicodeSegmentation::graphemes(s2, true).collect::<FastVec<&str>>();

    vec_damerau_levenshtein_distance(&us1, &us2)
}

#[cfg(test)]
mod test {
    use super::*;
    use crate::testutils::testutils;
    #[test]
    fn test_levenshtein() {
        testutils::test_distance_func("testdata/levenshtein.csv", levenshtein_distance);
    }

    #[test]
    fn test_damerau_levenshtein() {
        testutils::test_distance_func(
            "testdata/damerau_levenshtein.csv",
            damerau_levenshtein_distance,
        );
    }
}
