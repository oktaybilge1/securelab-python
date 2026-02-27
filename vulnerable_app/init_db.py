import sqlite3
import os

# Set the directory where the database file will be created / Dosyanın oluşturulacağı dizini sabitleyelim
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'database.db')

def init_db():
    # Establish database connection / Veri tabanı bağlantısı
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table / Kullanıcılar tablosunu oluştur
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            bio TEXT DEFAULT 'No biography provided.'
        )
    ''')
    
    # Vulnerable approach: Storing passwords in plain text (A04: Cryptographic Failures)
    # Zafiyetli yaklaşım: Parolaları düz metin olarak saklama (A04: Cryptographic Failures)
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin')")
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES ('victim1', 'pass123', 'user')")
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES ('victim2', 'secret456', 'user')")
    
    conn.commit()
    conn.close()
    print(f"Success: Vulnerable database created at {db_path}")

if __name__ == "__main__":
    init_db()