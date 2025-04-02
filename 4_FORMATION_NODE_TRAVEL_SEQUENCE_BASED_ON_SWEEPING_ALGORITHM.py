import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Вихідні дані: координати вузлів
nodes = {
    1: (10, 30),
    2: (40, 10),
    3: (50, 60),
    4: (20, 40),
    5: (60, 20),
    6: (70, 50),
}

# Визначаємо базовий вузол (центр маси)
base_x = sum(x for x, y in nodes.values()) / len(nodes)
base_y = sum(y for x, y in nodes.values()) / len(nodes)

# Обчислюємо нові координати, кути та полярні радіуси
sweeping_table = []
new_nodes = {}  # Для збереження нових координат
for node, (x, y) in nodes.items():
    new_x, new_y = x - base_x, y - base_y
    angle = np.arctan2(new_y, new_x)  # Кут у радіанах
    radius = np.sqrt(new_x**2 + new_y**2)  # Полярний радіус
    sweeping_table.append((node, new_x, new_y, np.degrees(angle), radius))
    new_nodes[node] = (new_x, new_y)

# Створюємо DataFrame для таблиці
columns = ["Вузол", "Новий X", "Новий Y", "Кут (градуси)", "Полярний радіус"]
df = pd.DataFrame(sweeping_table, columns=columns)

# Сортуємо за кутом (з урахуванням радіусу при рівних кутах)
df.sort_values(by=["Кут (градуси)", "Полярний радіус"], ascending=[True, False], inplace=True)

# Формуємо послідовність обходу
path = df["Вузол"].tolist()
path.append(path[0])  # Замикання циклу

# Виводимо sweeping-таблицю
print("Sweeping-таблиця:")
print(df.to_string(index=False))

# Створення першої картинки "Нові координати вузлів"
plt.figure(figsize=(8, 6))
for node, (new_x, new_y) in new_nodes.items():
    plt.scatter(new_x, new_y, color='blue')
    plt.text(new_x + 1, new_y + 1, str(node), fontsize=12, color='red')

plt.scatter(0, 0, color='green', s=100, label="Base Node")  # Центр маси
plt.xlabel("Новий X")
plt.ylabel("Новий Y")
plt.title("Нові координати вузлів")
plt.legend()
plt.grid()
plt.show()

# Візуалізація Гамільтонового циклу
plt.figure(figsize=(8, 6))
for i in range(len(path) - 1):
    x1, y1 = nodes[path[i]]
    x2, y2 = nodes[path[i + 1]]
    plt.plot([x1, x2], [y1, y2], 'bo-')  # З'єднання точок

# Позначаємо вузли
for node, (x, y) in nodes.items():
    plt.text(x + 1, y + 1, str(node), fontsize=12, color='red')

# Відображаємо базову точку
plt.scatter(base_x, base_y, color='green', s=100, label="Base Node")

plt.xlabel("X")
plt.ylabel("Y")
plt.title("Гамільтонів цикл за sweeping-алгоритмом")
plt.legend()
plt.grid()
plt.show()
