import random 
import os
from typing import List, Tuple

def generate_hard_dyn_instance(n, k):
    # Generate values and ensure a subset sums to k
    a = []
    total = 0
    for _ in range(n - 1):
        val = random.randint(1, 10)
        a.append(val)
        total += val

    # Add one last element to make exact sum = k (if possible)
    if total < k:
        a.append(k - total)
    else:
        a.append(1)  # fallback: will not exactly reach k

    random.shuffle(a)
    return len(a), k, a

def generate_hard_bfs_instance(n, k) -> Tuple[int, int, List[int]]:
    a = []
    current_sum = 0

    # Generate first n-1 elements randomly from a large range
    for _ in range(n - 1):
        val = random.randint(k // 4, k // 2)
        a.append(val)
        current_sum += val

    # Adjust last element to make total sum = k (if possible)
    if current_sum < k:
        a.append(k - current_sum)
    else:
        # fallback if we overshot
        a.append(random.randint(1, k // 4))

    random.shuffle(a)
    return len(a), k, a

def generate_bad_greedy_instance(M=1000) -> Tuple[int, int, List[int]]:
    a = [M + 1, M, M]
    k = 2 * M
    return 3, k, a

def generate_bad_fptas_instance(n=200, base=100) -> Tuple[int, int, List[int]]:
    a = [base + random.randint(-5, 5) for _ in range(n)]
    k = int(0.5 * sum(a))
    return n, k, a


def save_instance(name: str, index: int, n: int, k: int, a: list[int]):
    os.makedirs("bfs_instances", exist_ok=True)
    filename = os.path.join("bfs_instances", f"{name}_{index}.txt")
    with open(filename, "w") as f:
        f.write(f"{n}\n{k}\n")
        f.writelines([f"{num}\n" for num in a])

""" if __name__ == "__main__":
    generators = {
        "hard_for_dyn": generate_hard_dyn_instance,
        "hard_for_bfs": generate_hard_bfs_instance,
        "bad_for_greedy": generate_bad_greedy_instance,
        "bad_for_fptas": generate_bad_fptas_instance
    }

    for name, generator in generators.items():
        for i in range(1, 6):
            n, k, a = generator()
            save_instance(name, i, n, k, a) """
ns = [100,50,500,40,1000]
ks = [100,1000,10000,100000,1000000] 

for i in range (0,5):
    print(i)
    n,k,a = generate_hard_bfs_instance(1000, ks[i])
    save_instance("BFS_TEST", i, n, k, a)