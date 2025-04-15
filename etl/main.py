import os
import csv
from datetime import datetime
import psycopg2
from psycopg2 import sql
from typing import Dict, List
from data import schema
from psycopg2.extensions import cursor as Cursor

class ETLProcessor:
    def __init__(self, db_config: Dict, schema: Dict):
        self.db_config = db_config
        self.conn = None
        self.schema = schema

    # ========== EL (Extract-Load) Methods ==========
    def get_current_day(self) -> int:
        """Получает текущий day_number из логов или возвращает 1"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT COALESCE(MAX(day_number), 0) + 1
                FROM logs 
                """)
            return cur.fetchone()[0]

    def extract_csv(self, table_name: str, day_number: int) -> List[Dict]:
        """Читает CSV файл для указанного дня"""
        csv_path = f"data/{table_name}_day{day_number}.csv"
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV not found: {csv_path}")
        
        with open(csv_path, mode='r', encoding='utf-8') as f:
            return list(csv.DictReader(f))

    def load_to_raw(self, table_name: str, data: List[Dict], cur: Cursor) -> int:
        """Очищает и загружает данные в RAW-таблицу"""
        if not data:
            return 0
        columns = list(data[0].keys())
        query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table_name),
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join([sql.Placeholder()] * len(columns))
        )
        cur.execute(sql.SQL("TRUNCATE TABLE {}").format(sql.Identifier(table_name)))
        cur.executemany(query, [tuple(row.values()) for row in data])
        return len(data)

    def log_loading(self, table_name: str, day_number: int, rows_count: int, cur: Cursor):
        """Логирует результат загрузки в таблицу в БД"""
        cur.execute("""
            INSERT INTO logs
            (table_name, day_number, load_date, rows_count) 
            VALUES (%s, %s, %s, %s)
        """, (table_name, day_number, datetime.now(), rows_count))

    def run_el(self):
        """Основной метод EL-процесса"""
        try:
            self.conn = psycopg2.connect(**self.db_config)
            day_number = self.get_current_day()
            for table_name in self.schema["raw_layer"]:
                try:
                    data = self.extract_csv(table_name, day_number)
                    with self.conn.cursor() as cur:
                        rows_count = self.load_to_raw(table_name, data, cur)
                        self.log_loading(table_name, day_number, rows_count, cur)
                        self.conn.commit()
                        print(f"Loaded {rows_count} rows to {table_name}")
                except Exception as e:
                    print(f"Error processing {table_name}: {str(e)}")
                    continue
                    
        finally:
            if self.conn:
                self.conn.close()


if __name__ == "__main__":
    # Конфигурация БД
    DB_CONFIG = {
        "host": os.getenv('DB_HOST'),
        "port": os.getenv('DB_PORT'),
        "dbname": os.getenv('DB_NAME'),
        "user": os.getenv('DB_USER'),
        "password": os.getenv('DB_PASSWORD')
    }

    # Запуск EL-процесса
    etl = ETLProcessor(DB_CONFIG, schema.database_schema)
    
    print("=== Starting EL Process ===")
    etl.run_el()