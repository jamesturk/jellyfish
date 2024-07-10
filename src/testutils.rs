#[cfg(test)]
pub mod testutils {
    use csv;
    use num_traits::{Float, FromPrimitive};

    fn test_generic_func<T, F>(filename: &str, func: F)
    where
        F: Fn(&str, &str, Option<usize>) -> T, // Signature for functions with ngram_size
        T: PartialEq + std::fmt::Debug + std::str::FromStr + Float + FromPrimitive,
        <T as std::str::FromStr>::Err: std::fmt::Debug,
    {
        let mut reader = csv::ReaderBuilder::new()
            .has_headers(false)
            .from_path(filename)
            .unwrap();
        let mut num_tested = 0;
        for result in reader.records() {
            let rec = result.unwrap();
            let input1 = &rec[0];
            let input2 = &rec[1];
            let ngram_size = rec.get(3).and_then(|s| s.parse().ok());

            let expected: T = rec[2].parse().expect("Failed to parse expected value");
            let output = func(input1, input2, ngram_size);

            let abs_diff = (output.to_f64().unwrap() - expected.to_f64().unwrap()).abs();
            assert!(
                abs_diff < 0.001,
                "comparing {} to {} (ngram_size: {:?}), expected {:?}, got {:?} (diff {:?})",
                input1,
                input2,
                ngram_size,
                expected,
                output,
                abs_diff
            );

            num_tested += 1;
        }
        assert!(num_tested > 0);
    }

    pub fn test_distance_func(filename: &str, func: fn(&str, &str) -> usize) {
        let mut reader = csv::ReaderBuilder::new()
            .has_headers(false)
            .from_path(filename)
            .unwrap();
        let mut num_tested = 0;
        for result in reader.records() {
            let rec = result.unwrap();
            let input1 = &rec[0];
            let input2 = &rec[1];
            let expected: usize = rec[2].parse().expect("Failed to parse expected value");
            let output = func(input1, input2);

            println!(
                "comparing {} to {}, expecting {:?}, got {:?}",
                input1, input2, expected, output
            );
            assert_eq!(output, expected);
            num_tested += 1;
        }
        assert!(num_tested > 0);
    }

    // For functions with two string arguments
    pub fn test_similarity_func_two_args(filename: &str, func: fn(&str, &str) -> f64) {
        test_generic_func::<f64, _>(filename, |a, b, _| func(a, b));
    }

    // For functions with three arguments (including the optional usize)
    pub fn test_similarity_func_three_args(filename: &str, func: fn(&str, &str, Option<usize>) -> f64) {
        test_generic_func::<f64, _>(filename, |a, b, n| func(a, b, n));
    }

    pub fn test_str_func(filename: &str, func: fn(&str) -> String) {
        let mut reader = csv::ReaderBuilder::new()
            .has_headers(false)
            .from_path(filename)
            .unwrap();
        let mut num_tested = 0;
        for result in reader.records() {
            let rec = result.unwrap();
            let input1 = &rec[0];
            let expected = rec[1].to_string();

            let output = func(input1);

            println!(
                "comparing {}, expecting {:?}, got {:?}",
                input1, expected, output
            );
            assert_eq!(output, expected);
            num_tested += 1;
        }
        assert!(num_tested > 0);
    }
}
