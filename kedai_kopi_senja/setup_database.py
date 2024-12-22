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

#nambah list menunya
cursor.executemany('''
INSERT INTO menu (name, prices) VALUES (?, ?)
''', [
    ("Espresso", 20000),
    ("Cappuccino", 25000),
    ("Latte", 30000)
])

#commit/nandain perubahan & nutup koneksi
conn.commit()
conn.close()

print("Database Berhasil Dibuat!")