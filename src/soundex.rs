use crate::common::FastVec;
use unicode_normalization::UnicodeNormalization;

pub fn soundex(s: &str) -> String {
    if s.is_empty() {
        return String::from("");
    }

    let v = &s.to_uppercase().nfkd().collect::<FastVec<char>>();

    let mut result = FastVec::new();
    result.push(v[0]);

    let replacement = |ch| match ch {
        'B' | 'F' | 'P' | 'V' => '1',
        'C' | 'G' | 'J' | 'K' | 'Q' | 'S' | 'X' | 'Z' => '2',
        'D' | 'T' => '3',
        'L' => '4',
        'M' | 'N' => '5',
        'R' => '6',
        _ => '*',
    };

    // find would be replacement for first character
    let mut last = replacement(v[0]);

    // loop over remaining letters
    for letter in v.iter().skip(1) {
        let sub = replacement(*letter);
        if sub != '*' {
            if sub != last {
                result.push(sub);
                if result.len() == 4 {
                    break;
                }
            }
            last = sub;
        } else if *letter != 'H' && *letter != 'W' {
            last = '*';
        }
    }

    while result.len() < 4 {
        result.push('0');
    }
    let mut str_key = String::new();
    for k in result {
        str_key.push(k);
    }
    str_key
}

#[cfg(test)]
mod test {
    use super::*;
    use crate::testutils::testutils;
    #[test]
    fn test_soundex() {
        testutils::test_str_func("testdata/soundex.csv", soundex);
    }
}
