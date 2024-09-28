from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import string
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('url_shortener.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create the database and table (run this once)
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            custom_url TEXT UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

# Generate a random string for custom URLs
def generate_custom_url(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['original_url']
        custom_url = request.form['custom_url']

        if not original_url:
            flash('The original URL is required!')
            return redirect(url_for('index'))

        # Generate random short link if no custom URL is provided
        if not custom_url:
            custom_url = generate_custom_url()

        # Insert into the database
        try:
            conn = get_db_connection()
            conn.execute('INSERT INTO urls (original_url, custom_url) VALUES (?, ?)',
                         (original_url, custom_url))
            conn.commit()
            conn.close()
            flash(f'Shortened URL: {request.host_url}{custom_url}')
        except sqlite3.IntegrityError:
            flash('Custom URL already taken. Try another one.')
            return redirect(url_for('index'))

    return render_template('index.html')


@app.route('/<custom_url>')
def redirect_to_url(custom_url):
    conn = get_db_connection()
    url_data = conn.execute('SELECT original_url FROM urls WHERE custom_url = ?', (custom_url,)).fetchone()
    conn.close()

    if url_data is None:
        flash('Invalid short URL.')
        return redirect(url_for('index'))

    return redirect(url_data['original_url'])

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
