use crate::common::FastVec;
use smallvec::{smallvec, SmallVec};
use unicode_segmentation::UnicodeSegmentation;

fn isvowel(s: &str) -> bool {
    matches!(s, "A" | "E" | "I" | "O" | "U")
}

pub fn nysiis(s: &str) -> String {
    if s.is_empty() {
        return String::from("");
    }

    let s = &s.to_uppercase()[..];
    let mut v = UnicodeSegmentation::graphemes(s, true).collect::<FastVec<&str>>();

    // step 1: handle prefixes
    if s.starts_with("MAC") {
        v[1] = "C"; // switch MAC to MCC
    } else if s.starts_with("KN") {
        v.remove(0); // strip leading K from KN
    } else if s.starts_with('K') {
        v[0] = "C"; // switch K to C
    } else if s.starts_with("PH") || s.starts_with("PF") {
        v[0] = "F";
        v[1] = "F"; // switch these to FF
    } else if s.starts_with("SCH") {
        v[1] = "S";
        v[2] = "S"; // switch SCH to SSS
    }

    // step 2: suffixes
    if s.ends_with("IE") || s.ends_with("EE") {
        v.pop();
        v.pop();
        v.push("Y");
    } else if s.ends_with("DT")
        || s.ends_with("RT")
        || s.ends_with("RD")
        || s.ends_with("NT")
        || s.ends_with("ND")
    {
        v.pop();
        v.pop();
        v.push("D");
    }

    // step 3: key starts with first character of name
    let mut key = FastVec::new();
    key.push(v[0]);

    // step 4: translate remaining characters
    let mut i = 1;

    while i < v.len() {
        let chars: SmallVec<[&str; 3]> = match v[i] {
            "E" if i + 1 < v.len() && v[i + 1] == "V" => {
                i += 1;
                smallvec!["A", "F"]
            }
            "A" | "E" | "I" | "O" | "U" => smallvec!["A"],
            "Q" => smallvec!["G"],
            "Z" => smallvec!["S"],
            "M" => smallvec!["N"],
            "K" => {
                if i + 1 < v.len() && v[i + 1] == "N" {
                    smallvec!["N"]
                } else {
                    smallvec!["C"]
                }
            }
            "S" if i + 2 < v.len() && v[i + 1] == "C" && v[i + 2] == "H" => {
                i += 2;
                smallvec!["S", "S"]
            }
            "P" if i + 1 < v.len() && v[i + 1] == "H" => {
                i += 1;
                smallvec!["F"]
            }
            "H" if !isvowel(v[i - 1])
                || (i + 1 < v.len() && !isvowel(v[i + 1]))
                || (i + 1 == v.len()) =>
            {
                if isvowel(v[i - 1]) {
                    smallvec!["A"]
                } else {
                    smallvec![v[i - 1]]
                }
            }
            "W" if isvowel(v[i - 1]) => smallvec![v[i - 1]],
            _ => smallvec![v[i]],
        };

        if !chars.is_empty() && chars[chars.len() - 1] != key[key.len() - 1] {
            for c in chars {
                key.push(c);
            }
        }

        i += 1;
    }

    // step 5 remove trailing S
    if key[key.len() - 1] == "S" && key.len() > 1 {
        key.pop();
    }

    // step 6 replace AY w/ Y
    if key.ends_with(&["A", "Y"]) {
        key.remove(key.len() - 2);
    }

    // step 7 remove trailing A
    if key[key.len() - 1] == "A" && key.len() > 1 {
        key.pop();
    }

    let mut str_key = String::new();
    for k in key {
        str_key.push_str(k);
    }

    str_key
}

#[cfg(test)]
mod test {
    use super::*;
    use crate::testutils::testutils;
    #[test]
    fn test_nysiis() {
        testutils::test_str_func("testdata/nysiis.csv", nysiis);
    }
}
