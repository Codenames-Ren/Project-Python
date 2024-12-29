import sqlite3

#bikin database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

#bikin tabel menu
cursor.execute('''
CREATE TABLE IF NOT EXISTS menu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    PRICE INTEGER NOT NULL
)
''')

#bikin table orders
cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
id INTEGER PRIMARY KEY AUTOINCREMENT,
menu_name TEXT NOT NULL,
quantity INTEGER NOT NULL,
total_price INTEGER NOT NULL)
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
INSERT INTO menu (name, price) VALUES (?, ?)
''', [
    ("Espresso", 20000),
    ("Cappuccino", 25000),
    ("Latte", 30000),
    ("Mocha", 35000),
    ("Americano", 22000)
])

#Hapus data user yang sebelumnya kalo ada user yang ditambah (biar gak keduplikat)
cursor.execute('DELETE FROM users')

#Nambah username user biasa sama admin ke table users
cursor.executemany('''
INSERT INTO users (username, password, role) VALUES (?, ?, ?)
''', [
    ("admin", "admin123", "admin"), #Admin
    ("user", "user123", "user") #User
])

#commit/nandain perubahan & nutup koneksi
conn.commit()
conn.close()

print("Database Berhasil Diupdate!")