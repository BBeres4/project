import sqlite3
conn = sqlite3.connect('shop.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    image_url TEXT
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    customer_email TEXT NOT NULL,
    customer_address TEXT NOT NULL,
    total_price REAL NOT NULL
)
''')

cursor.execute('SELECT COUNT(*) FROM products')
count = cursor.fetchone()[0]

if count == 0:
    real_products = [
    ('Bagel', 'Breakfast', 'Our bagels are boiled and baked the traditional way for that perfect chewy bite and golden crust you\'ll crave.', 2.50, '/static/bagel.png'),
    ('Croissant', 'Breakfast', 'Our croissant is a buttery, flaky pastry with a crescent shape, made from layered dough and butter. Crisp on the outside, soft and airy inside.', 2.00, '/static/croissant.png'),
    ('Omelette', 'Breakfast', 'Our omelette has onions, tomato, bacon and is filled with parmesan cheese.', 4.50, '/static/omelette.png'),
    ('Ham & Cheese', 'Sandwiches', 'Our Ham and Cheese is a sandwich with ham, american cheese and mayonnaise. It can be served cold or toasted.', 4.00, '/static/hamcheese.png'),
    ('BLT', 'Sandwiches', 'Our BLT is a traditional sandwich with bacon, lettuce, tomato and mayonnaise on fresh, made from scratch sourdough bread. Additional condiment(mustard, pickles, onions) available upon request.', 5.50, '/static/blt.png'),
    ('Turkey Melt', 'Sandwiches', 'Our turkey melt is a grilled sandwich with sliced turkey, melted swiss cheese, and mayonnaise on fresh, made from scratch sourdough bread. Additional condiment(mustard, pickles, onions) available upon request.', 5.00, '/static/turkey.png'),
    ('Chicken Noodle', 'Soups', 'Our homemade chicken noodle has fresh carrots, celery, and shredded chicken combined to create a delicious mixture of flavor.', 3.00, '/static/chicken_noodle.png'),
    ('Italian Wedding', 'Soups', 'Our Italian wedding soup has fresh, shredded lettuce, homemade meatballs, and rinsed carnaroli rice making our soup one of a kind.', 4.00, '/static/italian_wedding.png'),
    ('Tomato', 'Soups', 'Our tomato soup uses fresh, chopped tomatoes, creamy whipping cream, and red pepper flakes. Served hot and topped with organic herbs and spices.', 3.00, '/static/tomato.png')
]

    cursor.executemany('INSERT INTO products (name, category, description, price, image_url) VALUES (?, ?, ?, ?, ?)', real_products)

conn.commit()
conn.close()
