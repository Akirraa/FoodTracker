import psycopg2
import csv

# Database connection
conn = psycopg2.connect(
    host="localhost",
    database="FoodTrackerDB",
    user="postgres",
    password="azerty"
)
cursor = conn.cursor()

# Path to your CSV file
csv_file_path = 'data_conversion\cleaned_food.csv'

# Open and insert data
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        cursor.execute('''
            INSERT INTO food (
                name, calories, protein, carbs, fats, fiber, sugar, water, sodium,
                calcium, iron, potassium, cholesterol
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            row['Name'],
            float(row['Calories']),
            float(row['Protein']),
            float(row['Carbs']),
            float(row['Fat']),
            float(row['Fiber']),
            float(row['Sugar']),
            float(row['Water']),
            float(row['Sodium']),
            float(row['Calcium']),
            float(row['Iron']),
            float(row['Potassium']),
            float(row['Cholesterol'])
        ))

conn.commit()
cursor.close()
conn.close()
