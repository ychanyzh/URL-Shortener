from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3
import random
import string

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database setup
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_url TEXT NOT NULL,
        short_url TEXT NOT NULL UNIQUE
    )''')
    conn.commit()
    conn.close()

# Generate short URL
def generate_short_url():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=6))

# Save URL to database
def save_url(original_url, short_url):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO urls (original_url, short_url) VALUES (?, ?)", (original_url, short_url))
    conn.commit()
    conn.close()

# Get original URL from short URL
def get_original_url(short_url):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT original_url FROM urls WHERE short_url = ?", (short_url,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['original_url']
        short_url = generate_short_url()
        save_url(original_url, short_url)
        flash(f'Your short URL is: {request.host_url}{short_url}')
        return render_template('result.html', short_url=short_url)
    return render_template('index.html')

@app.route('/<short_url>')
def redirect_to_url(short_url):
    original_url = get_original_url(short_url)
    if original_url:
        return redirect(original_url)
    else:
        flash('Invalid URL')
        return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)