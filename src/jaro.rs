use crate::common::FastVec;
use smallvec::smallvec;
use std::cmp;
use unicode_segmentation::UnicodeSegmentation;

enum JaroVersion {
    Pure,
    Winkler,
    WinklerLongTolerance,
}

fn vec_jaro_or_winkler<T: PartialEq>(
    s1: &FastVec<T>,
    s2: &FastVec<T>,
    version: JaroVersion,
) -> f64 {
    let s1_len = s1.len();
    let s2_len = s2.len();

    if s1_len == 0 || s2_len == 0 {
        return 0.0;
    }

    let min_len = cmp::min(s1_len, s2_len);
    let mut search_range = cmp::max(s1_len, s2_len);
    search_range = (search_range / 2).saturating_sub(1);

    let mut s1_flags: FastVec<bool> = smallvec![false; s1_len];
    let mut s2_flags: FastVec<bool> = smallvec![false; s2_len];
    let mut common_chars = 0;

    // looking only within search range, count & flag matched pairs
    for (i, s1_ch) in s1.iter().enumerate() {
        // avoid underflow on i - search_range
        let low = i.saturating_sub(search_range);
        let hi = cmp::min(i + search_range, s2_len - 1);
        for j in low..hi + 1 {
            if !s2_flags[j] && s2[j] == *s1_ch {
                s1_flags[i] = true;
                s2_flags[j] = true;
                common_chars += 1;
                break;
            }
        }
    }

    // no characters match
    if common_chars == 0 {
        return 0.0;
    }

    // count transpositions
    let mut k = 0;
    let mut trans_count = 0;
    for (i, s1_f) in s1_flags.iter().enumerate() {
        if *s1_f {
            let mut j = k;
            while j < s2_len {
                if s2_flags[j] {
                    k = j + 1;
                    break;
                }
                j += 1;
            }
            if s1[i] != s2[j] {
                trans_count += 1
            }
        }
    }
    // need to do floor division then cast to float
    let trans_count = (trans_count / 2) as f64;
    let common_charsf = common_chars as f64;
    let s1_lenf = s1_len as f64;
    let s2_lenf = s2_len as f64;

    // adjust for similarities in nonmatched characters
    let mut weight = (common_charsf / s1_lenf
        + common_charsf / s2_lenf
        + (common_charsf - trans_count) / common_charsf)
        / 3.0;

    // check which version to run
    let (winklerize, long_tolerance) = match version {
        JaroVersion::Pure => (false, false),
        JaroVersion::Winkler => (true, false),
        JaroVersion::WinklerLongTolerance => (true, true),
    };

    // winkler modification: continue to boost similar strings
    if winklerize && weight > 0.7 {
        let mut i = 0;
        let j = cmp::min(min_len, 4);
        while i < j && s1[i] == s2[i] {
            // TODO: also had s1[i] in Python, necessary?
            i += 1;
        }
        let fi = i as f64;
        if i > 0 {
            weight += fi * 0.1 * (1.0 - weight);
        }

        // optional adjustment for long strings
        // after agreeing beginning items, at least two or more must agree
        // and agreed items must be more than half of remaining items
        if long_tolerance && min_len > 4 && common_chars > i + 1 && 2 * common_chars >= min_len + i
        {
            weight +=
                (1.0 - weight) * (common_charsf - fi - 1.0) / (s1_lenf + s2_lenf - fi * 2.0 + 2.0);
        }
    }

    weight
}

pub fn vec_jaro_similarity<T: PartialEq>(s1: &FastVec<T>, s2: &FastVec<T>) -> f64 {
    vec_jaro_or_winkler(s1, s2, JaroVersion::Pure)
}

pub fn vec_jaro_winkler_similarity<T: PartialEq>(s1: &FastVec<T>, s2: &FastVec<T>) -> f64 {
    vec_jaro_or_winkler(s1, s2, JaroVersion::Winkler)
}

pub fn vec_jaro_winkler_similarity_longtol<T: PartialEq>(s1: &FastVec<T>, s2: &FastVec<T>) -> f64 {
    vec_jaro_or_winkler(s1, s2, JaroVersion::WinklerLongTolerance)
}

pub fn jaro_similarity(s1: &str, s2: &str) -> f64 {
    let us1 = UnicodeSegmentation::graphemes(s1, true).collect::<FastVec<&str>>();
    let us2 = UnicodeSegmentation::graphemes(s2, true).collect::<FastVec<&str>>();
    vec_jaro_similarity(&us1, &us2)
}

pub fn jaro_winkler_similarity(s1: &str, s2: &str) -> f64 {
    let us1 = UnicodeSegmentation::graphemes(s1, true).collect::<FastVec<&str>>();
    let us2 = UnicodeSegmentation::graphemes(s2, true).collect::<FastVec<&str>>();
    vec_jaro_winkler_similarity(&us1, &us2)
}

pub fn jaro_winkler_similarity_longtol(s1: &str, s2: &str) -> f64 {
    let us1 = UnicodeSegmentation::graphemes(s1, true).collect::<FastVec<&str>>();
    let us2 = UnicodeSegmentation::graphemes(s2, true).collect::<FastVec<&str>>();
    vec_jaro_winkler_similarity_longtol(&us1, &us2)
}

#[cfg(test)]
mod test {
    use super::*;
    use crate::testutils::testutils;
    #[test]
    fn test_jaro() {
        testutils::test_similarity_func_two_args("testdata/jaro_distance.csv", jaro_similarity);
    }

    #[test]
    fn test_jaro_winkler() {
        testutils::test_similarity_func_two_args("testdata/jaro_winkler.csv", jaro_winkler_similarity);
    }

    #[test]
    fn test_jaro_winkler_longtol() {
        testutils::test_similarity_func_two_args(
            "testdata/jaro_winkler_longtol.csv",
            jaro_winkler_similarity_longtol,
        );
    }
}
