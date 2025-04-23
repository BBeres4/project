# app.py
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session variables

# Product data matching the HTML templates
products = {
    'bagel': {'id': 'bagel', 'name': 'Bagel', 'price': 2.50, 'image': 'bagel.png', 'description': 'Our bagels are boiled and baked the traditional way for that perfect chewy bite and golden crust you\'ll crave.'},
    'croissant': {'id': 'croissant', 'name': 'Croissant', 'price': 2.00, 'image': 'croissant.png', 'description': 'Flaky, buttery croissants baked fresh daily.'},
    'omelette': {'id': 'omelette', 'name': 'Omelette', 'price': 4.50, 'image': 'omelette.png', 'description': 'Fluffy omelette made with farm-fresh eggs and your choice of fillings.'},
    'hamcheese': {'id': 'hamcheese', 'name': 'Ham & Cheese', 'price': 4.00, 'image': 'hamcheese.png', 'description': 'Classic ham and cheese sandwich on freshly baked bread.'},
    'blt': {'id': 'blt', 'name': 'BLT', 'price': 5.50, 'image': 'blt.png', 'description': 'Bacon, lettuce, and tomato sandwich on toasted bread.'},
    'turkey': {'id': 'turkey', 'name': 'Turkey Melt', 'price': 5.00, 'image': 'turkey.png', 'description': 'Sliced turkey with melted cheese and cranberry sauce.'},
    'chicken_noodle': {'id': 'chicken_noodle', 'name': 'Chicken Noodle', 'price': 3.00, 'image': 'chicken_noodle.png', 'description': 'Hearty chicken noodle soup made from scratch.'},
    'italian_wedding': {'id': 'italian_wedding', 'name': 'Italian Wedding', 'price': 4.00, 'image': 'italian_wedding.png', 'description': 'Traditional Italian wedding soup with meatballs and vegetables.'},
    'tomato': {'id': 'tomato', 'name': 'Tomato', 'price': 3.00, 'image': 'tomato.png', 'description': 'Creamy tomato soup with a hint of basil.'}
}

# Product categories
categories = {
    'breakfast': ['bagel', 'croissant', 'omelette'],
    'sandwiches': ['hamcheese', 'blt', 'turkey'],
    'soups': ['chicken_noodle', 'italian_wedding', 'tomato']
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/product/<product_id>')
def product_detail(product_id):
    product = products.get(product_id)
    if not product:
        return redirect(url_for('index'))
    return render_template('product.html', product=product)

@app.route('/product.html')
def product_default():
    # Default to the first product
    product = products['bagel']
    return render_template('product.html', product=product)

@app.route('/product2.html')
def product2():
    product = products['croissant']
    return render_template('product2.html', product=product)

@app.route('/product3.html')
def product3():
    product = products['omelette']
    return render_template('product3.html', product=product)

@app.route('/product4.html')
def product4():
    product = products['hamcheese']
    return render_template('product4.html', product=product)

@app.route('/product5.html')
def product5():
    product = products['blt']
    return render_template('product5.html', product=product)

@app.route('/product6.html')
def product6():
    product = products['turkey']
    return render_template('product6.html', product=product)

@app.route('/product7.html')
def product7():
    product = products['chicken_noodle']
    return render_template('product7.html', product=product)

@app.route('/product8.html')
def product8():
    product = products['italian_wedding']
    return render_template('product8.html', product=product)

@app.route('/product9.html')
def product9():
    product = products['tomato']
    return render_template('product9.html', product=product)

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/thankyou')
def thank_you():
    return render_template('thankyou.html')

@app.route('/about')
def about():
    return render_template('about.html')

# API endpoints for server-side cart management (optional)
@app.route('/api/cart', methods=['GET'])
def get_cart():
    cart = session.get('cart', {})
    return jsonify(cart)

@app.route('/api/cart/add/<product_id>', methods=['POST'])
def api_add_to_cart(product_id):
    cart = session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    session['cart'] = cart
    return jsonify({'success': True, 'cart': cart})

@app.route('/api/cart/remove/<product_id>', methods=['POST'])
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
    # Save order to a file or database
    session.pop('cart', None)
    return jsonify({'success': True, 'order_id': '12345'})

if __name__ == '__main__':
    app.run(debug=True)
