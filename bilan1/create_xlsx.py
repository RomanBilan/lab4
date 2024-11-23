import pandas as pd
from datetime import datetime
import os

# Функція для розрахунку віку
def calculate_age(birthdate):
    today = datetime.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

# Функція для створення XLSX файлу з категоріями за віком
def create_xlsx_from_csv(csv_filename, xlsx_filename):
    try:
        # Читаємо дані з CSV файлу
        df = pd.read_csv(csv_filename)
        
        # Перевіряємо, чи всі необхідні стовпці присутні
        required_columns = ["Прізвище", "Ім'я", "По батькові", "Дата народження"]
        if not all(col in df.columns for col in required_columns):
            print("Відсутні необхідні стовпці у файлі CSV")
            return
        
        # Конвертуємо дату народження у формат datetime
        df["Дата народження"] = pd.to_datetime(df["Дата народження"], errors='coerce')
        
        # Видаляємо рядки, де дата народження не була коректно прочитана
        df = df.dropna(subset=["Дата народження"])
        
        # Додаємо нову колонку з віком
        df["Вік"] = df["Дата народження"].apply(calculate_age)

        # Створюємо різні категорії за віком
        younger_18 = df[df["Вік"] < 18]
        range_18_45 = df[(df["Вік"] >= 18) & (df["Вік"] <= 45)]
        range_45_70 = df[(df["Вік"] > 45) & (df["Вік"] <= 70)]
        older_70 = df[df["Вік"] > 70]

        # Створюємо Excel файл з п'ятьма аркушами
        with pd.ExcelWriter(xlsx_filename, engine='openpyxl') as writer:
            # Записуємо всі дані на аркуш "all"
            df.to_excel(writer, sheet_name='all', index=False)
            
            # Записуємо дані по категоріям
            younger_18[["Прізвище", "Ім'я", "По батькові", "Дата народження", "Вік"]].to_excel(writer, sheet_name='younger_18', index=False)
            range_18_45[["Прізвище", "Ім'я", "По батькові", "Дата народження", "Вік"]].to_excel(writer, sheet_name='18-45', index=False)
            range_45_70[["Прізвище", "Ім'я", "По батькові", "Дата народження", "Вік"]].to_excel(writer, sheet_name='45-70', index=False)
            older_70[["Прізвище", "Ім'я", "По батькові", "Дата народження", "Вік"]].to_excel(writer, sheet_name='older_70', index=False)
        
        print("Ok, якщо програма завершила свою роботу успішно")
    
    except FileNotFoundError:
        print("Повідомлення про відсутність або проблеми при відкритті файлу CSV.")
    
    except Exception as e:
        print(f"Повідомлення про неможливість створення XLSX файлу: {e}")

if __name__ == "__main__":
    csv_filename = 'employees.csv'
    xlsx_filename = 'employees.xlsx'
    
    if os.path.exists(csv_filename):
        create_xlsx_from_csv(csv_filename, xlsx_filename)
    else:
        print("Повідомлення про відсутність або проблеми при відкритті файлу CSV.")
