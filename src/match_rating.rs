use crate::common::FastVec;
use std::cmp;
use unicode_segmentation::UnicodeSegmentation;

pub fn match_rating_codex(s: &str) -> Result<String, String> {
    // match rating only really makes sense on strings

    let s = &s.to_uppercase()[..];
    let v = UnicodeSegmentation::graphemes(s, true).collect::<FastVec<&str>>();
    let mut codex = String::new();
    let mut prev = "~tmp~";
    let is_alpha = s.chars().all(|c| c.is_alphabetic() || c == ' ');

    if !is_alpha {
        return Err(String::from("Strings must only contain alphabetical characters"));
    }

    for (i, c) in v.iter().enumerate() {
        let vowel = *c == "A" || *c == "E" || *c == "I" || *c == "O" || *c == "U";
        // not a space || starting char & vowel || non-double consonant
        if *c != " " && (i == 0 && vowel) || (!vowel && *c != prev) {
            codex.push_str(c);
        }
        prev = c;
    }

    if codex.len() > 6 {
        // not safe to take a slice without conversion to chars() since there
        // can be unicode left, this implementation matches the Python one
        // even though MRC really shouldn't be used with unicode chars
        let first_three: String = codex.chars().take(3).collect();
        let last_three: String = codex.chars().rev().take(3).collect::<String>().chars().rev().collect();
        return Ok(first_three + &last_three);
    }

    Ok(codex)
}

pub fn match_rating_comparison(s1: &str, s2: &str) -> Result<bool, String> {
    let codex1 = match_rating_codex(s1)?;
    let codex2 = match_rating_codex(s2)?;

    // need to know which is longer for comparisons later
    let (longer, shorter) = if codex1.len() > codex2.len() {
        (codex1, codex2)
    } else {
        (codex2, codex1)
    };

    let lensum = longer.len() + shorter.len();

    // can't do a comparison when difference is 3 or greater
    if longer.len() - shorter.len() >= 3 {
        return Err(String::from("strings differ in length by more than 2"));
    }

    // remove matching characters going forward
    let mut res1 = FastVec::new();
    let mut res2 = FastVec::new();
    let mut iter1 = longer.chars();
    let mut iter2 = shorter.chars();
    loop {
        match (iter1.next(), iter2.next()) {
            (Some(x), Some(y)) => {
                if x != y {
                    res1.push(x);
                    res2.push(y)
                }
            }
            (Some(x), None) => res1.push(x),
            (None, Some(y)) => res2.push(y),
            (None, None) => break,
        };
    }

    // count unmatched characters going backwards
    let mut unmatched_count1 = 0;
    let mut unmatched_count2 = 0;
    let mut iter1 = res1.iter().rev();
    let mut iter2 = res2.iter().rev();
    loop {
        match (iter1.next(), iter2.next()) {
            (Some(x), Some(y)) => {
                if x != y {
                    unmatched_count1 += 1;
                    unmatched_count2 += 1;
                }
            }
            (Some(_), None) => unmatched_count1 += 1,
            (None, Some(_)) => unmatched_count2 += 1,
            (None, None) => break,
        };
    }

    let score = 6 - cmp::max(unmatched_count1, unmatched_count2);
    match lensum {
        0..=4 => Ok(score >= 5),
        5..=7 => Ok(score >= 4),
        8..=11 => Ok(score >= 3),
        _ => Ok(score >= 2),
    }
}

#[cfg(test)]
mod test {
    use super::*;
    use crate::testutils::testutils;
    pub fn mrc_unwrapped(s: &str) -> String {
        return match_rating_codex(s).unwrap();
    }

    #[test]
    fn test_match_rating() {
        testutils::test_str_func("testdata/match_rating_codex.csv", mrc_unwrapped);
    }

    #[test]
    fn test_match_rating_comparison() {
        // TODO: switch to using CSV
        assert!(match_rating_comparison("Bryne", "Boern").unwrap());
        assert!(match_rating_comparison("Smith", "Smyth").unwrap());
        assert!(match_rating_comparison("Ed", "Ad").unwrap());
        assert!(match_rating_comparison("Catherine", "Kathryn").unwrap());
        assert!(!match_rating_comparison("Michael", "Mike").unwrap());
    }

    #[test]
    fn test_match_rating_comparison_err() {
        let result = match_rating_comparison("Tim", "Timothy");
        assert_eq!(result.is_err(), true);
    }

    #[test]
    fn test_match_rating_codex_bad_str() {
        let result = match_rating_codex("i’m going home");
        assert!(result.is_err());
    }
}
