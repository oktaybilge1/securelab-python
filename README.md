🛡️ SecureLab-Python: Vulnerability & Remediation Lab
SecureLab-Python is a comprehensive laboratory project designed to analyze and exploit common critical web vulnerabilities (OWASP Top 10) and implement fixes following Secure Software Development Life Cycle (S-SDLC) principles.

The project provides both Vulnerable and Secure versions of the same application, demonstrating vulnerability detection and remediation processes from a cybersecurity engineer's perspective.

🚀 Key Features
Comparative Architecture: Side-by-side analysis of vulnerable vs. secure code blocks.

Modern UI/UX: Professional "Cybersecurity Dashboard" themed user panels optimized with Bootstrap 5.

Exploit Automation: Python scripts located in the exploits/ directory that prove vulnerabilities as Proof-of-Concept (PoC).

Robust Cryptography: Enhanced password security using Bcrypt hashing with a salt mechanism.

🛠️ Vulnerabilities & Technical Remediations
1. A03:2021 – Injection (SQL Injection)
Vulnerability: Manipulation of database queries and login bypass via direct injection of user input (f-strings).

Remediation: Isolated user input from the SQL command structure using Parameterized Queries.

2. A01:2021 – Broken Access Control (IDOR)
Vulnerability: Insecure Direct Object Reference; unauthorized data access and horizontal privilege escalation via URL parameters.

Remediation: Implemented Server-side Session Validation and object-level authorization. ID values are strictly verified against the user's active session.

3. A03:2021 – Injection (Stored XSS)
Vulnerability: Malicious JavaScript code stored in the database and executed in the user's browser (DOM).

Remediation: Applied Output Encoding (Jinja2 Auto-escaping) and the markupsafe.escape library for input sanitization.

4. A02:2021 – Cryptographic Failures
Vulnerability: Sensitive data (passwords) stored in the database as "Plain Text".

Remediation: Implemented Salted Hashing; every password is converted into complex hashes using the Bcrypt algorithm before storage.

📦 Installation and Usage
1. Clone the Repository
Bash
git clone https://github.com/oktaybilge1/securelab-python.git
cd securelab-python
2. Install Dependencies
Bash
pip install -r requirements.txt
3. Initialize Databases
Bash
# Initialize vulnerable database
python vulnerable_app/init_db.py

# Initialize secure database
python secure_app/init_db_secure.py
4. Run the Applications
Vulnerable App: python vulnerable_app/app.py (Port: 5000)

Secure App: python secure_app/app.py (Port: 5001)

🧪 Attack Simulation (Exploits)
Test the vulnerabilities using the automated scripts in the exploits/ folder:

Bash
# SQL Injection Bypass Test
python exploits/sqli_bypass.py

# IDOR Data Leak Test
python exploits/idor_scan.py


👤 Developer
Oktay Bilge - Software Developer & Cyber Security Specialist

LinkedIn: linkedin.com/in/oktaybilge

GitHub: @oktaybilge1


⚖️ Developed for educational and security awareness purposes only.