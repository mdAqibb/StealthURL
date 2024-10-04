from flask import Flask, render_template, request, redirect, abort, Response
import sqlite3
import string
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('urls.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS urls
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     original_url TEXT NOT NULL,
                     short_url TEXT UNIQUE NOT NULL,
                     password TEXT,
                     count INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

def generate_short_url():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

def proxy_request(url):
    try:
        resp = requests.get(url)
        content_type = resp.headers.get('Content-Type', '')
        
        if 'text/html' in content_type:
            return modify_html(resp.text, url)
        else:
            return resp.content, content_type
    except requests.RequestException as e:
        return f"Error: {str(e)}", "text/plain"

def modify_html(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Update relative URLs to absolute URLs
    for tag in soup.find_all(['a', 'link', 'script', 'img']):
        for attr in ['href', 'src']:
            if tag.has_attr(attr):
                tag[attr] = urljoin(base_url, tag[attr])
    
    # Add base tag to ensure relative paths resolve correctly
    base_tag = soup.new_tag('base', href=base_url)
    if soup.head is None:
        soup.html.insert(0, soup.new_tag('head'))
    soup.head.insert(0, base_tag)
    
    # Inject our proxy script
    proxy_script = soup.new_tag('script')
    proxy_script.string = """
    (function() {
        var originalFetch = window.fetch;
        window.fetch = function(input, init) {
            if (typeof input === 'string') {
                input = '/proxy_fetch?url=' + encodeURIComponent(input);
            }
            return originalFetch.apply(this, arguments);
        };
    })();
    """
    if soup.body is None:
        soup.html.append(soup.new_tag('body'))
    soup.body.append(proxy_script)
    
    return str(soup), 'text/html'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['original_url']
        custom_path = request.form['custom_path']
        password_protected = 'password_protected' in request.form
        password = request.form['password'] if password_protected else None

        if custom_path:
            short_url = custom_path
        else:
            short_url = generate_short_url()

        conn = get_db_connection()
        existing_url = conn.execute('SELECT * FROM urls WHERE short_url = ?', (short_url,)).fetchone()
        if existing_url:
            conn.close()
            return render_template('index.html', error="Custom path already exists. Please choose another.")

        conn.execute('INSERT INTO urls (original_url, short_url, password) VALUES (?, ?, ?)',
                     (original_url, short_url, password))
        conn.commit()
        conn.close()

        shortened_url = request.host_url + 'proxy/' + short_url
        return render_template('index.html', shortened_url=shortened_url)

    return render_template('index.html')

@app.route('/proxy/<short_url>', methods=['GET', 'POST'])
def proxy_url(short_url):
    conn = get_db_connection()
    url = conn.execute('SELECT * FROM urls WHERE short_url = ?', (short_url,)).fetchone()
    
    if url is None:
        conn.close()
        abort(404)
    
    if url['count'] > 0:
        conn.close()
        abort(410)  # Gone - link has expired

    if url['password']:
        if request.method == 'POST':
            if request.form['password'] == url['password']:
                conn.execute('UPDATE urls SET count = count + 1 WHERE short_url = ?', (short_url,))
                conn.commit()
                conn.close()
                # Instead of rendering a template, proxy the content directly
                content, content_type = proxy_request(url['original_url'])
                return Response(content, content_type=content_type)
            else:
                conn.close()
                return render_template('redirect.html', error="Incorrect password")
        else:
            conn.close()
            return render_template('redirect.html')
    else:
        conn.execute('UPDATE urls SET count = count + 1 WHERE short_url = ?', (short_url,))
        conn.commit()
        conn.close()
        content, content_type = proxy_request(url['original_url'])
        return Response(content, content_type=content_type)

@app.route('/proxy_fetch')
def proxy_fetch():
    url = request.args.get('url')
    if not url:
        abort(400)
    
    content, content_type = proxy_request(url)
    return Response(content, content_type=content_type)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)