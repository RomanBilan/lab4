import csv
import random
from faker import Faker

# Налаштовуємо Faker для української локалізації
fake = Faker(locale='uk_UA')

# Словники з по батькові
male_patronymics = [
    "Олексійович", "Сергійович", "Андрійович", "Іванович", "Олегович", 
    "Васильович", "Михайлович", "Григорович", "Петрович", "Федорович",
    "Дмитрович", "Юрійович", "Богданович", "Володимирович", "Макарович",
    "Олександрович", "Степанович", "Вікторович", "Романович", "Павлович"
]

female_patronymics = [
    "Олексіївна", "Сергіївна", "Андріївна", "Іванівна", "Олегівна",
    "Василівна", "Михайлівна", "Григорівна", "Петрівна", "Федорівна",
    "Дмитрівна", "Юріївна", "Богданівна", "Володимирівна", "Макарівна",
    "Олександрівна", "Степанівна", "Вікторівна", "Романівна", "Павлівна"
]

# Визначаємо кількість записів та відсотки
total_records = 2000
female_percentage = 0.4
male_percentage = 0.6
female_records = int(total_records * female_percentage)
male_records = int(total_records * male_percentage)

# Створюємо функцію для генерування записів
def generate_employee_data():
    employees = []
    
    # Генерація чоловіків
    for _ in range(male_records):
        last_name = fake.last_name_male()
        first_name = fake.first_name_male()
        patronymic = random.choice(male_patronymics)
        gender = 'Чоловік'
        birthdate = fake.date_of_birth(minimum_age=16, maximum_age=85)
        position = fake.job()
        city = fake.city()
        address = fake.address()
        phone = fake.phone_number()
        email = fake.email()

        employees.append([last_name, first_name, patronymic, gender, birthdate, position, city, address, phone, email])
    
    # Генерація жінок
    for _ in range(female_records):
        last_name = fake.last_name_female()
        first_name = fake.first_name_female()
        patronymic = random.choice(female_patronymics)
        gender = 'Жінка'
        birthdate = fake.date_of_birth(minimum_age=16, maximum_age=85)
        position = fake.job()
        city = fake.city()
        address = fake.address()
        phone = fake.phone_number()
        email = fake.email()

        employees.append([last_name, first_name, patronymic, gender, birthdate, position, city, address, phone, email])
    
    return employees

# Запис у файл CSV
def save_to_csv(filename, data):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Записуємо заголовки
        writer.writerow(["Прізвище", "Ім'я", "По батькові", "Стать", "Дата народження", "Посада", "Місто проживання", "Адреса проживання", "Телефон", "Email"])
        # Записуємо дані
        writer.writerows(data)

if __name__ == "__main__":
    # Генеруємо дані та записуємо у CSV
    employees_data = generate_employee_data()
    save_to_csv('employees.csv', employees_data)
    print("Дані успішно збережені у файл employees.csv")
