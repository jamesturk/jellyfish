use crate::damerau_levenshtein_distance as _damerau;
use crate::hamming_distance as _hamming;
use crate::jaccard_similarity as _jaccard;
use crate::jaro_similarity as _jaro;
use crate::jaro_winkler_similarity as _jaro_winkler;
use crate::jaro_winkler_similarity_longtol as _jaro_winkler_long;
use crate::levenshtein_distance as _lev;
use crate::match_rating_codex as _mr_codex;
use crate::match_rating_comparison as _mr_comparison;
use crate::metaphone as _metaphone;
use crate::nysiis as _nysiis;
use crate::soundex as _soundex;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

/// Calculates the Damerau-Levenshtein distance between two strings.
#[pyfunction]
fn damerau_levenshtein_distance(a: &str, b: &str) -> PyResult<usize> {
    Ok(_damerau(a, b))
}

// Calculates the Hamming distance between two strings.
#[pyfunction]
fn hamming_distance(a: &str, b: &str) -> PyResult<usize> {
    Ok(_hamming(a, b))
}

// Calculates the Jaccard index between two strings.
#[pyfunction]
#[pyo3(signature=(a, b, ngram_size=None))]
fn jaccard_similarity(a: &str, b: &str, ngram_size: Option<usize>) -> PyResult<f64> {
    Ok(_jaccard(a, b, ngram_size))
}

// Calculates the Jaro similarity between two strings.
#[pyfunction]
fn jaro_similarity(a: &str, b: &str) -> PyResult<f64> {
    Ok(_jaro(a, b))
}

// Calculates the Jaro-Winkler similarity between two strings.
#[pyfunction]
#[pyo3(signature=(a, b, long_tolerance=None))]
fn jaro_winkler_similarity(a: &str, b: &str, long_tolerance: Option<bool>) -> PyResult<f64> {
    match long_tolerance {
        Some(true) => Ok(_jaro_winkler_long(a, b)),
        _ => Ok(_jaro_winkler(a, b)),
    }
}

// Calculates the Levenshtein distance between two strings.
#[pyfunction]
fn levenshtein_distance(a: &str, b: &str) -> PyResult<usize> {
    Ok(_lev(a, b))
}

// Calculates the Match Rating Approach code for a string.
#[pyfunction]
fn match_rating_codex(a: &str) -> PyResult<String> {
    // convert to ValueError
    _mr_codex(a).map_err(|e| PyErr::new::<PyValueError, _>(format!("{}", e)))
}

// Calculates the Match Rating Approach comparison for two strings.
#[pyfunction]
fn match_rating_comparison(a: &str, b: &str) -> Option<bool> {
    match _mr_comparison(a, b) {
        Ok(value) => Some(value),
        Err(_) => None,
    }
}

/// Calculates the NYSIIS phonetic encoding of a string.
#[pyfunction]
fn nysiis(a: &str) -> PyResult<String> {
    Ok(_nysiis(a))
}

/// Calculates the phonetic encoding of a string using the Soundex algorithm.
#[pyfunction]
fn soundex(a: &str) -> PyResult<String> {
    Ok(_soundex(a))
}

/// Calculates the phonetic encoding of a string using the Metaphone algorithm.
#[pyfunction]
fn metaphone(a: &str) -> PyResult<String> {
    Ok(_metaphone(a))
}

/// A Python module implemented in Rust.
#[pymodule]
pub fn _rustyfish(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(damerau_levenshtein_distance, m)?)?;
    m.add_function(wrap_pyfunction!(hamming_distance, m)?)?;
    m.add_function(wrap_pyfunction!(jaccard_similarity, m)?)?;
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
