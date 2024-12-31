import sqlite3

def initialize_database():
    conn = sqlite3.connect('command_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS command_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    command TEXT,
                    timestamp TEXT
                )''')
    conn.commit()
    conn.close()

def save_command(user_id, command):
    conn = sqlite3.connect('command_history.db')
    c = conn.cursor()
    c.execute('INSERT INTO command_history (user_id, command, timestamp) VALUES (?, ?, datetime("now"))',
              (user_id, command))
    conn.commit()
    conn.close()