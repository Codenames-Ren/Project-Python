from flask import Flask, render_template

app = Flask(__name__)
menu = [
    {"id" : 1, "name" : "Espresso", "price" : 20000},
    {"id" : 2, "name" : "Cappucino", "price" : 25000},
    {"id" : 3, "name" : "Latte", "price" : 30000},
]

orders = []

@app.route('/')
def index():
    return render_template('index.html', menu=menu)

@app.route('/add_order', methods=['POST'])
def add_order():
    menu_id = int(request.form['menu_id'])
    quantity = int(request.form['quantity'])

    selected_menu = next((item for item in menu if item["id"] == menu_id), None)
    if selected_menu:
        orders.append({
            "menu_name" : selected_menu["name"],
            "quantity" : quantity,
            "total_price" : selected_menu["price"] * quantity
        })
    return redirect(url_for('index'))

@app.route('/orders')
def view_orders():
    return render_template('orders.html', orders=orders)

@app.route('/clear_orders')
def clear_orders():
    orders.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)