import sqlite3

DB_PATH = 'channels.db'

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS channels (
                guild_id TEXT PRIMARY KEY,
                channel_id INTEGER
            )
        ''')
        conn.commit()

def save_channel(guild_id, channel_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO channels (guild_id, channel_id)
            VALUES (?, ?)
        ''', (guild_id, channel_id))
        conn.commit()

def get_channel(guild_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT channel_id FROM channels WHERE guild_id = ?', (guild_id,))
        result = cursor.fetchone()
        return result[0] if result else None

# Panggil init_db() saat memulai aplikasi untuk memastikan tabel ada
init_db()