from flask import Flask, render_template_string, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "pixel_ultra_final_v7_no_errors"

# --- CONFIG ---
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER): os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'shop_final.db')
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
    user_phone = db.Column(db.String(15))
    items_list = db.Column(db.Text)
    total = db.Column(db.Integer)
    status = db.Column(db.String(20), default="Pending")
    addr = db.Column(db.Text)

with app.app_context():
    db.create_all()
    if not User.query.filter_by(phone="01700000000").first():
        db.session.add(User(phone="01700000000", name="Admin", password=generate_password_hash("admin123"), is_admin=True))
        db.session.commit()

# --- CSS STYLING ---
STYLE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&family=Press+Start+2P&display=swap');
    :root { --main: #ff4757; --accent: #2ed573; --dark: #2d3436; }
    body { font-family: 'VT323', monospace; background: #f1f2f6; margin: 0; padding-bottom: 70px; font-size: 18px; }
    .pixel { font-family: 'Press Start 2P', cursive; font-size: 9px; }
    .header { background: var(--dark); color: white; padding: 15px; display: flex; justify-content: space-between; border-bottom: 4px solid var(--main); position: sticky; top:0; z-index:100; }
    .card { background: white; border: 3px solid #000; padding: 12px; margin-bottom: 15px; box-shadow: 4px 4px 0px #000; }
    .btn { padding: 8px 12px; border: 2px solid #000; cursor: pointer; text-decoration: none; display: inline-block; font-family: 'Press Start 2P'; font-size: 7px; color: white; margin: 2px; text-align: center; }
    .btn-main { background: var(--main); } .btn-accent { background: var(--accent); } .btn-blue { background: #3498db; } .btn-dark { background: #57606f; }
    input, textarea, select { width: 100%; padding: 10px; margin: 8px 0; border: 2px solid #000; box-sizing: border-box; font-family: 'VT323'; font-size: 18px; }
    .bottom-nav { background: var(--dark); position: fixed; bottom: 0; width: 100%; display: flex; justify-content: space-around; padding: 12px 0; border-top: 3px solid var(--main); z-index:100; }
    .bottom-nav a { color: white; text-decoration: none; font-size: 11px; }
    .st-Pending { color: #f39c12; } .st-Packaging { color: #3498db; } .st-Delivered { color: #2ecc71; } .st-Cancelled { color: #e74c3c; }
</style>
"""

def wrap(content):
    cart_len = len(session.get('cart', []))
    admin_link = '<a href="/admin">DB</a>' if session.get('is_admin') else ''
    return render_template_string(f"""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1.0">{STYLE}</head><body>
    <div class="header"><div class="pixel">PIXELULTRA</div></div>
    <div style="padding: 15px;">{content}</div>
    <div class="bottom-nav pixel"><a href="/">HOME</a><a href="/cart">BAG({cart_len})</a><a href="/login">USER</a>{admin_link}</div>
    </body></html>""")

# --- ROUTES ---

@app.route('/')
def home():
    prods = Product.query.all()
    html = '<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">'
    for p in prods:
        html += f"""<div class="card" style="text-align:center;">
            <a href="/product/{p.id}"><img src="{p.image}" style="width:100%; height:100px; object-fit:contain;"></a>
            <p class="pixel" style="font-size:7px; margin:5px 0;">{p.name}</p>
            <p style="color:var(--main);">{p.price} BDT</p>
            <a href="/add_to_cart/{p.id}" class="btn btn-main" style="width:90%;">+ BAG</a>
        </div>"""
    html += '</div>'
    return wrap(html if prods else "<p>No products available.</p>")

@app.route('/product/<int:id>')
def details(id):
    p = Product.query.get(id)
    content = f"""<div class='card' style='text-align:center;'>
        <img src='{p.image}' style='width:100%; max-height:300px; object-fit:contain;'>
        <h2 class='pixel'>{p.name}</h2>
        <p style='background:#f9f9f9; padding:10px; border:1px solid #ddd;'>{p.desc}</p>
        <h2 style='color:var(--main);'>{p.price} BDT</h2>
        <p class='pixel' style='color:blue;'>Status: {p.stock}</p>
        <a href='/add_to_cart/{p.id}' class='btn btn-accent' style='width:100%; box-sizing:border-box;'>ADD TO SHOPPING BAG</a>
    </div>"""
    return wrap(content)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return wrap(f"<div class='card'><h3 class='pixel'>HI, {session.get('u_name')}</h3><p>Phone: {session.get('u_phone')}</p><a href='/logout' class='btn btn-main'>LOGOUT</a></div>")
    if request.method == 'POST':
        u = User.query.filter_by(phone=request.form['phone']).first()
        if u and check_password_hash(u.password, request.form['password']):
            session['user_id'], session['is_admin'], session['u_phone'], session['u_name'] = u.id, u.is_admin, u.phone, u.name
            return redirect('/')
    return wrap("<div class='card'><h2 class='pixel'>LOGIN</h2><form method='post'><input name='phone' placeholder='Phone Number'><input name='password' type='password' placeholder='Password'><button class='btn btn-main' style='width:100%'>ENTER STORE</button></form><p>New customer? <a href='/register'>Register Here</a></p></div>")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        db.session.add(User(phone=request.form['phone'], name=request.form['name'], password=generate_password_hash(request.form['password'])))
        db.session.commit(); return redirect('/login')
    return wrap("<div class='card'><h2 class='pixel'>REGISTER</h2><form method='post'><input name='name' placeholder='Your Name'><input name='phone' placeholder='Phone Number'><input name='password' type='password' placeholder='Create Password'><button class='btn btn-accent' style='width:100%'>SIGN UP</button></form></div>")

@app.route('/cart')
def cart():
    items = session.get('cart', [])
    total = sum(i['price'] for i in items)
    
    status_section = ""
    if 'user_id' in session:
        my_orders = Order.query.filter_by(user_id=session['user_id']).order_by(Order.id.desc()).all()
        if my_orders:
            status_section = "<div class='card' style='background:#f0f0f0;'><h3 class='pixel'>MY ORDERS</h3>"
            for o in my_orders:
                status_section += f"<p style='font-size:14px; margin:5px 0;'>Order #{o.id}: <b class='st-{o.status}'>{o.status}</b></p>"
            status_section += "</div>"

    bag_items = "".join([f"<p style='border-bottom:1px solid #eee; padding:5px 0;'>+ {i['name']} ({i['price']} BDT)</p>" for i in items])
    
    checkout_form = ""
    if items:
        checkout_form = """<form action='/checkout' method='post'><textarea name='addr' placeholder='Delivery Address' required></textarea><button class='btn btn-accent' style='width:100%'>PLACE ORDER</button></form>"""
    
    content = f"""
    {status_section}
    <div class='card'>
        <h2 class='pixel'>MY BAG</h2>
        {bag_items if items else "<p>Your bag is empty.</p>"}
        <hr>
        <h3 style='text-align:right;'>Total: {total} BDT</h3>
        {checkout_form}
    </div>"""
    return wrap(content)

# --- ADMIN ROUTES ---
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('is_admin'): return redirect('/login')
    if request.method == 'POST' and 'add_p' in request.form:
        file = request.files.get('img_file')
        img = '/static/uploads/' + secure_filename(file.filename) if file else request.form['img_url']
        if file: file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        db.session.add(Product(name=request.form['name'], price=request.form['price'], image=img, desc=request.form['desc'], stock=request.form['stock']))
        db.session.commit()

    ords = Order.query.order_by(Order.id.desc()).all()
    prods = Product.query.all()
    
    admin_ui = """<div class='card'><h3 class='pixel'>ADD NEW PRODUCT</h3><form method='post' enctype='multipart/form-data'><input name='name' placeholder='Name'><input name='price' placeholder='Price'><input type='file' name='img_file'><input name='img_url' placeholder='OR Image URL'><textarea name='desc' placeholder='Description'></textarea><select name='stock'><option>In Stock</option><option>Out of Stock</option></select><button name='add_p' class='btn btn-main' style='width:100%'>SAVE PRODUCT</button></form></div>"""
    
    admin_ui += "<h3 class='pixel'>MANAGE ORDERS</h3>"
    for o in ords:
        admin_ui += f"""<div class='card' style='font-size:13px;'>
            <b>#{o.id}</b> | {o.user_phone} | <b class='st-{o.status}'>{o.status}</b><br>
            <div style='margin-top:8px;'>
                <a href='/st/{o.id}/Packaging' class='btn btn-blue'>PACK</a>
                <a href='/st/{o.id}/Delivered' class='btn btn-accent'>DONE</a>
                <a href='/st/{o.id}/Cancelled' class='btn btn-main'>X</a>
                <a href='/del_o/{o.id}' class='btn btn-dark' onclick='return confirm(\"Delete Order?\")'>DEL</a>
            </div>
        </div>"""
    
    admin_ui += "<h3 class='pixel'>ALL PRODUCTS</h3>"
    for p in prods:
        admin_ui += f"<div class='card' style='display:flex; justify-content:space-between; align-items:center;'><span>{p.name}</span> <a href='/del_p/{p.id}' style='color:red;' onclick='return confirm(\"Delete?\")'>DELETE</a></div>"
    
    return wrap(admin_ui)

@app.route('/st/<int:id>/<string:s>')
def update_st(id, s):
    if session.get('is_admin'):
        Order.query.get(id).status = s
        db.session.commit()
    return redirect('/admin')

@app.route('/del_o/<int:id>')
def del_o(id):
    if session.get('is_admin'):
        db.session.delete(Order.query.get(id)); db.session.commit()
    return redirect('/admin')

@app.route('/del_p/<int:id>')
def del_p(id):
    if session.get('is_admin'):
        db.session.delete(Product.query.get(id)); db.session.commit()
    return redirect('/admin')

@app.route('/add_to_cart/<int:id>')
def add_to_cart(id):
    if 'cart' not in session: session['cart'] = []
    p = Product.query.get(id)
    if p.stock == "In Stock":
        session['cart'].append({'id':p.id,'name':p.name,'price':p.price})
        session.modified = True
    return redirect('/cart')

@app.route('/checkout', methods=['POST'])
def checkout():
    if 'user_id' not in session: return redirect('/login')
    items = session.get('cart', [])
    new_o = Order(user_id=session['user_id'], user_phone=session['u_phone'], items_list=str(items), total=sum(i['price'] for i in items), addr=request.form['addr'])
    db.session.add(new_o); db.session.commit(); session['cart'] = []
    return redirect('/cart')

@app.route('/logout')
def logout(): session.clear(); return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
