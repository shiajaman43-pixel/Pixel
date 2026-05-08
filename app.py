from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "pixel_ultra_secret" # Session-er jonno proyojon

# Data storage
products = []
orders = []

# Admin Credentials (Ekhane apni password change korte paren)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "123"

# HTML Design
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>PixelUltra Store</title>
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Press Start 2P', cursive; background: #fdfae6; padding: 20px; font-size: 10px; }
        .box { border: 4px solid #000; background: white; padding: 20px; margin-bottom: 20px; box-shadow: 6px 6px 0px #000; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 15px; }
        .card { border: 3px solid #333; padding: 10px; text-align: center; background: #fff; }
        .card img { width: 80px; height: 80px; object-fit: contain; image-rendering: pixelated; }
        button, .btn { font-family: 'Press Start 2P'; cursor: pointer; background: #ff4757; color: white; border: 3px solid #000; padding: 8px; font-size: 8px; text-decoration: none; display: inline-block; }
        input { font-family: 'Press Start 2P'; padding: 8px; margin: 5px 0; width: 80%; font-size: 8px; border: 2px solid #000; }
        h1 { background: #2f3542; color: white; padding: 10px; text-align: center; font-size: 14px; margin-top: 0; }
        .admin-link { text-align: right; margin-bottom: 10px; }
        .order-box { background: #eccc68; padding: 10px; border: 2px dashed #000; margin-top: 10px; }
    </style>
</head>
<body>
    <h1>PIXELULTRA STATIONARY</h1>
    
    <div class="admin-link">
        {% if session.get('admin_logged_in') %}
            <a href="/logout" class="btn" style="background:#2f3542">LOGOUT</a>
        {% else %}
            <a href="/login" class="btn" style="background:#2f3542">ADMIN LOGIN</a>
        {% endif %}
    </div>

    <!-- CUSTOMER VIEW: SHOP -->
    <div class="box">
        <h3>[*] SHOP GALLERY</h3>
        <div class="grid">
            {% for i in range(products|length) %}
            <div class="card">
                <img src="{{ products[i].image }}">
                <p>{{ products[i].name }}</p>
                <p>{{ products[i].price }} BDT</p>
                <form action="/place_order/{{ i }}" method="post">
                    <input type="text" name="customer_name" placeholder="Your Name" required style="width:90%">
                    <button type="submit">ORDER NOW</button>
                </form>
            </div>
            {% endfor %}
        </div>
    </div>

    <!-- ADMIN ONLY VIEW -->
    {% if session.get('admin_logged_in') %}
    <div class="box" style="border-color: blue;">
        <h3 style="color: blue;">[+] ADMIN: ADD PRODUCT</h3>
        <form action="/add_product" method="post">
            <input type="text" name="name" placeholder="Item Name" required><br>
            <input type="text" name="price" placeholder="Price (BDT)" required><br>
            <input type="text" name="img_url" placeholder="Image URL" required><br>
            <button type="submit" style="background:blue">POST TO SHOP</button>
        </form>
    </div>

    <div class="box" style="border-color: green;">
        <h3 style="color: green;">[!] ADMIN: INCOMING ORDERS</h3>
        {% for order in orders %}
        <div class="order-box">
            <strong>CUSTOMER:</strong> {{ order.customer }} <br>
            <strong>PRODUCT:</strong> {{ order.item }} <br>
            <strong>STATUS:</strong> <span style="color:red;">{{ order.status }}</span>
        </div>
        {% else %}
        <p>No orders yet.</p>
        {% endfor %}
    </div>
    {% endif %}

</body>
</html>
"""

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Admin Login</title>
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Press Start 2P', cursive; background: #2f3542; display: flex; justify-content: center; align-items: center; height: 100vh; color: white; }
        .login-box { border: 5px solid white; padding: 30px; background: #000; text-align: center; }
        input { font-family: 'Press Start 2P'; padding: 10px; margin: 10px; width: 80%; }
        button { font-family: 'Press Start 2P'; padding: 10px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>ADMIN LOGIN</h2>
        <form method="post">
            <input type="text" name="username" placeholder="Username" required><br>
            <input type="password" name="password" placeholder="Password" required><br>
            <button type="submit">ENTER</button>
        </form>
        {% if error %}<p style="color:red">{{ error }}</p>{% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, products=products, orders=orders)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == ADMIN_USERNAME and request.form['password'] == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('home'))
        else:
            error = "Invalid Credentials!"
    return render_template_string(LOGIN_TEMPLATE, error=error)

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('home'))

@app.route('/add_product', methods=['POST'])
def add_product():
    if not session.get('admin_logged_in'): return redirect(url_for('login'))
    name = request.form.get('name')
    price = request.form.get('price')
    img_url = request.form.get('img_url')
    products.append({'name': name, 'price': price, 'image': img_url})
    return redirect(url_for('home'))

@app.route('/place_order/<int:product_id>', methods=['POST'])
def place_order(product_id):
    customer = request.form.get('customer_name')
    product = products[product_id]
    orders.append({'customer': customer, 'item': product['name'], 'status': 'Pending'})
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
