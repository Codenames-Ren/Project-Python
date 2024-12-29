#deklarasi import framework Flask sama SQLite
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3


app = Flask(__name__)
app.secret_key = "Algoritma"

#ini contoh awal pake list of dictionary
# menu = [
#     {"id" : 1, "name" : "Espresso", "price" : 20000},
#     {"id" : 2, "name" : "Cappucino", "price" : 25000},
#     {"id" : 3, "name" : "Latte", "price" : 30000},
# ]

# orders = []

#function buat manggil databasenya
def query_db(query, args=(), one=False):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(query, args)
    rv = cursor.fetchall()
    conn.commit()
    conn.close()
    return (rv[0] if rv else None) if one else rv

#Route ke login form
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        #Ngecek apakah usernamenya valid dan ada di database atau nggak
        user = query_db('SELECT * FROM users WHERE username = ? AND password = ?' [username, password], one=True)
        if user:
            session['username'] = user[1] #Nyimpen user di session pas login
            session['role'] = user[3] #Nyimpen rolenya di session pas login
            return redirect(url_for('homepage'))
        else:
            return render_template('login.html', error="Username atau Password Salah!")
    return render_template('login.html')

#route buat logout
@app.route('/logout')
def logout():
    session.clear() #ngehapus semua session (logout)
    return redirect(url_for('login'))

#route buat homepage
@app.route('/')
def homepage():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('homepage.html', username=session['username'], role=session['role'])

#route untuk fitur tambahan di menu
@app.route('/menu')
def menu():
    if 'username' not in session:
        return redirect(url_for('login'))
    menu = query_db('SELECT * FROM menu')
    return render_template('menu.html', menu=menu)

#Route buat nampilin pesanan versi user
@app.route('/orders')
def orders():
    if 'username' not in session:
        return redirect(url_for('login'))
    orders = query_db('SELECT * FROM orders')
    total_price = sum(order[3] for order in orders)
    return render_template('orders.html', orders=orders, total_price=total_price)

#Route buat admin
@app.route('/admin_page')
def admin_page():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    return render_template('admin_page.html')

#Ngirim data ke Database pake Metode POST *Kalo GET buat ngambil
# @app.route('/add_order', methods=['POST'])
# def add_order():
#     menu_id = int(request.form['menu_id'])
#     quantity = int(request.form['quantity'])

#     menu_item = query_db('SELECT name, price FROM menu WHERE id = ?', [menu_id], one=True)
#     if menu_item:
#         menu_name, price = menu_item
#         total_price = price * quantity

#         #Masukin pesanannya ke tabel orders
#         query_db('INSERT INTO orders(menu_name, quantity, total_price) VALUES (?, ?, ?)',
#                  [menu_name, quantity, total_price])

#     return redirect(url_for('index'))

# @app.route('/orders')
# def view_orders():
#     #Ngambil pesanan dari database
#     orders = query_db('SELECT * FROM orders')

#     #hitung total harga kopi yang dipesan
#     total_price = sum(order[3] for order in orders)
#     return render_template('orders.html', orders=orders, total_price=total_price)

# @app.route('/clear_orders')
# def clear_orders():
#     #Ngehapus semua data pesanan yang masuk di tabel orders (alias batal mesen)
#     query_db('DELETE FROM orders')
#     return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)