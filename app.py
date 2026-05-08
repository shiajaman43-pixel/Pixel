from flask import Flask, render_template_string, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = "pixel_ultra_premium_exclusive"

# --- DATABASE CONFIG ---
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'pixel_shop.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- MODELS ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    name = db.Column(db.String(100))
    password = db.Column(db.String(200))
    is_admin = db.Column(db.Boolean, default=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    image = db.Column(db.String(300))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    details = db.Column(db.Text)
    total = db.Column(db.Integer)
    status = db.Column(db.String(20), default="Pending")
    address = db.Column(db.Text)

with app.app_context():
    db.create_all()
    # Auto-create Admin (Login: 01700000000 / Pass: admin123)
    if not User.query.filter_by(phone="01700000000").first():
        admin = User(phone="01700000000", name="Main Admin", password=generate_password_hash("admin123"), is_admin=True)
        db.session.add(admin)
        db.session.commit()

# --- PREMIUM UI (CSS) ---
PREMIUM_STYLE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
    :root { --primary: #ff4757; --secondary: #2ed573; --dark: #2f3542; --light: #f1f2f6; --gold: #ffa502; }
    body { font-family: 'Press Start 2P', cursive; background: #fdfae6; color: var(--dark); margin: 0; font-size: 9px; line-height: 1.6; }
    .container { max-width: 900px; margin: auto; padding: 20px; }
    .header { background: var(--dark); color: white; padding: 20px; border-bottom: 6px solid #000; display: flex; justify-content: space-between; align-items: center; }
    .box { background: white; border: 4px solid #000; padding: 15px; margin-bottom: 20px; box-shadow: 8px 8px 0px #000; }
    .btn { padding: 10px 15px; border: 3px solid #000; cursor: pointer; text-decoration: none; display: inline-block; font-size: 8px; color: white; transition: 0.2s; }
    .btn:active { transform: translate(2px, 2px); box-shadow: none; }
    .btn-red { background: var(--primary); } .btn-green { background: var(--secondary); } .btn-blue { background: #1e90ff; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 20px; }
    .product-card { background: white; border: 3px solid #000; padding: 10px; text-align: center; }
    .product-card img { width: 100px; height: 100px; image-rendering: pixelated; object-fit: contain; }
    input, textarea, select { font-family: 'Press Start 2P'; padding: 10px; border: 3px solid #000; margin: 10px 0; width: 90%; font-size: 8px; background: #fff; }
    .nav-bar { background: #eee; padding: 10px; border: 3px solid #000; margin-bottom: 20px; display: flex; gap: 10px; overflow-x: auto; }
    .status-badge { padding: 4px 8px; border: 2px solid #000; font-size: 7px; color: white; }
    .Pending { background: var(--gold); } .Delivered { background: var(--secondary); }
</style>
"""

# --- BASE LAYOUT ---
def layout(content):
    nav = f"""<div class="nav-bar">
        <a href="/" class="btn btn-blue">HOME</a>
        <a href="/cart" class="btn btn-green">BAG ({len(session.get('cart', []))})</a>
        {'<a href="/admin" class="btn" style="background:#000">ADMIN</a>' if session.get('is_admin') else ''}
        {'<a href="/history" class="btn btn-blue">ORDERS</a> <a href="/logout" class="btn btn-red">LOGOUT</a>' if 'user_id' in session else '<a href="/login" class="btn btn-green">LOGIN</a>'}
    </div>"""
    return render_template_string(f"<html><head>{PREMIUM_STYLE}</head><body><div class='header'><span>PIXELULTRA v2.0</span> <span>{session.get('user_name', 'GUEST')}</span></div><div class='container'>{nav}{content}</div></body></html>")

# --- ROUTES ---

@app.route('/')
def home():
    prods = Product.query.all()
    html = '<div class="grid">'
    for p in prods:
        html += f'<div class="product-card"><img src="{p.image}"><h4>{p.name}</h4><p style="color:green">{p.price} BDT</p><a href="/add_to_cart/{p.id}" class="btn btn-red">ADD TO BAG</a></div>'
    html += '</div>'
    if not prods: html = '<div class="box">No products yet! Admin, please add some.</div>'
    return layout(html)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(phone=request.form['phone']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['user_id'], session['user_name'], session['is_admin'] = user.id, user.name, user.is_admin
            return redirect('/')
        return layout("<div class='box'>Wrong credentials! <a href='/login'>Try again</a></div>")
    return layout('<div class="box" style="text-align:center;"><h3>LOGIN</h3><form method="post"><input name="phone" placeholder="PHONE" required><input name="password" type="password" placeholder="PASS" required><br><button class="btn btn-green">ENTER SHOP</button></form><p>New? <a href="/register">Register</a></p></div>')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if User.query.filter_by(phone=request.form['phone']).first(): return "User exists!"
        new_u = User(phone=request.form['phone'], name=request.form['name'], password=generate_password_hash(request.form['password']))
        db.session.add(new_u); db.session.commit()
        return redirect('/login')
    return layout('<div class="box"><h3>REGISTER</h3><form method="post"><input name="name" placeholder="FULL NAME"><input name="phone" placeholder="MOBILE"><input name="password" type="password" placeholder="PASSWORD"><br><button class="btn btn-blue">CREATE ACCOUNT</button></form></div>')

@app.route('/add_to_cart/<int:id>')
def add_to_cart(id):
    if 'cart' not in session: session['cart'] = []
    p = Product.query.get(id)
    session['cart'].append({'id': p.id, 'name': p.name, 'price': p.price})
    session.modified = True
    return redirect('/')

@app.route('/cart')
def cart():
    items = session.get('cart', [])
    total = sum(i['price'] for i in items)
    html = f'<div class="box"><h3>YOUR BAG</h3>'
    for i in items: html += f'<p>+ {i["name"]} - {i["price"]} BDT</p>'
    html += f'<hr><h4>TOTAL: {total} BDT</h4>'
    if items: html += '<form action="/checkout" method="post"><input name="addr" placeholder="DELIVERY ADDRESS" required><br><button class="btn btn-green">ORDER NOW</button></form>'
    html += '</div>'
    return layout(html)

@app.route('/checkout', methods=['POST'])
def checkout():
    if 'user_id' not in session: return redirect('/login')
    items = session.get('cart', [])
    total = sum(i['price'] for i in items)
    details = ", ".join([i['name'] for i in items])
    new_order = Order(user_id=session['user_id'], details=details, total=total, address=request.form['addr'])
    db.session.add(new_order); db.session.commit()
    session['cart'] = []; return layout("<div class='box'><h3>ORDER PLACED!</h3><a href='/history' class='btn btn-blue'>VIEW ORDERS</a></div>")

@app.route('/history')
def history():
    ords = Order.query.filter_by(user_id=session.get('user_id')).all()
    html = '<div class="box"><h3>MY ORDERS</h3>'
    for o in ords: html += f'<div style="border-bottom:2px solid #eee; padding:10px;"><p>{o.details}</p><p>Total: {o.total} BDT | <span class="status-badge {o.status}">{o.status}</span></p></div>'
    html += '</div>'
    return layout(html)

# --- ADMIN PANEL ---
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('is_admin'): return "Access Denied"
    if request.method == 'POST':
        new_p = Product(name=request.form['name'], price=int(request.form['price']), image=request.form['img'])
        db.session.add(new_p); db.session.commit()
    
    ords = Order.query.all()
    prods = Product.query.all()
    html = '<div class="box"><h3>ADD PRODUCT</h3><form method="post"><input name="name" placeholder="Name"><input name="price" placeholder="Price"><input name="img" placeholder="Img URL"><button class="btn btn-blue">ADD</button></form></div>'
    html += '<div class="box"><h3>ALL ORDERS</h3>'
    for o in ords:
        html += f'<div style="border-bottom:1px solid #000; padding:10px;">User ID: {o.user_id} | {o.details} | Status: {o.status} <a href="/update_order/{o.id}" class="btn btn-green" style="font-size:6px;">MARK DELIVERED</a></div>'
    html += '</div>'
    return layout(html)

@app.route('/update_order/<int:id>')
def update_order(id):
    if session.get('is_admin'):
        o = Order.query.get(id); o.status = "Delivered"; db.session.commit()
    return redirect('/admin')

@app.route('/logout')
def logout():
    session.clear(); return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
