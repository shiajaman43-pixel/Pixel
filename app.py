from flask import Flask, render_template_string, request, redirect, url_for, session
import smtplib, random

app = Flask(__name__)
app.secret_key = "pixel_ultra_final_secret_key"

# --- GOOGLE GMAIL CONFIG ---
# Ekhane apnar asol Gmail address-ti bhashan:
SENDER_EMAIL = "apnar-email@gmail.com" 
SENDER_PASS = "qesd sqzt zpou cccc" 

# Data Storage (Note: Render restart hole eita khali hoye jabe)
products = []
orders = []

# Admin Credentials
ADMIN_U = "admin"
ADMIN_P = "123"

# --- HTML DESIGN (All-in-one Pixel Style) ---
BASE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>PixelUltra Shop</title>
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Press Start 2P', cursive; background: #fdfae6; padding: 20px; font-size: 10px; color: #2f3542; line-height: 1.6; }
        .box { border: 4px solid #000; background: white; padding: 15px; margin-bottom: 20px; box-shadow: 6px 6px 0px #000; }
        .btn { font-family: 'Press Start 2P'; cursor: pointer; background: #ff4757; color: white; border: 3px solid #000; padding: 8px; font-size: 8px; text-decoration: none; display: inline-block; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 15px; }
        .card { border: 3px solid #333; padding: 10px; text-align: center; background: #fff; }
        .card img { width: 80px; height: 80px; object-fit: contain; image-rendering: pixelated; margin-bottom: 10px; }
        input, select, textarea { font-family: 'Press Start 2P'; padding: 10px; border: 2px solid #000; margin: 5px 0; width: 90%; font-size: 8px; }
        h1 { background: #2f3542; color: white; padding: 10px; text-align: center; border: 4px solid #000; font-size: 14px; margin-bottom: 20px; }
        .status { padding: 4px; border: 1px solid #000; font-size: 7px; text-transform: uppercase; }
        .pending { background: #ffa502; } .packaging { background: #eccc68; } .delivered { background: #2ed573; color: white; }
        .nav { display: flex; justify-content: space-between; margin-bottom: 20px; }
    </style>
</head>
<body>
    <h1>PIXELULTRA STATIONARY</h1>
    <div class="nav">
        <div>
            {% if session.get('user') %}
                <span>HI, {{ session['user'].split('@')[0] }}!</span> | <a href="/logout" class="btn" style="background:gray">LOGOUT</a>
            {% else %}
                <a href="/login" class="btn" style="background:#4285F4">GMAIL LOGIN</a>
                <a href="/admin_login" class="btn" style="background:#000">ADMIN</a>
            {% endif %}
        </div>
        <div>
            <a href="/cart" class="btn" style="background:orange">BAG ({{ session.get('cart', [])|length }})</a>
            {% if session.get('user') and not session.get('is_admin') %}
                <a href="/history" class="btn" style="background:blue">HISTORY</a>
            {% endif %}
        </div>
    </div>
    {% block content %}{% endblock %}
</body>
</html>
"""

# --- ROUTES ---

@app.route('/')
def home():
    return render_template_string(BASE_HTML + """
    {% block content %}
    <div class="box">
        <h3>[*] SHOP GALLERY</h3>
        <div class="grid">
            {% for i in range(products|length) %}
            <div class="card">
                <img src="{{ products[i].image }}">
                <p>{{ products[i].name }}</p>
                <p style="color:green;">{{ products[i].price }} BDT</p>
                <a href="/add_to_cart/{{ i }}" class="btn">ADD TO BAG</a>
            </div>
            {% endfor %}
            {% if not products %}<p style="color:gray;">No products yet. Admin, please add some!</p>{% endif %}
        </div>
    </div>
    {% if session.get('is_admin') %}
    <div class="box" style="border-color:blue;">
        <h3 style="color:blue;">[+] ADMIN: ADD PRODUCT</h3>
        <form action="/add_product" method="post">
            <input name="name" placeholder="Item Name" required>
            <input name="price" placeholder="Price" required>
            <input name="img" placeholder="Image URL (Direct Link)" required>
            <button type="submit" class="btn" style="background:blue">POST TO SHOP</button>
        </form>
    </div>
    <div class="box" style="border-color:red;">
        <h3 style="color:red;">[!] ADMIN: MANAGE ORDERS</h3>
        {% for o in orders %}
        <div style="border-bottom:2px dashed #000; padding:10px; margin-bottom:5px;">
            <p><strong>USER:</strong> {{ o.user }} | <strong>ITEM:</strong> {{ o.item }}</p>
            <p><strong>STATUS:</strong> <span class="status {{ o.status.lower() }}">{{ o.status }}</span></p>
            <form action="/update_status/{{ loop.index0 }}" method="post" style="display:inline;">
                <select name="st" style="width:auto;"><option value="Pending">Pending</option><option value="Packaging">Packaging</option><option value="Delivered">Delivered</option></select>
                <button type="submit" class="btn" style="background:black">UPDATE</button>
            </form>
        </div>
        {% else %}<p>No orders yet.</p>{% endfor %}
    </div>
    {% endif %}
    {% endblock %}
    """, products=products, orders=orders)

@app.route('/login')
def login_page():
    return render_template_string(BASE_HTML + """
    {% block content %}
    <div class="box" style="text-align:center;">
        <h3>GMAIL OTP LOGIN</h3>
        <form action="/send_otp" method="post">
            <input name="email" type="email" placeholder="Enter Gmail Address" required><br><br>
            <button type="submit" class="btn" style="background:#4285F4">SEND CODE</button>
        </form>
    </div>
    {% endblock %}
    """)

@app.route('/send_otp', methods=['POST'])
def send_otp():
    email = request.form['email']
    otp = str(random.randint(1000, 9999))
    session['temp_email'] = email
    session['temp_otp'] = otp
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASS)
        msg = f"Subject: PixelShop OTP\\n\\nYour secret code is: {otp}"
        server.sendmail(SENDER_EMAIL, email, msg)
        server.quit()
        return render_template_string(BASE_HTML + """
        {% block content %}
        <div class="box" style="text-align:center;">
            <h3>VERIFY OTP</h3>
            <p>Check your email: {{ email }}</p>
            <form action="/verify_otp" method="post">
                <input name="otp" placeholder="Enter 4-digit code" required><br><br>
                <button type="submit" class="btn" style="background:green">VERIFY & ENTER</button>
            </form>
        </div>
        {% endblock %}
        """, email=email)
    except Exception as e:
        return f"<h3>Email Error!</h3><p>Make sure SENDER_EMAIL is correct and App Password is valid.</p><br><a href='/login'>Try Again</a>"

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    if request.form['otp'] == session.get('temp_otp'):
        session['user'] = session['temp_email']
        session['is_admin'] = False
        return redirect('/')
    return "<h3>Wrong OTP!</h3><a href='/login'>Go back and try again</a>"

@app.route('/add_to_cart/<int:p_id>')
def add_to_cart(p_id):
    if 'cart' not in session: session['cart'] = []
    session['cart'].append(products[p_id])
    session.modified = True
    return redirect('/')

@app.route('/cart')
def cart():
    items = session.get('cart', [])
    return render_template_string(BASE_HTML + """
    {% block content %}
    <div class="box">
        <h3>YOUR BAG</h3>
        {% for i in items %}<p>- {{ i.name }} ({{ i.price }} BDT)</p>
        {% else %}<p>Your bag is empty!</p>{% endfor %}
        <hr>
        {% if items %}
        <form action="/checkout" method="post">
            <input name="phone" placeholder="Phone Number" required>
            <textarea name="addr" placeholder="Full Delivery Address" required></textarea>
            <button type="submit" class="btn" style="background:green; width:100%;">CONFIRM ORDER</button>
        </form>
        {% endif %}
        <br><a href="/" style="font-size:8px;">Back to shop</a>
    </div>
    {% endblock %}
    """, items=items)

@app.route('/checkout', methods=['POST'])
def checkout():
    if not session.get('user'): return redirect('/login')
    for i in session.get('cart', []):
        orders.append({
            'user': session['user'], 
            'item': i['name'], 
            'status': 'Pending', 
            'phone': request.form['phone'], 
            'addr': request.form['addr']
        })
    session['cart'] = []
    return redirect('/history')

@app.route('/history')
def history():
    my_orders = [o for o in orders if o['user'] == session.get('user')]
    return render_template_string(BASE_HTML + """
    {% block content %}
    <div class="box">
        <h3>MY ORDERS</h3>
        {% for o in my %}<div style="border-bottom:1px solid #ddd; padding:5px;">
            <p>{{ o.item }} - <span class="status {{ o.status.lower() }}">{{ o.status }}</span></p>
        </div>
        {% else %}<p>No orders found.</p>{% endfor %}
        <br><a href="/" class="btn" style="background:black">BACK TO SHOP</a>
    </div>
    {% endblock %}
    """, my=my_orders)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['u'] == ADMIN_U and request.form['p'] == ADMIN_P:
            session['user'] = "Admin"
            session['is_admin'] = True
            return redirect('/')
    return render_template_string(BASE_HTML + """
    {% block content %}
    <div class="box" style="text-align:center;">
        <h3>ADMIN ACCESS</h3>
        <form method="post">
            <input name="u" placeholder="Admin Username" required><br>
            <input name="p" type="password" placeholder="Password" required><br><br>
            <button type="submit" class="btn" style="background:black">LOGIN</button>
        </form>
    </div>
    {% endblock %}
    """)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/add_product', methods=['POST'])
def add_product():
    if session.get('is_admin'):
        products.append({'name': request.form['name'], 'price': request.form['price'], 'image': request.form['img']})
    return redirect('/')

@app.route('/update_status/<int:o_id>', methods=['POST'])
def update_status(o_id):
    if session.get('is_admin') and o_id < len(orders):
        orders[o_id]['status'] = request.form['st']
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
