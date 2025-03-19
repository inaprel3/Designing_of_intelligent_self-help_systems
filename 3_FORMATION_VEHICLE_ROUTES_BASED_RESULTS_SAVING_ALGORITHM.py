import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

# Координати вузлів (міст)
nodes = {
    'Depot': (0, 0),
    'A': (2, 4),
    'B': (5, 1),
    'C': (6, 7),
    'D': (8, 3),
    'E': (1, 6),
    'F': (3, 8),
    'G': (7, 5),
    'H': (4, 5)
}

# Чотири різні програми замовлень
order_programs = [
    {'A': 4, 'B': 6, 'C': 3, 'D': 5, 'E': 2, 'F': 7, 'G': 4, 'H': 3},
    {'A': 5, 'B': 7, 'C': 4, 'D': 6, 'E': 3, 'F': 6, 'G': 5, 'H': 4},
    {'A': 6, 'B': 5, 'C': 7, 'D': 4, 'E': 5, 'F': 8, 'G': 6, 'H': 3},
    {'A': 3, 'B': 4, 'C': 5, 'D': 7, 'E': 6, 'F': 5, 'G': 8, 'H': 6}
]

Dmax = 15  # Максимальна вантажопідйомність одного транспорту

# Функція обчислення відстані
def distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Колірні палітри для кожної програми
color_palettes = [
    ['skyblue', 'blue', 'green', 'lightgreen'],
    ['orange', 'red', 'lightgreen', 'brown'],
    ['purple', 'pink', 'darkred', 'blue'],
    ['darkblue', 'darkgreen', 'yellow', 'cyan']
]

# Побудова маршрутів для кожної програми
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes = axes.flatten()

for program_idx, (orders, colors) in enumerate(zip(order_programs, color_palettes)):
    savings = []
    
    # Формуємо список savings для поточної програми
    for i in orders:
        for j in orders:
            if i != j:
                saving = distance(nodes['Depot'], nodes[i]) + distance(nodes['Depot'], nodes[j]) - distance(nodes[i], nodes[j])
                savings.append((saving, i, j))

    # Сортуємо saving за спаданням
    savings.sort(reverse=True, key=lambda x: x[0])

    # Формування маршрутів
    routes = []
    used_nodes = set()
    
    for _, i, j in savings:
        if i in used_nodes or j in used_nodes:
            continue
        if orders[i] + orders[j] <= Dmax:
            routes.append(['Depot', i, j, 'Depot'])
            used_nodes.update([i, j])

    # Додаємо окремі маршрути для тих, хто не увійшов
    for node in orders:
        if node not in used_nodes:
            routes.append(['Depot', node, 'Depot'])

    # Обчислення довжин маршрутів
    route_lengths = []
    for route in routes:
        length = sum(distance(nodes[route[i]], nodes[route[i+1]]) for i in range(len(route)-1))
        route_lengths.append(length)

    # Загальна довжина маршрутів
    total_length = sum(route_lengths)

    # Вивід результатів у консоль
    print(f"\nПрограма {program_idx + 1}:")
    print(f"Загальна кількість маршрутів: {len(routes)}")
    for i, route in enumerate(routes):
        print(f"Маршрут {i+1}: {' -> '.join(route)}, Довжина: {route_lengths[i]:.2f}")
    print(f"Сумарна довжина всіх маршрутів: {total_length:.2f}")

    # Візуалізація маршрутів
    G = nx.Graph()
    for node, (x, y) in nodes.items():
        G.add_node(node, pos=(x, y))

    ax = axes[program_idx]

    for idx, (route, color) in enumerate(zip(routes, colors)):
        edges = [(route[i], route[i+1]) for i in range(len(route)-1)]
        nx.draw_networkx_edges(G, pos=nx.get_node_attributes(G, 'pos'), edgelist=edges, width=2, edge_color=color, ax=ax)
        nx.draw_networkx_nodes(G, pos=nx.get_node_attributes(G, 'pos'), node_size=700, node_color='lightgray', ax=ax)
        nx.draw_networkx_labels(G, pos=nx.get_node_attributes(G, 'pos'), ax=ax)

    ax.set_title(f"Програма {program_idx + 1}")

plt.tight_layout()
plt.show()
