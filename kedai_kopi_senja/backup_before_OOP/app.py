#deklarasi import framework Flask sama SQLite
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3


app = Flask(__name__, static_folder='static')
app.secret_key = "Algoritma"

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
        user = query_db('SELECT * FROM users WHERE username = ? AND password = ?', (username, password), one=True)
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

#route untuk menu
@app.route('/menu')
def menu():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    elif session['role'] == 'admin':
        return redirect(url_for('admin_menu'))
    
    menu_data = query_db('SELECT * FROM menu')
    return render_template('menu.html', menu=menu_data)

#Route buat admin
@app.route('/admin_menu')
def admin_menu():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    menu_data = query_db('SELECT * FROM menu')
    return render_template('admin_menu.html', menu=menu_data)

@app.route('/about')
def about():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('about.html', username=session['username'], role=session['role'])

# #Route buat nampilin pesanan versi user
# @app.route('/orders')
# def orders():
#     if 'username' not in session:
#         return redirect(url_for('login'))
#     orders = query_db('SELECT * FROM orders')
#     total_price = sum(order[3] for order in orders)
#     return render_template('orders.html', orders=orders, total_price=total_price)

@app.route('/api/add_order', methods=['POST'])
def api_add_order():
    if 'username' not in session:
        return jsonify({"error": "Unautorized"}), 401
    
    data = request.json
    print("Data yang diterima : ", data)

    try:
        for item in data['cart']:
            menu_name = item['name']
            jumlah = item['jumlah']
            harga = item['harga']
            total_price = jumlah * harga
            username = session['username']

            print(f"Menu name : {menu_name}, Jumlah : {jumlah}, Harga : {harga}")
            query_db('UPDATE menu SET stock = stock - ? WHERE name = ?', [jumlah, menu_name])
            query_db('INSERT INTO orders(menu_name, quantity, total_price, username) VALUES (?, ?, ?, ?)', [menu_name, jumlah, total_price, username])
            print(f"Username : {username}, Total Price : {total_price}")
            
        return jsonify({"message": "Pesanan berhasil ditambahkan!"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error:" "Gagal mencatat pesanan. Mohon Coba lagi."}), 400

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'username' not in session:
        return redirect(url_for('login'))
    data = request.get_json()
    for item in data:
        menu_name = item['name']
        quantity = item['jumlah']
        price = item['harga'] * quantity
        
        #atur stock buat menu
        menu_item = query_db('SELECT stock FROM menu WHERE name = ?', [menu_name], one=True)
        if menu_item and menu_item[0] >= quantity:
            query_db('UPDATE menu SET stock = stock - ? WHERE name = ?', [quantity, menu_name])
            query_db('INSERT INTO orders(menu_name, quantity, total_prices) VALUES (?, ?, ?)', [menu_name, quantity, price])
        else:
            return {"message": f"Stock {menu_name} tidak cukup!"}, 400
    return {"Message": "Pesanan berhasil ditambahkan!"}

#API buat ngambil menu dari database
@app.route('/api/menu', methods=['GET'])
def api_get_menu():
    menu = query_db('SELECT * FROM menu')
    menu_list = [{"id": item[0], "name": item[1], "price": item[2], "stock": item[3], "image": item[4]} for item in menu]
    return jsonify({"menu": menu_list})

#API buat update stock
@app.route('/api/update_stock', methods=['POST'])
def api_update_stock():
    data = request.json
    print(data)
    try:
        for item in data['cart']:
            query_db('UPDATE menu SET stock = stock - ? WHERE name = ?', (item['jumlah'], item['name']))
        return jsonify({"message": "Success"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Terjadi kesalahan saat memproses permintaan. Mohon coba lagi nanti!"}), 400
    

if __name__ == "__main__":
    app.run(debug=True)