mod common;
mod hamming;
mod jaccard;
mod jaro;
mod levenshtein;
mod match_rating;
mod metaphone;
mod nysiis;
mod soundex;
mod testutils;

pub use hamming::{hamming_distance, vec_hamming_distance};
pub use jaccard::jaccard_similarity;
pub use jaro::{
    jaro_similarity, jaro_winkler_similarity, jaro_winkler_similarity_longtol, vec_jaro_similarity,
    vec_jaro_winkler_similarity, vec_jaro_winkler_similarity_longtol,
};
pub use levenshtein::{
    damerau_levenshtein_distance, levenshtein_distance, vec_damerau_levenshtein_distance,
    vec_levenshtein_distance,
};
pub use match_rating::{match_rating_codex, match_rating_comparison};
pub use metaphone::metaphone;
pub use nysiis::nysiis;
pub use soundex::soundex;

#[cfg(feature = "python")]
mod rustyfish;
#[cfg(feature = "python")]
pub use rustyfish::_rustyfish;
