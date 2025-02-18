import micropip
await micropip.install(["numpy", "matplotlib"])

import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

# Координати складу
warehouse = (0, 0)

# Координати вузлів
nodes = {
    1: (2, 3),
    2: (5, 1),
    3: (7, 4),
    4: (6, 8),
    5: (3, 7),
    6: (8, 2)
}

all_nodes = {0: warehouse, **nodes}
node_ids = list(all_nodes.keys())

def distance(a, b):
    return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

# 1 Симетрична матриця відстаней
n = len(all_nodes)
distance_matrix = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        if i != j:
            distance_matrix[i, j] = distance(all_nodes[node_ids[i]], all_nodes[node_ids[j]])

print("\nСиметрична матриця відстаней:")
print(distance_matrix)

# 2 Saving-таблиця
saving_table = {}
for (i, j) in combinations(range(1, n), 2):
    s = distance_matrix[0, i] + distance_matrix[0, j] - distance_matrix[i, j]
    saving_table[(i, j)] = s

sorted_savings = dict(sorted(saving_table.items(), key=lambda item: item[1], reverse=True))

print("\nSaving-таблиця (пари вузлів та їх savings):")
for pair, saving in sorted_savings.items():
    print(f"{pair}: {saving:.2f}")

# 3 Побудова маршруту
parents = {i: i for i in range(1, n)}
chains = {i: [i] for i in range(1, n)}

def find_parent(node):
    while parents[node] != node:
        node = parents[node]
    return node

def union(i, j):
    pi, pj = find_parent(i), find_parent(j)
    if pi != pj:
        parents[pj] = pi
        chains[pi].extend(chains[pj])
        chains.pop(pj)

for (i, j) in sorted_savings.keys():
    if find_parent(i) != find_parent(j) and len(chains[find_parent(i)]) < n - 1:
        union(i, j)

final_route = [0] + chains[find_parent(1)] + [0]

print("\nГамільтонів цикл (маршрут):")
print(" -> ".join(map(str, [node_ids[i] for i in final_route])))

# 4 Візуалізація маршруту
plt.figure(figsize=(7, 7))
plt.scatter(*zip(*all_nodes.values()), c='blue', marker='o', label="Вузли")
plt.scatter(*warehouse, c='red', marker='s', label="Склад")

for i, (x, y) in all_nodes.items():
    plt.text(x, y, f'{i}', fontsize=9, ha='right')

for i in range(len(final_route) - 1):
    x1, y1 = all_nodes[node_ids[final_route[i]]]
    x2, y2 = all_nodes[node_ids[final_route[i+1]]]
    plt.plot([x1, x2], [y1, y2], 'k-')

plt.title("Гамільтонів цикл (Saving-алгоритм)")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.grid(True)
plt.show()
