import sqlite3

#bikin database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

#hapus tabel lama kalo ada perubahan
cursor.execute('DROP TABLE IF EXISTS menu')
# cursor.execute('DROP TABLE IF EXISTS orders')
# cursor.execute('DROP TABLE IF EXISTS users')

#bikin tabel menu
cursor.execute('''
CREATE TABLE IF NOT EXISTS menu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER NOT NULL,
    stock INTEGER NOT NULL,
    image TEXT NOT NULL
)
''')

#bikin table orders
cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    menu_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    total_price INTEGER NOT NULL
)
''')

#Bikin table users
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN('admin', 'user'))
)
''')

#Hapus data lama kalo ada update dari databasenya biar gak duplikat
cursor.execute('DELETE FROM menu')

#nambah list menunya
cursor.executemany('''
INSERT INTO menu (name, price, stock, image) VALUES (?, ?, ?, ?)
''', [
    ("Espresso", 20000, 6, "/static/images/espresso.png"),
    ("Cappuccino", 25000, 5, "/static/images/cappuccino.jpg"),
    ("Latte", 30000, 12, "/static/images/latte.jpg"),
    ("Mocha", 35000, 20, "/static/images/mocha.jpg"),
    ("Americano", 22000, 25, "/static/images/americano.png")
])

#Hapus data user yang sebelumnya kalo ada user yang ditambah (biar gak keduplikat)
cursor.execute('DELETE FROM users')

#Nambah username user biasa sama admin ke table users
cursor.executemany('''
INSERT INTO users (username, password, role) VALUES (?, ?, ?)
''', [
    ("admin", "admin123", "admin"), #Admin
    ("user", "user123", "user"), #User
    ("ren", "ren11", "user"), #User2
    ("bayu", "bayu11", "admin") #Admin2
])

#commit/nandain perubahan & nutup koneksi
conn.commit()
conn.close()

print("Database Berhasil Diupdate!")