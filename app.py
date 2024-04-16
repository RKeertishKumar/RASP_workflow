from flask import Flask, request, render_template
import sqlite3
#from pyrasp.pyrasp import FlaskRASP
app = Flask(__name__)
FlaskRASP(app, conf = rasp.json)
#FlaskRASP(app, conf = 'rasp.json')
# Vulnerable SQLite database setup
conn = sqlite3.connect('vulnerable_app.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
c.execute("INSERT INTO users (username, password) VALUES ('admin', 'adminpass')")
conn.commit()
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # Vulnerable SQL query with concatenation (SQLi vulnerability)
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    c.execute(query)
    user = c.fetchone()
    if user:
        return f"Welcome, {user[1]}!"
    else:
        return "Invalid credentials."
@app.route('/search')
def search():
    query = request.args.get('q', '')
    # Vulnerable endpoint susceptible to XSS
    return render_template('search.html', query=query)
if __name__ == '__main__':
    app.run(debug=True)
