import time
import os
from collections import deque
from tabulate import tabulate


def subset_sum_bellman(n, k, a):
    dp = [[0] * (k + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(k + 1):
            if j >= a[i - 1]:
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - a[i - 1]] + a[i - 1])
            else:
                dp[i][j] = dp[i - 1][j]

    return dp[n][k]

# BFS Extensive Search approach
def subset_sum_bfs(n, k, a):
    queue = deque([0])
    visited = set()
    while queue:
        current = queue.popleft()
        if current == k:
            return True
        for num in a:
            new_sum = current + num
            if new_sum <= k and new_sum not in visited:
                visited.add(new_sum)
                queue.append(new_sum)
    return False

#BFS with "prunning"
def subset_sum_bfs_pruned(n, k, a):
    current = set([0])
    for num in a:
        next_layer = set()
        for val in current:
            new_val = val + num
            if new_val <= k:
                next_layer.add(new_val)
        current |= next_layer
    return max(current)

#2-APX greedy algortihm 
def subset_sum_approx(n, k, a):
    a_sorted = sorted(a, reverse=True)
    total = 0
    for num in a_sorted:
        if total + num <= k:
            total += num
    return total

#FPTAS
def trim(L, delta):
    trimmed = [L[0]]
    last = L[0]
    for x in L:
        if x > last * (1 + delta):
            trimmed.append(x)
            last = x
    return trimmed

def subset_sum_fptas(n, k, a, epsilon):
    delta = epsilon / (2 * n)
    L = [0]

    for num in a:
        # Generate new candidate list
        new_L = sorted(set(L + [x + num for x in L]))
        # Filter out values > k
        new_L = [x for x in new_L if x <= k]
        # Apply TRIM to reduce list size
        L = trim(new_L, delta)

    return max(L)


# Run test cases
def run_tests():
    test_folder = "test"
    for i in range(1, 6):
        filepath = os.path.join(test_folder, f"SS{i}.txt")
        n, k, a = read_input(filepath)

        print(f"\nTest case {i}: n={n}, k={k}")
        
        results = []

        #DYNAMIC
        start = time.time()
        sum_bellman = subset_sum_bellman(n, k, a)
        end = time.time()
        results.append(["Bellman DP", sum_bellman, f"{end - start:.6f}s"])
        
        #BFS
        start = time.time()
        sum_bfs = subset_sum_bfs_pruned(n, k, a)
        end = time.time()
        results.append(["BFS Pruned", sum_bfs, f"{end - start:.6f}s"])

        #2-APX greedy
        start = time.time()
        sum_approx = subset_sum_approx(n, k, a)
        end = time.time()
        results.append(["2-Approx Greedy", sum_approx, f"{end - start:.6f}s"])
        
        # FPTAS
        epsilons = [0.1, 0.2, 0.4]

        for epsilon in epsilons:
            # FPTAS
            start = time.time()
            fptas_sum = subset_sum_fptas(n, k, a, epsilon)
            end = time.time()
            results.append([f"FPTAS (ε={epsilon})", fptas_sum, f"{end - start:.6f}s"])

        print("\nAlgorithm Comparison:")
        print(tabulate(results, headers=["Algorithm", "Subset Sum ≤ k", "Time"]))

if __name__ == "__main__":
    run_tests()