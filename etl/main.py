import os
import psycopg2
from psycopg2 import sql

# Подключение к БД
conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)

# Создание курсора
cur = conn.cursor()
print("start")
# Вставка данных
try:
    cur.execute("""
        INSERT INTO orders (order_id, order_date, customer_id, load_date)
        VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
    """, ("111", "01.01.2025", "123"))
    
    conn.commit()
    print("Запись успешно добавлена!")
except Exception as e:
    conn.rollback()
    print(f"Ошибка: {e}")
finally:
    cur.close()
    conn.close()
print("Finish")
