from flask import Flask, render_template, request, redirect, url_for, flash, g
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'
DATABASE = 'vulnerable.db'

# Connect to the database
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect(DATABASE)
    return g.sqlite_db

# Close database connection when the app is closed
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

# Home page - display books
@app.route('/')
def home():
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('SELECT id, title, author FROM books')
    books = cursor.fetchall()
    return render_template('home.html', books=books)

# Add Book - form to add a new book
@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']

        # Use parameterized queries to prevent SQL injection
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO books (title, author) VALUES (?, ?)', (title, author))
        connection.commit()

        flash('Book added successfully', 'success')
        return redirect(url_for('home'))
    return render_template('add_book.html')

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute('SELECT id, password FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[1], password):
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

# Initialize the database
if __name__ == '__main__':
    app.run(debug=True)
