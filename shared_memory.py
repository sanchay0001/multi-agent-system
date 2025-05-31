 # memory/shared_memory.py

import sqlite3
import time

class SharedMemory:
    def __init__(self, db_path="shared_memory.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            source TEXT,
            format TEXT,
            intent TEXT,
            sender TEXT,
            extracted_values TEXT,
            thread_id TEXT
        );
        """
        self.conn.execute(query)
        self.conn.commit()

    def log(self, source, format_, intent, sender=None, extracted_values=None, thread_id=None):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        query = """
        INSERT INTO memory (timestamp, source, format, intent, sender, extracted_values, thread_id)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        self.conn.execute(query, (timestamp, source, format_, intent, sender, str(extracted_values), thread_id))
        self.conn.commit()

    def fetch_all(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM memory;")
        return cursor.fetchall()

    def close(self):
        self.conn.close()

