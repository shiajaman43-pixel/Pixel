from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "pixel_ultra_mega_key_99"

# Data storage (Temporary)
products = []
orders = []
users = {"admin": "123"} # Default admin

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>PixelUltra Store</title>
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Press Start 2P', cursive; background: #fdfae6; padding: 20px; font-size: 10px; color: #2f3542; }
        .box { border: 4px solid #000; background: white; padding: 15px; margin-bottom: 20px; box-shadow: 6px 6px 0px #000; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 15px; }
        .card { border: 3px solid #333; padding: 10px; text-align: center; background: #fff; }
        .card img { width: 80px; height: 80px; object-fit: contain; image-rendering: pixelated; }
        
        input, textarea, select { font-family: 'Press Start 2P'; padding: 8px; margin: 5px 0; width: 85%; font-size: 8px; border: 2px solid #000; }
        button, .btn { font-family: 'Press Start 2P'; cursor: pointer; background: #ff4757; color: white; border: 3px solid #000; padding: 8px; font-size: 8px; text-decoration: none; display: inline-block; }
        
        .status { padding: 4px; border: 1px solid #000; font-size: 7px; }
        .pending { background: #ff7f50; } .packaging { background: #eccc68; } .delivered { background: #2ed573; }
        
        h1 { background: #2f3542; color: white; padding: 10px; text-align: center; font-size: 14px; border: 4px solid #000; }
        .nav-bar { display: flex; justify-content: space-between; margin-bottom: 20px; }
        .cart-count { color: red; }
    </style>
</head>
<body>
    <h1>PIXELULTRA STATIONARY</h1>
    
    <div class="nav-bar">
        <div>
            {% if session.get('user') %}
                <span>Hi, {{ session['user'] }}!</span>
                <a href="/logout" class="btn" style="background:#2f3542">LOGOUT</a>
            {% else %}
                <a href="/login" class="btn" style="background:#2f3542">LOGIN / SIGNUP</a>
            {% endif %}
        </div>
        <div>
            <a href="/cart" class="btn" style="background:#ffa502">CART (<span class="cart-count">{{ session.get('cart', [])|length }}</span>)</a>
            {% if session.get('user') and session['user'] != 'admin' %}
                <a href="/history" class="btn" style="background:#70a1ff">MY ORDERS</a>
            {% endif %}
        </div>
    </div>

    <div class="box">
        <h3>[*] SHOP GALLERY</h3>
        <div class="grid">
            {% for i in range(products|length) %}
            <div class="card">
                <img src="{{ products[i].image }}">
                <p>{{ products[i].name }}</p>
                <p style="color:green;">{{ products[i].price }} BDT</p>
                <a href="/add_to_cart/{{ i }}" class="btn">ADD TO CART</a>
            </div>
            {% endfor %}
        </div>
    </div>

    {% if session.get('user') == 'admin' %}
    <div class="box" style="border-color: blue;">
        <h3>[+] ADMIN: ADD PRODUCT</h3>
        <form action="/add_product" method="post">
            <input type="text" name="name" placeholder="Name" required>
            <input type="text" name="price" placeholder="Price" required>
            <input type="text" name="img_url" placeholder="Image URL" required>
            <button type="submit" style="background:blue">POST</button>
        </form>
    </div>

    <div class="box" style="border-color: green;">
        <h3>[!] MANAGE ALL ORDERS</h3>
        {% for order in orders %}
        <div style="border: 2px solid #000; padding: 10px; margin-bottom: 10px;">
            <p><strong>USER:</strong> {{ order.user }} | <strong>ITEM:</strong> {{ order.item }}</p>
            <p><strong>STATUS:</strong> <span class="status {{ order.status.lower() }}">{{ order.status }}</span></p>
            <form action="/update_status/{{ loop.index0 }}" method="post">
                <select name="new_status">
                    <option value="Pending">Pending</option>
                    <option value="Packaging">Packaging</option>
                    <option value="Delivered">Delivered</option>
                </select>
                <button type="submit" style="background:black">OK</button>
            </form>
        </div>
        {% endfor %}
    </div>
    {% endif %}
</body>
</html>
"""

# Cart & History Templates (Simplified)
CART_TEMPLATE = """
<body style="font-family:'Press Start 2P'; background:#fdfae6; padding:50px;">
    <h2>YOUR CART</h2>
    <div style="border:4px solid #000; background:white; padding:20px;">
        {% for item in cart_items %}
            <p>- {{ item.name }} ({{ item.price }} BDT)</p>
        {% else %}
            <p>Cart is empty!</p>
        {% endfor %}
        <hr>
        {% if cart_items %}
        <form action="/checkout" method="post">
            <input type="text" name="phone" placeholder="Phone" required><br>
            <textarea name="address" placeholder="Address" required></textarea><br>
            <button type="submit" style="padding:10px; cursor:pointer;">CONFIRM ORDER</button>
        </form>
        {% endif %}
        <br><a href="/">Back to Shop</a>
    </div>
</body>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, products=products, orders=orders)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u, p = request.form['u'], request.form['p']
        if u in users and users[u] == p:
            session['user'] = u
            return redirect(url_for('home'))
        elif u not in users:
            users[u] = p # Auto Signup
            session['user'] = u
            return redirect(url_for('home'))
    return """<body style="font-family:'Press Start 2P'; background:#2f3542; color:white; text-align:center; padding-top:100px;">
        <form method="post">
            <h2>LOGIN / SIGNUP</h2>
            <input name="u" placeholder="Username" required><br>
            <input name="p" type="password" placeholder="Password" required><br><br>
            <button type="submit">ENTER</button>
        </form>
    </body>"""

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/add_product', methods=['POST'])
def add_product():
    if session.get('user') == 'admin':
        products.append({'name': request.form['name'], 'price': request.form['price'], 'image': request.form['img_url']})
    return redirect(url_for('home'))

@app.route('/add_to_cart/<int:p_id>')
def add_to_cart(p_id):
    if 'cart' not in session: session['cart'] = []
    session['cart'].append(products[p_id])
    session.modified = True
    return redirect(url_for('home'))

@app.route('/cart')
def cart():
    return render_template_string(CART_TEMPLATE, cart_items=session.get('cart', []))

@app.route('/checkout', methods=['POST'])
def checkout():
    if not session.get('user'): return redirect(url_for('login'))
    cart_items = session.get('cart', [])
    for item in cart_items:
        orders.append({
            'user': session['user'],
            'item': item['name'],
            'phone': request.form['phone'],
            'address': request.form['address'],
            'status': 'Pending'
        })
    session['cart'] = []
    return "<h2>Order Placed!</h2><a href='/'>Go Home</a>"

@app.route('/history')
def history():
    user_orders = [o for o in orders if o['user'] == session.get('user')]
    return f"""<body style="font-family:'Press Start 2P'; background:#fdfae6; padding:20px;">
        <h2>MY ORDER HISTORY</h2>
        {user_orders if user_orders else 'No orders yet.'}
        <br><br><a href="/">Back</a>
    </body>"""

@app.route('/update_status/<int:o_id>', methods=['POST'])
def update_status(o_id):
    if session.get('user') == 'admin':
        orders[o_id]['status'] = request.form['new_status']
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
