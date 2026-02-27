import sqlite3
import os

# Dosyanın oluşturulacağı dizini sabitleyelim
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'database.db')

def init_db():
    # Artık 'database.db' değil, db_path kullanıyoruz
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            bio TEXT DEFAULT 'Henüz bir bilgi girilmedi.'
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin')")
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES ('victim1', 'pass123', 'user')")
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES ('victim2', 'secret456', 'user')")
    conn.commit()
    conn.close()
    print(f"Veri tabanı şuraya oluşturuldu: {db_path}")

if __name__ == "__main__":
    init_db()