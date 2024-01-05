# database.py
import sqlite3

class DBHelper:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schedules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                schedule_time TEXT
            )
        ''')
        self.conn.commit()

    def add_schedule(self, username, schedule_time):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO schedules (username, schedule_time) VALUES (?, ?)", (username, schedule_time))
        self.conn.commit()

    def get_all_users(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()

    def get_all_schedules(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM schedules")
        return cursor.fetchall()
