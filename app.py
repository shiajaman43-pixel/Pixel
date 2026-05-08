from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "pixel_ultra_secret_key_123"

# Data storage (In-memory)
products = []
orders = []

# Admin Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "123"

# HTML Template (All-in-one)
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
        .card img { width: 80px; height: 80px; object-fit: contain; image-rendering: pixelated; margin-bottom: 10px; }
        
        input, textarea, select { font-family: 'Press Start 2P'; padding: 8px; margin: 5px 0; width: 85%; font-size: 8px; border: 2px solid #000; }
        button, .btn { font-family: 'Press Start 2P'; cursor: pointer; background: #ff4757; color: white; border: 3px solid #000; padding: 8px; font-size: 8px; text-decoration: none; display: inline-block; }
        
        .status-tag { padding: 4px; border: 1px solid #000; font-size: 7px; display: inline-block; margin-top: 5px; }
        .pending { background: #ff7f50; }
        .packaging { background: #eccc68; }
        .delivered { background: #2ed573; color: white; }
        
        h1 { background: #2f3542; color: white; padding: 10px; text-align: center; font-size: 14px; margin-top: 0; border: 4px solid #000; }
        h3 { border-bottom: 2px solid #000; padding-bottom: 5px; }
        .admin-nav { text-align: right; margin-bottom: 10px; }
    </style>
</head>
<body>
    <h1>PIXELULTRA STATIONARY</h1>
    
    <div class="admin-nav">
        {% if session.get('admin_logged_in') %}
            <a href="/logout" class="btn" style="background:#2f3542">LOGOUT ADMIN</a>
        {% else %}
            <a href="/login" class="btn" style="background:#2f3542">ADMIN LOGIN</a>
        {% endif %}
    </div>

    <div class="box">
        <h3>[*] STATIONARY SHOP</h3>
        <div class="grid">
            {% for i in range(products|length) %}
            <div class="card">
                <img src="{{ products[i].image }}">
                <p>{{ products[i].name }}</p>
                <p style="color:green;">{{ products[i].price }} BDT</p>
                
                <hr>
                <form action="/place_order/{{ i }}" method="post">
                    <input type="text" name="c_name" placeholder="Name" required>
                    <input type="text" name="c_phone" placeholder="Phone" required>
                    <textarea name="c_address" placeholder="Address" rows="2" required></textarea>
                    <button type="submit">ORDER NOW</button>
                </form>
            </div>
            {% endfor %}
            {% if not products %}<p>No products added yet.</p>{% endif %}
        </div>
    </div>

    {% if session.get('admin_logged_in') %}
    <div class="box" style="border-color: #3742fa;">
        <h3 style="color: #3742fa;">[+] ADMIN: ADD PRODUCT</h3>
        <form action="/add_product" method="post">
            <input type="text" name="name" placeholder="Product Name" required>
            <input type="text" name="price" placeholder="Price (BDT)" required>
            <input type="text" name="img_url" placeholder="Image URL (Direct Link)" required>
            <br><button type="submit" style="background:#3742fa">POST PRODUCT</button>
        </form>
    </div>

    <div class="box" style="border-color: #2ed573;">
        <h3 style="color: #2ed573;">[!] ADMIN: MANAGE ORDERS</h3>
        {% for order in orders %}
        <div style="border: 2px solid #000; padding: 10px; margin-bottom: 10px; background: #f1f2f6;">
            <p><strong>ORDER ID:</strong> #{{ loop.index }}</p>
            <p><strong>CUSTOMER:</strong> {{ order.customer }} ({{ order.phone }})</p>
            <p><strong>ADDRESS:</strong> {{ order.address }}</p>
            <p><strong>ITEM:</strong> {{ order.item }}</p>
            <p><strong>STATUS:</strong> 
                <span class="status-tag {{ order.status.lower() }}">{{ order.status }}</span>
            </p>
            
            <form action="/update_status/{{ loop.index0 }}" method="post" style="margin-top:10px;">
                <select name="new_status">
                    <option value="Pending" {% if order.status == 'Pending' %}selected{% endif %}>Pending</option>
                    <option value="Packaging" {% if order.status == 'Packaging' %}selected{% endif %}>Packaging</option>
                    <option value="Delivered" {% if order.status == 'Delivered' %}selected{% endif %}>Delivered</option>
                </select>
                <button type="submit" style="background:#2f3542; padding: 5px;">UPDATE</button>
            </form>
        </div>
        {% else %}
        <p>No orders to manage.</p>
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
        input { font-family: 'Press Start 2P'; padding: 10px; margin: 10px; width: 80%; border: 2px solid #fff; }
        button { font-family: 'Press Start 2P'; padding: 10px; cursor: pointer; background: #fff; border: none; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>ADMIN ACCESS</h2>
        <form method="post">
            <input type="text" name="user" placeholder="Username" required><br>
            <input type="password" name="pass" placeholder="Password" required><br>
            <button type="submit">LOGIN</button>
        </form>
        {% if error %}<p style="color:red; font-size:8px;">{{ error }}</p>{% endif %}
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
        if request.form['user'] == ADMIN_USERNAME and request.form['pass'] == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('home'))
        error = "WRONG CREDENTIALS!"
    return render_template_string(LOGIN_TEMPLATE, error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/add_product', methods=['POST'])
def add_product():
    if not session.get('admin_logged_in'): return redirect(url_for('login'))
    products.append({
        'name': request.form.get('name'),
        'price': request.form.get('price'),
        'image': request.form.get('img_url')
    })
    return redirect(url_for('home'))

@app.route('/place_order/<int:p_id>', methods=['POST'])
def place_order(p_id):
    if p_id < len(products):
        orders.append({
            'customer': request.form.get('c_name'),
            'phone': request.form.get('c_phone'),
            'address': request.form.get('c_address'),
            'item': products[p_id]['name'],
            'status': 'Pending'
        })
    return redirect(url_for('home'))

@app.route('/update_status/<int:o_id>', methods=['POST'])
def update_status(o_id):
    if session.get('admin_logged_in') and o_id < len(orders):
        orders[o_id]['status'] = request.form.get('new_status')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
