#deklarasi import framework Flask sama SQLite
from flask import Flask, render_template, request, redirect, url_for
import sqlite3


app = Flask(__name__)

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

@app.route('/')
def index():
    #Request atau ambil data dari database
    menu = query_db('SELECT * FROM menu')
    return render_template('index.html', menu=menu)

#Ngirim data ke Database pake Metode POST *Kalo GET buat ngambil
@app.route('/add_order', methods=['POST'])
def add_order():
    menu_id = int(request.form['menu_id'])
    quantity = int(request.form['quantity'])

    menu_item = query_db('SELECT name, price FROM menu WHERE id = ?', [menu_id], one=True)
    if menu_item:
        menu_name, price = menu_item
        total_price = price * quantity

        #Masukin pesanannya ke tabel orders
        query_db('INSERT INTO orders(menu_name, quantity, total_price) VALUES (?, ?, ?)',
                 [menu_name, quantity, total_price])

    return redirect(url_for('index'))

@app.route('/orders')
def view_orders():
    #Ngambil pesanan dari database
    orders = query_db('SELECT * FROM orders')
    return render_template('orders.html', orders=orders)

@app.route('/clear_orders')
def clear_orders():
    #Ngehapus semua data pesanan yang masuk di tabel orders (alias batal mesen)
    query_db('DELETE FROM orders')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)