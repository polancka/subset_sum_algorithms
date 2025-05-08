import random
import time
import os
from typing import List, Tuple
from tabulate import tabulate
from subset_sum import subset_sum_bellman, subset_sum_bfs, subset_sum_bfs_pruned, subset_sum_approx, subset_sum_fptas
from generate_instances import generate_hard_dyn_instance, generate_hard_bfs_instance, generate_bad_greedy_instance, generate_bad_fptas_instance 

# Read the input from a file
def read_input(filename):
    with open(filename, 'r') as f:
        lines = list(map(str.strip, f.readlines()))
        n = int(lines[0])
        k = int(lines[1])
        a = list(map(int, lines[2:2+n]))
        return n, k, a

def evaluate_algorithms(n: int, k: int, a: List[int], epsilon: float = 0.4) -> List[Tuple[str, int, float]]:
    results = []

    start = time.time()
    val = subset_sum_bellman(n, k, a)
    results.append(("DYN", val, time.time() - start))

    start = time.time()
    val = subset_sum_bfs_pruned(n, k, a)
    results.append(("EXH", val, time.time() - start))

    start = time.time()
    val = subset_sum_approx(n, k, a)
    results.append(("GREEDY", val, time.time() - start))

    start = time.time()
    val = subset_sum_fptas(n, k, a, epsilon)
    results.append((f"FPTAS (ε={epsilon})", val, time.time() - start))

    return results

def run_instances():
    instances = {
        "Hard for DYN": generate_hard_dyn_instance(),
        "Hard for BFS": generate_hard_bfs_instance(),
        "Bad for GREEDY": generate_bad_greedy_instance(),
        "Bad for FPTAS": generate_bad_fptas_instance()
    }

    all_results = []

    for name, (n, k, a) in instances.items():
        results = evaluate_algorithms(n, k, a)
        for alg, val, t in results:
            all_results.append([name, alg, val, f"{t:.6f}s"])

    # --- Print table ---

    print(tabulate(all_results, headers=["Instance", "Algorithm", "Subset Sum ≤ k", "Time"]))

if __name__ == "__main__":
    #run_instances()
    algorithm_map = {
        "hard_for_dyn": subset_sum_bellman,
        "hard_for_bfs": subset_sum_bfs_pruned,
        "bad_for_greedy": subset_sum_approx,
        "bad_for_fptas": lambda n, k, a: subset_sum_fptas(n, k, a, epsilon=0.4)
    }

    # --- Timing and result table ---

    results = []

    for instance_type, algorithm in algorithm_map.items():
        for i in range(1, 6):
            filename = os.path.join("instances", f"{instance_type}_{i}.txt")
            if not os.path.exists(filename):
                continue
            n, k, a = read_input(filename)
            start = time.time()
            result = algorithm(n, k, a)
            duration = time.time() - start
            results.append([
                instance_type,
                filename,
                result,
                f"{duration:.6f}s"
            ])

    # --- Output the table ---

    print(tabulate(results, headers=["Instance Type", "Filename", "Subset Sum", "Time"]))