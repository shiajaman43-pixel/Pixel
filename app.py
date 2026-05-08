from flask import Flask, render_template_string, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = "pixel_ultra_premium_v3"

# --- DATABASE ---
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'store.db')
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
    image = db.Column(db.String(500))
    desc = db.Column(db.Text)
    stock = db.Column(db.String(20), default="In Stock")

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    items = db.Column(db.Text)
    total = db.Column(db.Integer)
    status = db.Column(db.String(20), default="Pending")
    addr = db.Column(db.Text)

with app.app_context():
    db.create_all()
    if not User.query.filter_by(phone="01700000000").first():
        db.session.add(User(phone="01700000000", name="Admin", password=generate_password_hash("admin123"), is_admin=True))
        db.session.commit()

# --- PREMIUM STYLING ---
STYLE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap');
    :root { --main: #ff4757; --bg: #f0f2f5; --glass: rgba(255, 255, 255, 0.9); }
    body { font-family: 'VT323', monospace; background: var(--bg); margin: 0; color: #2d3436; font-size: 20px; }
    .pixel-font { font-family: 'Press Start 2P', cursive; font-size: 10px; }
    .nav { background: #2d3436; color: white; padding: 15px 5%; display: flex; justify-content: space-between; align-items: center; border-bottom: 5px solid var(--main); position: sticky; top: 0; z-index: 100; }
    .card { background: white; border: 3px solid #000; border-radius: 0; transition: 0.3s; padding: 15px; position: relative; overflow: hidden; }
    .card:hover { transform: translateY(-5px); box-shadow: 10px 10px 0px #000; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 25px; padding: 30px 5%; }
    .btn { padding: 10px 20px; border: 3px solid #000; cursor: pointer; text-decoration: none; display: inline-block; background: var(--main); color: white; font-family: 'Press Start 2P'; font-size: 8px; }
    .btn-green { background: #2ecc71; } .btn-dark { background: #2d3436; }
    input, textarea, select { font-family: 'VT323'; width: 100%; padding: 10px; margin: 10px 0; border: 2px solid #000; font-size: 20px; box-sizing: border-box; }
    .badge { padding: 2px 8px; border: 2px solid #000; font-size: 14px; position: absolute; top: 10px; right: 10px; background: #fff; }
    .footer { text-align: center; padding: 40px; background: #2d3436; color: white; margin-top: 50px; }
</style>
"""

# --- UTILS ---
def wrap(content):
    cart_count = len(session.get('cart', []))
    admin_btn = '<a href="/admin" style="color:yellow; margin-right:15px;">ADMIN</a>' if session.get('is_admin') else ''
    auth_btn = '<a href="/logout" style="color:#ff7675;">LOGOUT</a>' if 'user_id' in session else '<a href="/login" style="color:#55efc4;">LOGIN</a>'
    return render_template_string(f"""
    <html><head>{STYLE}</head><body>
    <div class="nav">
        <div class="pixel-font" style="font-size:16px;"><a href="/" style="color:white; text-decoration:none;">PIXELULTRA</a></div>
        <div>
            {admin_btn}
            <a href="/cart" style="color:white; margin-right:15px;">BAG({cart_count})</a>
            {auth_btn}
        </div>
    </div>
    <div style="min-height: 80vh;">{content}</div>
    <div class="footer pixel-font">DESIGNED FOR PIXEL ART ENTHUSIASTS © 2026</div>
    </body></html>""")

# --- ROUTES ---

@app.route('/')
def home():
    prods = Product.query.all()
    html = '<div class="grid">'
    for p in prods:
        stock_color = "green" if p.stock == "In Stock" else "red"
        html += f"""
        <div class="card">
            <div class="badge" style="color:{stock_color}">{p.stock}</div>
            <a href="/product/{p.id}"><img src="{p.image}" style="width:100%; height:180px; object-fit:contain; image-rendering:pixelated;"></a>
            <h3 style="margin:10px 0;">{p.name}</h3>
            <p style="color:var(--main); font-weight:bold;">{p.price} BDT</p>
            <a href="/add_to_cart/{p.id}" class="btn" style="width:100%; box-sizing:border-box; text-align:center;">+ ADD TO BAG</a>
        </div>"""
    html += '</div>'
    return wrap(html)

@app.route('/product/<int:id>')
def details(id):
    p = Product.query.get(id)
    html = f"""
    <div style="display:flex; flex-wrap:wrap; padding:50px 5%; gap:40px;">
        <div style="flex:1; min-width:300px;" class="box">
            <img src="{p.image}" style="width:100%; image-rendering:pixelated; border:4px solid #000;">
        </div>
        <div style="flex:1; min-width:300px;">
            <h1 class="pixel-font">{p.name}</h1>
            <p class="badge" style="position:static; display:inline-block;">{p.stock}</p>
            <h2 style="color:var(--main);">{p.price} BDT</h2>
            <p style="background:#fff; padding:20px; border:3px solid #000;">{p.desc}</p>
            <a href="/add_to_cart/{p.id}" class="btn btn-green" style="font-size:14px; padding:15px 30px;">ADD TO SHOPPING BAG</a>
        </div>
    </div>"""
    return wrap(html)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(phone=request.form['phone']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['user_id'], session['is_admin'], session['user_name'] = user.id, user.is_admin, user.name
            return redirect('/')
        return "Login Failed"
    return wrap('<div style="max-width:400px; margin:100px auto;" class="card"><h2 class="pixel-font">LOGIN</h2><form method="post"><input name="phone" placeholder="Phone Number"><input name="password" type="password" placeholder="Password"><button class="btn btn-dark" style="width:100%">ENTER STORE</button></form><p>New? <a href="/register">Register</a></p></div>')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_u = User(phone=request.form['phone'], name=request.form['name'], password=generate_password_hash(request.form['password']))
        db.session.add(new_u); db.session.commit()
        return redirect('/login')
    return wrap('<div style="max-width:400px; margin:100px auto;" class="card"><h2 class="pixel-font">REGISTER</h2><form method="post"><input name="name" placeholder="Full Name"><input name="phone" placeholder="Mobile Number"><input name="password" type="password" placeholder="Password"><button class="btn btn-green" style="width:100%">CREATE ACCOUNT</button></form></div>')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('is_admin'): return "Access Denied"
    if request.method == 'POST' and 'add_p' in request.form:
        p = Product(name=request.form['name'], price=request.form['price'], image=request.form['img'], desc=request.form['desc'], stock=request.form['stock'])
        db.session.add(p); db.session.commit()
    
    prods = Product.query.all()
    ords = Order.query.all()
    html = f"""
    <div style="padding:20px 5%;">
        <div class="card" style="margin-bottom:40px;">
            <h2 class="pixel-font">ADD NEW PRODUCT</h2>
            <form method="post">
                <input name="name" placeholder="Product Name" required>
                <input name="price" placeholder="Price" required>
                <input name="img" placeholder="Image Link (Direct URL from ImgBB)" required>
                <textarea name="desc" placeholder="Product Description"></textarea>
                <select name="stock"><option value="In Stock">In Stock</option><option value="Out of Stock">Out of Stock</option></select>
                <button name="add_p" class="btn btn-dark">SAVE PRODUCT</button>
            </form>
        </div>
        <h2 class="pixel-font">MANAGE ORDERS</h2>
        {"".join([f'<div class="card" style="margin-bottom:10px;">ID: {o.id} | {o.items} | <b>{o.status}</b> <a href="/ship/{o.id}" class="btn-green btn" style="float:right">MARK SHIPPED</a></div>' for o in ords])}
    </div>"""
    return wrap(html)

@app.route('/add_to_cart/<int:id>')
def add_to_cart(id):
    if 'cart' not in session: session['cart'] = []
    p = Product.query.get(id)
    if p.stock == "Out of Stock": return "Sorry, item is out of stock!"
    session['cart'].append({'id': p.id, 'name': p.name, 'price': p.price})
    session.modified = True
    return redirect('/cart')

@app.route('/cart')
def cart():
    items = session.get('cart', [])
    total = sum(i['price'] for i in items)
    items_html = "".join([f"<p>+ {i['name']} - {i['price']} BDT</p>" for i in items])
    html = f"""<div style="max-width:600px; margin:50px auto;" class="card">
        <h2 class="pixel-font">YOUR BAG</h2>
        {items_html if items else "<p>Bag is empty</p>"}
        <hr><h3>TOTAL: {total} BDT</h3>
        <form action="/checkout" method="post"><textarea name="addr" placeholder="Your Delivery Address" required></textarea><button class="btn btn-green" style="width:100%">PLACE ORDER</button></form>
    </div>"""
    return wrap(html)

@app.route('/checkout', methods=['POST'])
def checkout():
    if 'user_id' not in session: return redirect('/login')
    items = session.get('cart', [])
    new_o = Order(user_id=session['user_id'], items=str([i['name'] for i in items]), total=sum(i['price'] for i in items), addr=request.form['addr'])
    db.session.add(new_o); db.session.commit()
    session['cart'] = []; return wrap("<div class='card' style='text-align:center; margin:100px auto; max-width:400px;'><h2>SUCCESS!</h2><p>Order Placed Successfully.</p><a href='/' class='btn'>CONTINUE SHOPPING</a></div>")

@app.route('/ship/<int:id>')
def ship(id):
    if session.get('is_admin'):
        o = Order.query.get(id); o.status = "Shipped"; db.session.commit()
    return redirect('/admin')

@app.route('/logout')
def logout():
    session.clear(); return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
  
