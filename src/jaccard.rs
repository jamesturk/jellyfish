use std::borrow::Cow;
use std::collections::HashSet;

pub fn jaccard_similarity(s1: &str, s2: &str, ngram_size: Option<usize>) -> f64 {
    // 1. Tokenize into ngrams
    let grams1: HashSet<String> = get_ngrams(s1, ngram_size)
        .into_iter()
        .map(|cow| cow.into_owned())
        .collect();
    let grams2: HashSet<String> = get_ngrams(s2, ngram_size)
        .into_iter()
        .map(|cow| cow.into_owned())
        .collect();

    // 2. Calculate intersection and union sizes
    let intersection_size: usize = grams1.iter().filter(|gram| grams2.contains(*gram)).count();
    let union_size: usize = grams1.len() + grams2.len() - intersection_size;

    // 3. Calculate Jaccard index
    if union_size == 0 {
        0.0
    } else {
        intersection_size as f64 / union_size as f64
    }
}

fn get_ngrams(s: &str, n: Option<usize>) -> Vec<Cow<'_, str>> {
    if let Some(size) = n {
        // Non-overlapping character-level n-grams
        s.chars()
            .collect::<Vec<char>>()
            .chunks(size) // Use chunks() for non-overlapping groups
            .map(|chunk| Cow::from(chunk.iter().collect::<String>()))
            .collect()
    } else {
        // Word-level "n-grams" (i.e., words)
        s.split_whitespace()
            .map(Cow::from)
            .collect()
    }
}



#[cfg(test)]
mod test {
    use super::*; // Import the Jaccard functions
    use crate::testutils::testutils; // Import the test utils

    #[test]
    fn test_jaccard_similarity() {
        testutils::test_similarity_func_three_args("testdata/jaccard.csv", jaccard_similarity);
    }
}
