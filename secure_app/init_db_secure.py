import sqlite3
import bcrypt
import os

base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'database_secure.db')

def init_db_secure():
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

    # Parolayı hashleyelim (A04:2025 Cryptographic Failures Çözümü)
    password = "admin_secure_123".encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)", 
                   ('admin', hashed_password, 'admin'))
    
    conn.commit()
    conn.close()
    print(f"Güvenli veri tabanı oluşturuldu: {db_path}")

if __name__ == "__main__":
    init_db_secure()