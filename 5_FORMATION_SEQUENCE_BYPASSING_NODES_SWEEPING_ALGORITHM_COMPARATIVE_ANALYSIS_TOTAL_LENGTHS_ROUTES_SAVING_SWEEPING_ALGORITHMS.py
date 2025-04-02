import matplotlib.pyplot as plt
import numpy as np

# Задані параметри з ПР7.pdf
Dmax = 100

# Координати вузлів (з рис. 25 ПР7.pdf)
coordinates = {
    0: (0, 0),
    1: (20, 25),
    4: (15, 10),
    11: (25, -20),
    12: (-5, -10),
    13: (10, 15),
    16: (25, -5),
    17: (-20, -25),
    18: (-25, -20),
    20: (5, 20),
    21: (10, 10),
    22: (4, -5),
    23: (-10, -10),
    24: (-30, -25),
    39: (-10, -15),
    44: (0, 15),
    49: (-15, -15)
}

# Замовлення для кожної програми (потрібно уточнити з опису програм у ПР7.pdf)
# Припускаємо, що базовий вузол 0 не має замовлення
orders_program_1 = {1: 15, 4: 20, 13: 25, 21: 10, 44: 18}
orders_program_2 = {1: 12, 11: 18, 13: 22, 20: 15, 22: 20}
orders_program_3 = {4: 15, 12: 25, 17: 20, 23: 18, 39: 12}
orders_program_4 = {16: 20, 18: 25, 24: 15, 39: 10, 49: 22}

# Функція для розрахунку полярного кута
def polar_angle(coord):
    x, y = coord
    return np.arctan2(y, x)

# Функція для розрахунку відстані між двома точками
def distance(coord1, coord2):
    return np.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

# Функція для формування маршрутів за допомогою sweeping-алгоритму
def form_routes_sweeping(orders, Dmax, coordinates):
    routes = []
    current_route = []
    current_load = 0
    # Сортуємо вузли за полярним кутом відносно базового вузла
    sorted_nodes = sorted(orders.keys(), key=lambda node: polar_angle(coordinates[node]))

    for node in sorted_nodes:
        order = orders[node]
        if current_load + order <= Dmax:
            current_route.append(node)
            current_load += order
        else:
            routes.append(current_route)
            current_route = [node]
            current_load = order
    if current_route:
        routes.append(current_route)
    return routes

# Функція для розрахунку довжини маршруту
def calculate_route_length(route, coordinates):
    length = 0
    if route:
        length += distance(coordinates[0], coordinates[route[0]])
        for i in range(len(route) - 1):
            length += distance(coordinates[route[i]], coordinates[route[i+1]])
        length += distance(coordinates[route[-1]], coordinates[0])
    return length

# Функція для візуалізації простору маршрутів
def visualize_routes(routes, coordinates, program_name):
    plt.figure(figsize=(10, 8))
    plt.scatter(coordinates[0][0], coordinates[0][1], color='red', marker='s', s=100, label='Базовий вузол')
    for node, coord in coordinates.items():
        if node != 0:
            plt.scatter(coord[0], coord[1], color='blue', marker='o', s=50)
            plt.annotate(str(node), (coord[0], coord[1]), textcoords="offset points", xytext=(5,5), ha='center')

    colors = ['green', 'purple', 'orange', 'cyan', 'magenta', 'yellow', 'brown']
    for i, route in enumerate(routes):
        color = colors[i % len(colors)]
        route_nodes = [0] + route + [0]
        x_coords = [coordinates[node][0] for node in route_nodes]
        y_coords = [coordinates[node][1] for node in route_nodes]
        plt.plot(x_coords, y_coords, color=color, linestyle='-', linewidth=1.5, label=f'Маршрут {i+1}')

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f"Простір маршрутів для програми '{program_name}' (Sweeping-алгоритм)")
    plt.legend()
    plt.grid(True)
    plt.show()

# Обробка кожної програми
program_names = ["F1", "F2", "F3", "F4"]
all_program_routes_sweeping = {}
all_program_lengths_sweeping = {}

program_orders_list = [orders_program_1, orders_program_2, orders_program_3, orders_program_4]

for i, program_orders in enumerate(program_orders_list):
    program_name = program_names[i]
    print(f"\n--- Програма {program_name} ---")

    routes_sweeping = form_routes_sweeping(program_orders, Dmax, coordinates)
    all_program_routes_sweeping[program_name] = routes_sweeping

    print("Маршрути (Sweeping-алгоритм):")
    for j, route in enumerate(routes_sweeping):
        print(f"Маршрут {j+1}: {route}")

    route_lengths_sweeping = []
    for route in routes_sweeping:
        length = calculate_route_length(route, coordinates)
        route_lengths_sweeping.append(length)
        print(f"Довжина маршруту {len(route_lengths_sweeping)}: {length:.2f}")

    all_program_lengths_sweeping[program_name] = route_lengths_sweeping

    total_routes = len(routes_sweeping)
    total_length = sum(route_lengths_sweeping)
    print(f"Загальна кількість маршрутів: {total_routes}")
    print(f"Сумарна довжина всіх маршрутів: {total_length:.2f}")

    visualize_routes(routes_sweeping, coordinates, program_name)

# Порівняння з результатами saving-алгоритму (з рис. 26 ПР7.pdf)
all_program_lengths_saving = {
    "F1": 352.7210,
    "F2": 396.8616,
    "F3": 432.2034,
    "F4": 487.2166
}

print("\n--- Порівняння загальних довжин маршрутів ---")
print("| Програма | Saving L | Sweeping L | Різниця |")
print("|----------|----------|------------|---------|")

for program_name in program_names:
    saving_length = all_program_lengths_saving.get(program_name, 0)
    sweeping_length = sum(all_program_lengths_sweeping.get(program_name, []))
    difference = sweeping_length - saving_length
    print(f"| {program_name}    | {saving_length:.2f} | {sweeping_length:.2f} | {difference:.2f} |")

total_saving_length_all = sum(all_program_lengths_saving.values())
total_sweeping_length_all = sum(sum(lengths) for lengths in all_program_lengths_sweeping.values())
total_difference = total_sweeping_length_all - total_saving_length_all
print(f"| Сума     | {total_saving_length_all:.2f} | {total_sweeping_length_all:.2f} | {total_difference:.2f} |")

# Додаткова візуалізація порівняння
program_labels = list(all_program_lengths_sweeping.keys())
saving_totals = [all_program_lengths_saving.get(prog, 0) for prog in program_labels]
sweeping_totals = [sum(all_program_lengths_sweeping.get(prog, [])) for prog in program_labels]

x = np.arange(len(program_labels))
width = 0.35

fig, ax = plt.subplots(figsize=(8, 6))
rects1 = ax.bar(x - width/2, saving_totals, width, label='Saving')
rects2 = ax.bar(x + width/2, sweeping_totals, width, label='Sweeping')

ax.set_ylabel('Загальна довжина маршрутів')
ax.set_title('Порівняння загальної довжини маршрутів за алгоритмами')
ax.set_xticks(x)
ax.set_xticklabels(program_labels)
ax.legend()

fig.tight_layout()
plt.show()
