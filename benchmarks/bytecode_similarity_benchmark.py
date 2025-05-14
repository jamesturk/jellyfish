#!/usr/bin/env python3
import time
import csv
import jellyfish
import sys
from pathlib import Path

# Load bytecode pairs from CSV file
def load_bytecode_pairs(csv_path):
    first_bytecode = None
    other_bytecodes = []
    
    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        # Skip header row
        next(reader)
        
        for row in reader:
            if len(row) >= 2:
                if first_bytecode is None:
                    first_bytecode = row[0]
                other_bytecodes.append(row[1])
    
    return first_bytecode, other_bytecodes

# Run benchmark using standard Jaro-Winkler
def benchmark_standard(first_bytecode, other_bytecodes):
    start_time = time.time()
    results = []

    for bytecode in other_bytecodes:
        similarity = jellyfish.jaro_winkler_similarity(first_bytecode, bytecode)
        results.append(similarity)

    end_time = time.time()
    return results, end_time - start_time

# Run benchmark using quick Jaro-Winkler with threshold
def benchmark_quick(first_bytecode, other_bytecodes, threshold):
    start_time = time.time()
    results = []

    for bytecode in other_bytecodes:
        similarity = jellyfish.jaro_winkler_similarity_quick(first_bytecode, bytecode, threshold)
        results.append(similarity)

    end_time = time.time()
    return results, end_time - start_time

def main():
    # Path to CSV file with bytecode pairs (using local path)
    csv_path = Path("benchmarks/bytecode_pairs.csv")

    # Ensure benchmark directory exists
    csv_path.parent.mkdir(exist_ok=True)

    print("Loading bytecode pairs from CSV...")
    first_bytecode, other_bytecodes = load_bytecode_pairs(csv_path)
    print(f"Loaded {len(other_bytecodes)} bytecode pairs")

    # Run standard benchmark
    print("\nRunning standard Jaro-Winkler benchmark...")
    standard_results, standard_time = benchmark_standard(first_bytecode, other_bytecodes)
    print(f"Standard Jaro-Winkler completed in {standard_time:.4f} seconds")

    # Run quick benchmark with threshold 0.8
    threshold = 0.8
    print(f"\nRunning quick Jaro-Winkler benchmark with threshold {threshold}...")
    quick_results, quick_time = benchmark_quick(first_bytecode, other_bytecodes, threshold)
    print(f"Quick Jaro-Winkler completed in {quick_time:.4f} seconds")

    # Print speedup
    speedup = standard_time / quick_time if quick_time > 0 else float('inf')
    print(f"\nSpeedup: {speedup:.2f}x")

    # Count how many results were filtered by the threshold
    filtered_count = sum(1 for r in quick_results if r == 0.0)
    print(f"Number of comparisons filtered by threshold: {filtered_count} out of {len(quick_results)}")

    # Print some sample results for comparison
    print("\nSample results (first 5):")
    for i in range(min(5, len(standard_results))):
        print(f"  Pair {i+1}: Standard={standard_results[i]:.4f}, Quick={quick_results[i]:.4f}")

if __name__ == "__main__":
    main()
