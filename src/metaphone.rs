use crate::common::FastVec;
use unicode_normalization::UnicodeNormalization;

pub fn isvowel(s: char) -> bool {
    matches!(s, 'A' | 'E' | 'I' | 'O' | 'U')
}

fn is_iey(s: char) -> bool {
    matches!(s, 'I' | 'E' | 'Y')
}

pub fn metaphone(s: &str) -> String {
    if s.is_empty() {
        return String::from("");
    }

    let s = &s.to_uppercase()[..];
    let mut v = s.nfkd().collect::<FastVec<char>>();
    let mut ret = FastVec::new();

    // skip first character if s starts with these
    if s.starts_with("KN")
        || s.starts_with("GN")
        || s.starts_with("PN")
        || s.starts_with("WR")
        || s.starts_with("AE")
    {
        v.remove(0);
    }

    let mut i = 0;

    while i < v.len() {
        let c = v[i];
        let next = if i + 1 < v.len() { v[i + 1] } else { '*' };
        let nextnext = if i + 2 < v.len() { v[i + 2] } else { '*' };

        // skip doubles except for CC
        if c == next && c != 'C' {
            i += 1;
            continue;
        }

        match c {
            'A' | 'E' | 'I' | 'O' | 'U' => {
                if i == 0 || v[i - 1] == ' ' {
                    ret.push(c);
                }
            }
            'B' => {
                if (i == 0 || v[i - 1] != 'M') || next != '*' {
                    ret.push('B');
                }
            }
            'C' => {
                if next == 'I' && nextnext == 'A' || next == 'H' {
                    i += 1;
                    ret.push('X');
                } else if is_iey(next) {
                    i += 1;
                    ret.push('S');
                } else {
                    ret.push('K');
                }
            }
            'D' => {
                if next == 'G' && is_iey(nextnext) {
                    i += 2;
                    ret.push('J');
                } else {
                    ret.push('T');
                }
            }
            'F' | 'J' | 'L' | 'M' | 'N' | 'R' => {
                ret.push(c);
            }
            'G' => {
                if is_iey(next) {
                    ret.push('J');
                } else if (next == 'H' && nextnext != '*' && !isvowel(nextnext))
                    || (next == 'N' && nextnext == '*')
                {
                    i += 1;
                } else {
                    ret.push('K');
                }
            }
            'H' => {
                if i == 0 || isvowel(next) || !isvowel(v[i - 1]) {
                    ret.push('H');
                }
            }
            'K' => {
                if i == 0 || v[i - 1] != 'C' {
                    ret.push('K');
                }
            }
            'P' => {
                if next == 'H' {
                    i += 1;
                    ret.push('F');
                } else {
                    ret.push('P');
                }
            }
            'Q' => {
                ret.push('K');
            }
            'S' => {
                if next == 'H' {
                    i += 1;
                    ret.push('X');
                } else if next == 'I' && (nextnext == 'O' || nextnext == 'A') {
                    i += 2;
                    ret.push('X');
                } else {
                    ret.push('S');
                }
            }
            'T' => {
                if next == 'I' && (nextnext == 'O' || nextnext == 'A') {
                    ret.push('X');
                } else if next == 'H' {
                    i += 1;
                    ret.push('0');
                } else if next != 'C' || nextnext != 'H' {
                    ret.push('T');
                }
            }
            'V' => {
                ret.push('F');
            }
            'W' => {
                if i == 0 && next == 'H' {
                    i += 1;
                    ret.push('W');
                } else if isvowel(next) {
                    ret.push('W');
                }
            }
            'X' => {
                if i == 0 {
                    if next == 'H' || (next == 'I' && (nextnext == 'O' || nextnext == 'A')) {
                        ret.push('X');
                    } else {
                        ret.push('S');
                    }
                } else {
                    ret.push('K');
                    ret.push('S');
                }
            }
            'Y' => {
                if isvowel(next) {
                    ret.push('Y');
                }
            }
            'Z' => {
                ret.push('S');
            }
            ' ' => {
                if !ret.is_empty() && ret[ret.len() - 1] != ' ' {
                    ret.push(' ');
                }
            }
            _ => {}
        };
        i += 1;
    }

    let mut str_key = String::new();
    for k in ret {
        str_key.push(k);
    }

    str_key
}

#[cfg(test)]
mod test {
    use super::*;
    use crate::testutils::testutils;
    #[test]
    fn test_metaphone() {
        testutils::test_str_func("testdata/metaphone.csv", metaphone);
    }
}
