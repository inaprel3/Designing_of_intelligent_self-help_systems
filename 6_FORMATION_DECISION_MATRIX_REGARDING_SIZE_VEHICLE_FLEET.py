import numpy as np
import matplotlib.pyplot as plt

# Альтернативи та критерії
alternatives = [f"E{i}" for i in range(1, 11)]
criteria = ["F1", "F2", "F3", "F4", "MM", "BL", "S", "HW", "HL", "G", "P", "Z"]

# Генеруємо випадкові значення F1-F4
np.random.seed(42)  # Для відтворюваності
F_values = np.random.randint(1000, 10000, size=(10, 4))

# Матриця рішень (F1-F4 + 7 критеріїв + Z)
decision_matrix = np.zeros((10, 12))

for i in range(10):
    F1, F2, F3, F4 = F_values[i]
    decision_matrix[i, :4] = [F1, F2, F3, F4]  # Записуємо F1-F4

    # Розрахунок критеріїв (прикладні формули, можна змінити)
    decision_matrix[i, 4] = F1 + F2  # MM
    decision_matrix[i, 5] = F3 - F4  # BL
    decision_matrix[i, 6] = F1 * 1.1  # S
    decision_matrix[i, 7] = F2 * 0.9  # HW
    decision_matrix[i, 8] = (F3 + F4) / 2  # HL
    decision_matrix[i, 9] = np.sqrt(F1**2 + F2**2)  # G
    decision_matrix[i, 10] = max(F1, F2, F3, F4)  # P

    # Розрахунок Z (сума всіх критеріїв, можна змінити формулу)
    decision_matrix[i, 11] = np.sum(decision_matrix[i, 4:11])

# Визначаємо найкращу альтернативу (мінімальний Z, якщо критерії на мінімізацію)
best_index = np.argmin(decision_matrix[:, 11])  # Мінімальне значення Z
best_alternative = alternatives[best_index]

# Візуалізація таблиці
fig, ax = plt.subplots(figsize=(14, 8))

cell_text = [[f"{x:.2f}" for x in row] for row in decision_matrix]

# Додаємо мітку найкращої альтернативи
row_labels = [alt + (" *" if alt == best_alternative else "") for alt in alternatives]

table = ax.table(cellText=cell_text,
                 rowLabels=row_labels,
                 colLabels=criteria,
                 cellLoc='center',
                 loc='center')

table.auto_set_font_size(False)
table.set_fontsize(10)
ax.axis('off')

plt.title("Матриця рішень з критеріями та вибором оптимальної альтернативи")
plt.tight_layout()
plt.show()

# Виведення найкращої альтернативи
print(f"Найкраща альтернатива: {best_alternative} (мінімальне Z = {decision_matrix[best_index, 11]:.2f})")
