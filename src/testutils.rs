#[cfg(test)]
pub mod testutils {
    use csv;

    pub fn test_distance_func(filename: &str, func: fn(&str, &str) -> usize) {
        let mut reader = csv::ReaderBuilder::new()
            .has_headers(false)
            .from_path(filename)
            .unwrap();
        let mut num_tested = 0;
        for result in reader.records() {
            let rec = result.unwrap();
            let expected = rec[2].parse().ok().unwrap();
            println!(
                "comparing {} to {}, expecting {:?}",
                &rec[0], &rec[1], expected
            );
            assert_eq!(func(&rec[0], &rec[1]), expected);
            num_tested += 1;
        }
        assert!(num_tested > 0);
    }

    pub fn test_similarity_func(filename: &str, func: fn(&str, &str) -> f64) {
        let mut reader = csv::ReaderBuilder::new()
            .has_headers(false)
            .from_path(filename)
            .unwrap();
        let mut num_tested = 0;
        for result in reader.records() {
            let rec = result.unwrap();
            let expected: f64 = rec[2].parse().ok().unwrap();
            let output = func(&rec[0], &rec[1]);
            println!(
                "comparing {} to {}, expecting {}, got {}",
                &rec[0], &rec[1], expected, output
            );
            assert!(
                (output - expected).abs() < 0.001,
                "{} !~= {} [{}]",
                output,
                expected,
                output - expected
            );
            num_tested += 1;
        }
        assert!(num_tested > 0);
    }

    pub fn test_str_func(filename: &str, func: fn(&str) -> String) {
        let mut reader = csv::ReaderBuilder::new()
            .has_headers(false)
            .from_path(filename)
            .unwrap();
        let mut num_tested = 0;
        for result in reader.records() {
            let rec = result.unwrap();
            let output = func(&rec[0]);
            println!("testing {}, expecting {}, got {}", &rec[0], &rec[1], output);
            assert_eq!(&rec[1], output);
            num_tested += 1;
        }
        assert!(num_tested > 0);
    }
}
