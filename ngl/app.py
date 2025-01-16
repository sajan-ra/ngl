from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3
import uuid

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            link_id TEXT UNIQUE NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link_id TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    link_id = str(uuid.uuid4())[:8]

    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, link_id) VALUES (?, ?)', (username, link_id))
        conn.commit()
        return jsonify({"message": "User registered successfully", "link": f"/send/{link_id}"})
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 400
    finally:
        conn.close()

@app.route('/send/<link_id>', methods=['GET', 'POST'])
def send_message(link_id):
    if request.method == 'GET':
        return render_template('send_message.html', link_id=link_id)

    if request.method == 'POST':
        message = request.form['message']
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO messages (link_id, message) VALUES (?, ?)', (link_id, message))
        conn.commit()
        conn.close()
        return jsonify({"message": "Message sent successfully"})

@app.route('/messages/<link_id>', methods=['GET'])
def view_messages(link_id):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT message, timestamp FROM messages WHERE link_id = ? ORDER BY timestamp DESC', (link_id,))
    messages = cursor.fetchall()
    conn.close()
    return render_template('view_messages.html', messages=messages)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
