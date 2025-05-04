import random 
from typing import List, Tuple

def generate_hard_dyn_instance(n=100, max_val=100, k=10000) -> Tuple[int, int, List[int]]:
    a = [random.randint(1, max_val) for _ in range(n)]
    return n, k, a

def generate_hard_bfs_instance(n=30, k=100) -> Tuple[int, int, List[int]]:
    a = [random.randint(k // 4, k // 2) for _ in range(n)]
    return n, k, a

def generate_bad_greedy_instance(M=100) -> Tuple[int, int, List[int]]:
    a = [M + 1, M, M]
    k = 2 * M
    return 3, k, a

def generate_bad_fptas_instance(n=20, base=100) -> Tuple[int, int, List[int]]:
    a = [base + random.randint(-5, 5) for _ in range(n)]
    k = int(0.5 * sum(a))
    return n, k, a