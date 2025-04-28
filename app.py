from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


def get_db_connection():
    conn = sqlite3.connect('shop.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall() 
    conn.close()
    products = [
        {
            **dict(product), 
            'price': f"{product['price']:.2f}" 
        }
        for product in products
    ]
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()
    if not product:
        return redirect(url_for('index'))
    return render_template('product.html', product=product)

@app.route('/cart')
def cart():
    cart_items = []
    total_price = 0.0
    if 'cart' in session:
        conn = get_db_connection()
        for product_id in session['cart']:
            product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
            if product:
                product = dict(product)
                product['price'] = float(product['price']) 
                cart_items.append(product)
                total_price += product['price']
        conn.close()

    total_price = round(total_price, 2)
    print(f"Total price in cart: {total_price}")

    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session.pop('cart', None)
    return jsonify({'success': True})

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(product_id)
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if 'cart' in session:
        session['cart'] = [pid for pid in session['cart'] if pid != product_id]
        session.modified = True
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        total_price = request.form['total_price']

        conn = get_db_connection()
        conn.execute('INSERT INTO orders (customer_name, customer_email, customer_address, total_price) VALUES (?, ?, ?, ?)',
                     (name, email, address, total_price))
        conn.commit()
        conn.close()

        session.pop('cart', None)

        return render_template('thankyou.html', name=name, total_price=total_price)

    else:
        cart_items = []
        total_price = 0.00
        if 'cart' in session:
            conn = get_db_connection()
            for product_id in session['cart']:
                product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,))
                product = product.fetchone()
                if product:
                    product = dict(product)
                    product['price'] = float(product['price'])
                    cart_items.append(product)
                    total_price += product['price']
            conn.close()

        total_price = f"{total_price:.2f}" 

        return render_template('checkout.html', cart_items=cart_items, total_price=total_price)


@app.route('/thankyou')
def thank_you():
    return render_template('thankyou.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api/cart', methods=['GET'])
def get_cart():
    cart = session.get('cart', {})
    return jsonify(cart)

@app.route('/api/cart/add/<int:product_id>', methods=['POST'])
def api_add_to_cart(product_id):
    cart = session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    session['cart'] = cart
    return jsonify({'success': True, 'cart': cart})

@app.route('/api/cart/remove/<int:product_id>', methods=['POST'])
def api_remove_from_cart(product_id):
    cart = session.get('cart', {})
    if product_id in cart:
        del cart[product_id]
        session['cart'] = cart
    return jsonify({'success': True, 'cart': cart})

@app.route('/api/checkout', methods=['POST'])
def api_checkout():
    data = request.json
    order = {
        'name': data.get('name'),
        'email': data.get('email'),
        'address': data.get('address'),
        'cart': session.get('cart', {})
    }
    session.pop('cart', None)
    return jsonify({'success': True, 'order_id': '12345'})

if __name__ == '__main__':
    app.run(debug=True)
