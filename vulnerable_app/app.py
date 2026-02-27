from flask import Flask, request, render_template, redirect, url_for, render_template_string
import sqlite3
import os

app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'database.db')

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
        password = request.form['password']
        conn = get_db_connection()
        # A05: Injection açığı (f-string kullanımı)  / # A05: Injection vulnerability (f-string usage)
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        user = conn.execute(query).fetchone()
        conn.close()
        if user:
            return redirect(url_for('profile', user_id=user['id']))
        return "Hatalı giriş!", 401
    return render_template('login.html')

@app.route('/profile/<int:user_id>', methods=['GET'])
def profile(user_id):
    conn = get_db_connection()
    # A01: IDOR açığı (Oturum kontrolü yok) / A01: IDOR vulnerability (No session control)
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if user:
        # A03: Stored XSS açığı (render_template_string kullanımı) / A03: Stored XSS vulnerability (render_template_string usage)
        html_template = f"""
        <!DOCTYPE html>
        <html lang="tr">
        <head>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <title>Vulnerable Profile</title>
        </head>
        <body class="bg-dark text-danger" style="font-family: 'Courier New', Courier, monospace;">
            <nav class="navbar navbar-dark bg-danger mb-4 shadow"><div class="container"><span class="navbar-brand fw-bold">⚠️ VULNERABLE_ZONE</span></div></nav>
            <div class="container">
                <div class="card bg-black border-danger text-danger p-4 shadow-lg">
                    <h2 class="fw-bold">ACCESS_GRANTED: {user['username']}</h2>
                    <hr class="border-danger">
                    <p><strong>CURRENT_BIO:</strong> {user['bio']}</p>
                    <form action="/update_bio" method="POST" class="mt-4 p-3 border border-danger">
                        <label class="form-label small">INJECT_PAYLOAD:</label>
                        <input type="hidden" name="user_id" value="{user['id']}">
                        <textarea name="bio" class="form-control bg-dark text-danger border-danger mb-3" rows="3"></textarea>
                        <button class="btn btn-danger w-100 fw-bold">EXECUTE_UPDATE</button>
                    </form>
                    <a href="/logout" class="mt-4 text-center text-decoration-none text-danger small">>> TERMINATE_SESSION</a>
                </div>
            </div>
        </body>
        </html>
        """
        return render_template_string(html_template)
    return "Kullanıcı bulunamadı!", 404

@app.route('/update_bio', methods=['POST'])
def update_bio():
    user_id = request.form['user_id']
    new_bio = request.form['bio']
    conn = get_db_connection()
    conn.execute("UPDATE users SET bio = ? WHERE id = ?", (new_bio, user_id))
    conn.commit()
    conn.close()
    return redirect(url_for('profile', user_id=user_id))

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)