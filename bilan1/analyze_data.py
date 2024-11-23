import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# Функція для розрахунку віку
def calculate_age(birthdate):
    today = datetime.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
# Функція для аналізу даних з CSV файлу
def analyze_csv(csv_filename):
    try:
        # Читаємо дані з CSV файлу
        df = pd.read_csv(csv_filename)
        
        # Перевіряємо, чи всі необхідні стовпці присутні
        if "Стать" not in df.columns or "Дата народження" not in df.columns:
            print("Відсутні необхідні стовпці у файлі CSV")
            return
        
        # Конвертуємо дату народження у формат datetime
        df["Дата народження"] = pd.to_datetime(df["Дата народження"], errors='coerce')
        df = df.dropna(subset=["Дата народження"])
        
        # Додаємо нову колонку з віком
        df["Вік"] = df["Дата народження"].apply(calculate_age)

        # Рахуємо кількість співробітників чоловічої і жіночої статі
        gender_count = df["Стать"].value_counts()
        print(f"Кількість чоловіків: {gender_count.get('Чоловік', 0)}")
        print(f"Кількість жінок: {gender_count.get('Жінка', 0)}")

        # Будуємо діаграму за статтю
        gender_count.plot(kind='bar', color=['blue', 'pink'])
        plt.title("Кількість співробітників за статтю")
        plt.xlabel("Стать")
        plt.ylabel("Кількість")
        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.show()

        # Рахуємо кількість співробітників у вікових категоріях
        younger_18 = df[df["Вік"] < 18]
        range_18_45 = df[(df["Вік"] >= 18) & (df["Вік"] <= 45)]
        range_45_70 = df[(df["Вік"] > 45) & (df["Вік"] <= 70)]
        older_70 = df[df["Вік"] > 70]

        age_categories = {
            "Молодше 18": younger_18,
            "18-45": range_18_45,
            "45-70": range_45_70,
            "Старше 70": older_70
        }

        # Виводимо кількість співробітників у кожній віковій категорії
        for category, data in age_categories.items():
            print(f"Кількість співробітників у категорії '{category}': {len(data)}")

        # Будуємо діаграму за віковими категоріями
        age_category_counts = [len(younger_18), len(range_18_45), len(range_45_70), len(older_70)]
        plt.bar(age_categories.keys(), age_category_counts, color=['green', 'orange', 'red', 'purple'])
        plt.title("Кількість співробітників за віковими категоріями")
        plt.xlabel("Категорія")
        plt.ylabel("Кількість")
        plt.tight_layout()
        plt.show()

        # Рахуємо кількість чоловіків і жінок у кожній віковій категорії
        for category, data in age_categories.items():
            gender_category_count = data["Стать"].value_counts()
            print(f"\nКатегорія '{category}':")
            print(f"Чоловіків: {gender_category_count.get('Чоловік', 0)}")
            print(f"Жінок: {gender_category_count.get('Жінка', 0)}")

            # Будуємо діаграму за статтю у вікових категоріях
            gender_category_count.plot(kind='bar', color=['blue', 'pink'])
            plt.title(f"Кількість співробітників за статтю в категорії '{category}'")
            plt.xlabel("Стать")
            plt.ylabel("Кількість")
            plt.xticks(rotation=0)
            plt.tight_layout()
            plt.show()

        print("Ok")

    except FileNotFoundError:
        print("Повідомлення про відсутність або проблеми при відкритті файлу CSV.")
    
    except Exception as e:
        print(f"Сталася помилка: {e}")

if __name__ == "__main__":
    csv_filename = 'employees.csv'
    
    if os.path.exists(csv_filename):
        analyze_csv(csv_filename)
    else:
        print("Повідомлення про відсутність або проблеми при відкритті файлу CSV.")
