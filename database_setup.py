import sqlite3

DATABASE = 'vulnerable.db'

def init_db():
    connection = sqlite3.connect(DATABASE)
    with connection:
        cursor = connection.cursor()
        with open('schema.sql', 'r') as f:
            cursor.executescript(f.read())
    print("Database initialized successfully")

if __name__ == '__main__':
    init_db()
