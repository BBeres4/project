# app.py
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session variables

# Sample product data
products = {
    1: {'id': 1, 'name': 'Burger', 'price': 9.99, 'image': 'burger.jpg', 'description': 'Delicious burger'},
    2: {'id': 2, 'name': 'Pizza', 'price': 12.99, 'image': 'pizza.jpg', 'description': 'Cheesy pizza'},
    # Add more products...
}

@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = products.get(product_id)
    return render_template('product.html', product=product)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        product = products[product_id]
        product['quantity'] = quantity
        product['subtotal'] = product['price'] * quantity
        cart_items.append(product)
        total += product['subtotal']
    return render_template('cart.html', cart=cart_items, total=total)

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    if product_id in cart:
        del cart[product_id]
        session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        order = {
            'name': request.form['name'],
            'email': request.form['email'],
            'address': request.form['address'],
            'cart': session.get('cart', {})
        }
        # Save to a file
        with open(f'orders/{order["name"]}.txt', 'w') as f:
            f.write(str(order))
        session.pop('cart', None)
        return redirect(url_for('thank_you', name=order['name']))
    return render_template('checkout.html')

@app.route('/thankyou')
def thank_you():
    name = request.args.get('name')
    return render_template('thankyou.html', name=name)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
