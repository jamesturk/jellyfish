use std::cmp;
use std::collections::HashMap;
use unicode_segmentation::UnicodeSegmentation;

fn range_vec(size: usize) -> Vec<usize> {
    let mut vec = Vec::new();
    let mut p: usize = 0;
    vec.resize_with(size, || {
        p += 1;
        p - 1
    });
    return vec;
}

pub fn vec_levenshtein_distance<T: PartialEq>(v1: &Vec<T>, v2: &Vec<T>) -> usize {
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
        let prev = cur.to_vec();
        cur = vec![0; cols];
        cur[0] = r;
        for c in 1..cols {
            // deletion cost or insertion cost
            let del_or_ins = cmp::min(prev[c] + 1, cur[c - 1] + 1);
            let edit = prev[c - 1] + (if v1[r - 1] == v2[c - 1] { 0 } else { 1 });
            cur[c] = cmp::min(del_or_ins, edit);
        }
    }

    // last element of bottom row
    return cur[cur.len() - 1];
}

pub fn vec_damerau_levenshtein_distance<T: Eq + std::hash::Hash>(
    v1: &Vec<T>,
    v2: &Vec<T>,
) -> usize {
    let len1 = v1.len();
    let len2 = v2.len();
    let infinite = len1 + len2;

    let mut item_position = HashMap::new();
    // distance matrix
    let mut score = vec![vec![0; len2 + 2]; len1 + 2];
    score[0][0] = infinite;
    for i in 0..len1 + 1 {
        score[i + 1][0] = infinite;
        score[i + 1][1] = i;
    }
    for i in 0..len2 + 1 {
        score[0][i + 1] = infinite;
        score[1][i + 1] = i;
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
            score[i + 1][j + 1] = cmp::min(
                // substitution & insertion
                cmp::min(score[i][j] + cost, score[i + 1][j] + 1),
                cmp::min(
                    // deletion & transposition
                    score[i][j + 1] + 1,
                    score[*i1][j1] + (i - *i1 - 1) + 1 + (j - j1 - 1),
                ),
            )
        }
        // store the position of this character for transpositions
        item_position.insert(&v1[i - 1], i);
    }

    return score[len1 + 1][len2 + 1];
}

pub fn levenshtein_distance(s1: &str, s2: &str) -> usize {
    if s1 == s2 {
        return 0;
    }

    let us1 = UnicodeSegmentation::graphemes(s1, true).collect::<Vec<&str>>();
    let us2 = UnicodeSegmentation::graphemes(s2, true).collect::<Vec<&str>>();

    vec_levenshtein_distance(&us1, &us2)
}

pub fn damerau_levenshtein_distance(s1: &str, s2: &str) -> usize {
    if s1 == s2 {
        return 0;
    }

    let us1 = UnicodeSegmentation::graphemes(s1, true).collect::<Vec<&str>>();
    let us2 = UnicodeSegmentation::graphemes(s2, true).collect::<Vec<&str>>();

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
