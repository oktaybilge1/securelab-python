import sqlite3
import bcrypt
import os

base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'database_secure.db')

def init_db_secure():
    # Database connection / Veri tabanı bağlantısı
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table with secure schema / Güvenli şema ile kullanıcılar tablosunu oluştur
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            bio TEXT DEFAULT 'No biography provided.'
        )
    ''')

    # Hash the password (Solution for A04: Cryptographic Failures) 
    # Parolayı hashleyelim (A04: Cryptographic Failures Çözümü)
    password = "admin_secure_123".encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

    # Insert admin user if not exists / Admin kullanıcısını eğer yoksa ekle
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)", 
                   ('admin', hashed_password, 'admin'))
    
    conn.commit()
    conn.close()
    print(f"Success: Secure database created at {db_path}")

if __name__ == "__main__":
    init_db_secure()