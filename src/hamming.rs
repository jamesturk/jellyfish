use crate::common::FastVec;
use unicode_segmentation::UnicodeSegmentation;

pub fn vec_hamming_distance<T: PartialEq>(s1: &FastVec<T>, s2: &FastVec<T>) -> usize {
    let (longer, shorter) = if s1.len() > s2.len() {
        (s1, s2)
    } else {
        (s2, s1)
    };

    // distance is difference in length + differing chars
    let mut distance = longer.len() - shorter.len();
    for (i, c) in shorter.iter().enumerate() {
        if *c != longer[i] {
            distance += 1
        }
    }

    distance
}

pub fn hamming_distance(s1: &str, s2: &str) -> usize {
    let us1 = UnicodeSegmentation::graphemes(s1, true).collect::<FastVec<&str>>();
    let us2 = UnicodeSegmentation::graphemes(s2, true).collect::<FastVec<&str>>();

    vec_hamming_distance(&us1, &us2)
}

#[cfg(test)]
mod test {
    use super::*;
    use crate::testutils::testutils;
    #[test]
    fn test_hamming() {
        testutils::test_distance_func("testdata/hamming.csv", hamming_distance);
    }
}
