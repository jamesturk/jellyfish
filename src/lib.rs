use jellyfish;
use pyo3::prelude::*;

/// Calculates the Damerau-Levenshtein distance between two strings.
#[pyfunction]
fn damerau_levenshtein_distance(a: &str, b: &str) -> PyResult<usize> {
    Ok(jellyfish::damerau_levenshtein_distance(a, b))
}

// Calculates the Hamming distance between two strings.
#[pyfunction]
fn hamming_distance(a: &str, b: &str) -> PyResult<usize> {
    Ok(jellyfish::hamming_distance(a, b))
}

// Calculates the Jaro similarity between two strings.
#[pyfunction]
fn jaro_similarity(a: &str, b: &str) -> PyResult<f64> {
    Ok(jellyfish::jaro_similarity(a, b))
}

// Calculates the Jaro-Winkler similarity between two strings.
#[pyfunction]
fn jaro_winkler_similarity(a: &str, b: &str, long_tolerance: Option<bool>) -> PyResult<f64> {
    match long_tolerance {
        Some(true) => Ok(jellyfish::jaro_winkler_similarity_longtol(a, b)),
        _ => Ok(jellyfish::jaro_winkler_similarity(a, b)),
    }
}

// Calculates the Levenshtein distance between two strings.
#[pyfunction]
fn levenshtein_distance(a: &str, b: &str) -> PyResult<usize> {
    Ok(jellyfish::levenshtein_distance(a, b))
}

// Calculates the Match Rating Approach code for a string.
#[pyfunction]
fn match_rating_codex(a: &str) -> PyResult<String> {
    Ok(jellyfish::match_rating_codex(a))
}

// Calculates the Match Rating Approach comparison for two strings.
#[pyfunction]
fn match_rating_comparison(a: &str, b: &str) -> Option<bool> {
    match jellyfish::match_rating_comparison(a, b) {
        Ok(value) => Some(value),
        Err(_) => None,
    }
}

/// Calculates the NYSIIS phonetic encoding of a string.
#[pyfunction]
fn nysiis(a: &str) -> PyResult<String> {
    Ok(jellyfish::nysiis(a))
}

/// Calculates the phonetic encoding of a string using the Soundex algorithm.
#[pyfunction]
fn soundex(a: &str) -> PyResult<String> {
    Ok(jellyfish::soundex(a))
}

/// Calculates the phonetic encoding of a string using the Metaphone algorithm.
#[pyfunction]
fn metaphone(a: &str) -> PyResult<String> {
    Ok(jellyfish::metaphone(a))
}

/// A Python module implemented in Rust.
#[pymodule]
fn rustyfish(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(damerau_levenshtein_distance, m)?)?;
    m.add_function(wrap_pyfunction!(hamming_distance, m)?)?;
    m.add_function(wrap_pyfunction!(jaro_similarity, m)?)?;
    m.add_function(wrap_pyfunction!(jaro_winkler_similarity, m)?)?;
    m.add_function(wrap_pyfunction!(levenshtein_distance, m)?)?;
    m.add_function(wrap_pyfunction!(match_rating_codex, m)?)?;
    m.add_function(wrap_pyfunction!(match_rating_comparison, m)?)?;
    m.add_function(wrap_pyfunction!(nysiis, m)?)?;
    m.add_function(wrap_pyfunction!(soundex, m)?)?;
    m.add_function(wrap_pyfunction!(metaphone, m)?)?;

    Ok(())
}
