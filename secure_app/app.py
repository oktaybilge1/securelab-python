from flask import Flask, request, render_template, redirect, url_for, session
from markupsafe import escape
import sqlite3, bcrypt, os

app = Flask(__name__)
app.secret_key = os.urandom(24) # A04: Güçlü session key
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'database_secure.db')

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password'].encode('utf-8')
        conn = get_db_connection()
        # FIX A05: Parametreli sorgu ile SQLi engellendi
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        
        # FIX A04: Bcrypt ile şifre doğrulaması
        if user and bcrypt.checkpw(password_candidate, user['password'].encode('utf-8')):
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['username'] = user['username']
            return redirect(url_for('profile', user_id=user['id']))
        return "Hatalı kimlik bilgileri!", 401
    return render_template('login.html')

@app.route('/profile/<int:user_id>', methods=['GET'])
def profile(user_id):
    # FIX A01: Yetki Kontrolü (IDOR Engellendi)
    if 'user_id' not in session or (session['user_id'] != user_id and session['role'] != 'admin'):
        return "YETKİSİZ ERİŞİM: Bu işlem için izniniz bulunmamaktadır.", 403

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    
    if user:
        # FIX A03: HTML Escaping ile XSS Engellendi
        safe_bio = escape(user['bio'] if user['bio'] else "Henüz bir bilgi girilmedi.")
        return render_template('profile_secure.html', user=user, bio=safe_bio)
    return "Kullanıcı bulunamadı!", 404

@app.route('/update_bio', methods=['POST'])
def update_bio():
    # Güvenli güncelleme: ID formdan değil sessiondan alınır
    if 'user_id' not in session:
        return "Lütfen giriş yapın!", 403
    
    new_bio = request.form['bio']
    current_user_id = session['user_id']

    conn = get_db_connection()
    conn.execute("UPDATE users SET bio = ? WHERE id = ?", (new_bio, current_user_id))
    conn.commit()
    conn.close()
    return redirect(url_for('profile', user_id=current_user_id))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    # A02: Canlıda debug=False olmalı
    app.run(debug=True, port=5001)