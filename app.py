from flask import Flask, render_template_string, request, redirect, url_for, session
import smtplib, random

app = Flask(__name__)
app.secret_key = "pixel_ultra_final_v10_fixed"

# --- CONFIG ---
SENDER_EMAIL = "applegadget07@gmail.com"
SENDER_PASS = "qesd sqzt zpou cccc" 

products = [
    {'name': 'Pixel Pen', 'price': '150', 'image': 'https://img.icons8.com/pixel-line/100/pencil.png'},
    {'name': 'Retro Notebook', 'price': '350', 'image': 'https://img.icons8.com/pixel-line/100/book.png'}
]
orders = []

# --- BASE HTML (No double blocks) ---
BASE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>PixelUltra</title>
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Press Start 2P', cursive; background: #fdfae6; padding: 20px; font-size: 10px; }
        .box { border: 4px solid #000; background: #fff; padding: 15px; margin-bottom: 20px; box-shadow: 5px 5px 0 #000; }
        .btn { font-family: 'Press Start 2P'; padding: 8px; border: 3px solid #000; cursor: pointer; text-decoration: none; display: inline-block; font-size: 8px; margin: 2px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 10px; }
        .card { border: 2px solid #000; padding: 10px; text-align: center; }
        input, textarea { font-family: 'Press Start 2P'; padding: 5px; margin-bottom: 5px; border: 2px solid #000; width: 85%; font-size: 8px; }
    </style>
</head>
<body>
    <div class="box" style="background:#2f3542; color:#fff; text-align:center;">PIXELULTRA STATIONARY</div>
    <div style="margin-bottom:15px;">
        {% if session.get('user') %}
            <span>HI, {{ session['user'].split('@')[0] }}</span> | <a href="/logout">LOGOUT</a>
        {% else %}
            <a href="/login" class="btn" style="background:#4285F4; color:#fff;">GMAIL LOGIN</a>
        {% endif %}
        | <a href="/cart" class="btn" style="background:orange;">BAG ({{ session.get('cart', [])|length }})</a>
    </div>
    {{ content | safe }}
</body>
</html>
"""

@app.route('/')
def home():
    content = f"""
    <div class="box">
        <div class="grid">
            {"".join([f'''
            <div class="card">
                <img src="{p['image']}" width="50">
                <p>{p['name']}<br>{p['price']} BDT</p>
                <a href="/add_to_cart/{idx}" class="btn" style="background:#ff4757; color:#fff;">+ ADD</a>
            </div>
            ''' for idx, p in enumerate(products)])}
        </div>
    </div>
    """
    if session.get('is_admin'):
        content += """
        <div class="box" style="border-color:blue;">
            <h3>ADMIN PANEL</h3>
            <form action="/add_product" method="post">
                <input name="name" placeholder="Name"><br><input name="price" placeholder="Price"><br>
                <input name="img" placeholder="Img URL"><br><button class="btn">POST</button>
            </form>
        </div>
        """
    return render_template_string(BASE_HTML, content=content)

@app.route('/login')
def login():
    content = """
    <div class="box" style="text-align:center;">
        <h3>GMAIL OTP</h3>
        <form action="/send_otp" method="post">
            <input name="email" type="email" placeholder="Gmail Address" required><br><br>
            <button class="btn" style="background:#4285F4; color:#fff;">SEND CODE</button>
        </form>
        <p style="font-size:7px;"><a href="/admin_login">Admin?</a></p>
    </div>
    """
    return render_template_string(BASE_HTML, content=content)

@app.route('/send_otp', methods=['POST'])
def send_otp():
    email = request.form['email']
    otp = str(random.randint(1111, 9999))
    session['temp_email'], session['temp_otp'] = email, otp
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587); server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASS)
        server.sendmail(SENDER_EMAIL, email, f"Subject: OTP Code\\n\\nYour code: {otp}")
        server.quit()
        content = """
        <div class="box" style="text-align:center;">
            <h3>OTP SENT!</h3>
            <form action="/verify_otp" method="post">
                <input name="otp" placeholder="4-digit code"><br><br>
                <button class="btn" style="background:green; color:#fff;">VERIFY</button>
            </form>
        </div>
        """
        return render_template_string(BASE_HTML, content=content)
    except Exception as e:
        return f"Email Error: {e}. Testing OTP: {otp}"

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    if request.form['otp'] == session.get('temp_otp'):
        session['user'], session['is_admin'] = session.get('temp_email'), False
        return redirect('/')
    return "Wrong OTP!"

@app.route('/add_to_cart/<int:p_id>')
def add_to_cart(p_id):
    if 'cart' not in session: session['cart'] = []
    session['cart'].append(products[p_id]); session.modified = True
    return redirect('/')

@app.route('/cart')
def cart():
    items = session.get('cart', [])
    items_list = "".join([f"<p>- {i['name']} ({i['price']} BDT)</p>" for i in items])
    content = f"""
    <div class="box">
        <h3>MY BAG</h3>
        {items_list if items else '<p>Bag is empty!</p>'}
        <hr>
        <form action="/checkout" method="post">
            <input name="phone" placeholder="Phone" required><br>
            <textarea name="addr" placeholder="Full Address" required></textarea><br>
            <button class="btn" style="background:green; color:#fff;">CONFIRM ORDER</button>
        </form>
        <br><a href="/">Back</a>
    </div>
    """
    return render_template_string(BASE_HTML, content=content)

@app.route('/checkout', methods=['POST'])
def checkout():
    if not session.get('user'): return redirect('/login')
    orders.append({'user': session['user'], 'status': 'Pending'})
    session['cart'] = []; return "<h2>ORDER SUCCESSFUL!</h2><a href='/'>Home</a>"

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['u'] == "admin" and request.form['p'] == "123":
            session['user'], session['is_admin'] = "Admin", True
            return redirect('/')
    return '<form method="post" style="padding:50px;"><input name="u"><input name="p" type="password"><button>GO</button></form>'

@app.route('/logout')
def logout():
    session.clear(); return redirect('/')

@app.route('/add_product', methods=['POST'])
def add_product():
    if session.get('is_admin'):
        products.append({'name': request.form['name'], 'price': request.form['price'], 'image': request.form['img']})
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
