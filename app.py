from flask import Flask, render_template_string, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "pixel_ultra_pro_ultimate"

# --- FILE UPLOAD CONFIG ---
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- DATABASE ---
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'pixel_premium.db')
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
    items = db.Column(db.Text)
    total = db.Column(db.Integer)
    status = db.Column(db.String(20), default="Pending")
    addr = db.Column(db.Text)

with app.app_context():
    db.create_all()
    if not User.query.filter_by(phone="01700000000").first():
        db.session.add(User(phone="01700000000", name="Admin", password=generate_password_hash("admin123"), is_admin=True))
        db.session.commit()

# --- PREMIUM UI CSS ---
STYLE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap');
    :root { --main: #ff4757; --accent: #2ed573; --dark: #1e272e; --glass: rgba(255,255,255,0.95); }
    body { font-family: 'VT323', monospace; background: #dfe4ea; margin: 0; font-size: 20px; color: var(--dark); }
    .pixel-font { font-family: 'Press Start 2P', cursive; font-size: 10px; }
    .nav { background: var(--dark); color: white; padding: 15px 5%; display: flex; justify-content: space-between; border-bottom: 5px solid var(--main); position: sticky; top:0; z-index:1000; }
    .container { padding: 30px 5%; max-width: 1200px; margin: auto; }
    .card { background: var(--glass); border: 4px solid #000; padding: 20px; box-shadow: 8px 8px 0px #000; margin-bottom: 25px; transition: 0.3s; }
    .card:hover { transform: translate(-3px, -3px); box-shadow: 12px 12px 0px #000; }
    .btn { padding: 12px 20px; border: 3px solid #000; cursor: pointer; text-decoration: none; display: inline-block; font-family: 'Press Start 2P'; font-size: 9px; color: white; margin: 5px; }
    .btn-main { background: var(--main); } .btn-accent { background: var(--accent); } .btn-dark { background: var(--dark); }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 30px; }
    input, textarea, select { width: 100%; padding: 12px; margin: 10px 0; border: 3px solid #000; font-family: 'VT323'; font-size: 22px; }
    .badge { padding: 5px 10px; border: 2px solid #000; font-size: 14px; background: white; font-weight: bold; }
    .status-Pending { background: #ffa502; color: #fff; } .status-Packaging { background: #1e90ff; color: #fff; }
    .status-Delivered { background: #2ed573; color: #fff; } .status-Cancelled { background: #ff4757; color: #fff; }
</style>
"""

# --- LAYOUT HELPER ---
def layout(content):
    cart_len = len(session.get('cart', []))
    admin_link = '<a href="/admin" style="color:#eccc68; margin-right:20px;">DASHBOARD</a>' if session.get('is_admin') else ''
    auth = '<a href="/logout" style="color:#ff7675;">LOGOUT</a>' if 'user_id' in session else '<a href="/login" style="color:#55efc4;">LOGIN</a>'
    return render_template_string(f"""
    <html><head>{STYLE}</head><body>
    <div class="nav"><div class="pixel-font" style="font-size:18px;"><a href="/" style="color:white; text-decoration:none;">PIXELULTRA v3</a></div>
    <div>{admin_link} <a href="/cart" style="color:white; margin-right:20px;">BAG({cart_len})</a> {auth}</div></div>
    <div class="container">{content}</div></body></html>""")

# --- ROUTES ---

@app.route('/')
def home():
    products = Product.query.all()
    html = '<div class="grid">'
    for p in products:
        html += f"""<div class="card" style="text-align:center;">
            <div class="badge" style="float:right;">{p.stock}</div><br>
            <a href="/product/{p.id}"><img src="{p.image}" style="width:100%; height:200px; object-fit:contain; image-rendering:pixelated;"></a>
            <h3 class="pixel-font">{p.name}</h3><p style="color:var(--main); font-weight:bold;">{p.price} BDT</p>
            <a href="/add_to_cart/{p.id}" class="btn btn-main" style="width:90%;">+ ADD</a>
        </div>"""
    html += '</div>'
    return layout(html)

@app.route('/product/<int:id>')
def details(id):
    p = Product.query.get(id)
    return layout(f"""
    <div style="display:flex; flex-wrap:wrap; gap:40px;">
        <div class="card" style="flex:1; min-width:300px; text-align:center;"><img src="{p.image}" style="width:100%; image-rendering:pixelated;"></div>
        <div style="flex:1; min-width:300px;">
            <h1 class="pixel-font" style="font-size:24px;">{p.name}</h1>
            <span class="badge">{p.stock}</span>
            <h2 style="color:var(--main); font-size:40px; margin:20px 0;">{p.price} BDT</h2>
            <div class="card" style="background:#fff;"><p>{p.desc}</p></div>
            <a href="/add_to_cart/{p.id}" class="btn btn-accent" style="font-size:14px; padding:20px;">ADD TO SHOPPING BAG</a>
        </div>
    </div>""")

# --- ADMIN: GALLERY UPLOAD & MANAGEMENT ---
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('is_admin'): return redirect('/login')
    
    if request.method == 'POST':
        if 'add_p' in request.form:
            name, price, desc, stock = request.form['name'], request.form['price'], request.form['desc'], request.form['stock']
            file = request.files['image_file']
            img_path = request.form['image_url']
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                img_path = '/static/uploads/' + filename
            db.session.add(Product(name=name, price=price, image=img_path, desc=desc, stock=stock))
            db.session.commit()
    
    prods, ords = Product.query.all(), Order.query.all()
    html = """<div class="card"><h2 class="pixel-font">ADD PRODUCT</h2><form method="post" enctype="multipart/form-data">
        <input name="name" placeholder="Product Name"><input name="price" placeholder="Price">
        <p>Gallery Upload: <input type="file" name="image_file"></p><input name="image_url" placeholder="OR Image URL">
        <textarea name="desc" placeholder="Product Details"></textarea>
        <select name="stock"><option>In Stock</option><option>Out of Stock</option></select>
        <button name="add_p" class="btn btn-dark" style="width:100%;">SAVE TO DATABASE</button></form></div>"""
    
    html += "<h2 class="pixel-font">MANAGE ORDERS</h2>"
    for o in ords:
        html += f"""<div class="card"><b>Order #{o.id}</b> | User: {o.user_phone} | Items: {o.items}<br>
        Status: <span class="badge status-{o.status}">{o.status}</span><br><br>
        <a href="/status/{o.id}/Packaging" class="btn btn-dark">PACKAGING</a>
        <a href="/status/{o.id}/Delivered" class="btn btn-accent">DELIVERED</a>
        <a href="/status/{o.id}/Cancelled" class="btn btn-main">CANCEL</a></div>"""
        
    html += "<h2 class="pixel-font">PRODUCTS IN STORE</h2><div class='grid'>"
    for p in prods:
        html += f"<div class='card' style='font-size:14px;'>{p.name}<br><a href='/delete/{p.id}' style='color:red;'>DELETE</a></div>"
    html += "</div>"
    return layout(html)

@app.route('/status/<int:id>/<string:st>')
def update_status(id, st):
    if session.get('is_admin'):
        o = Order.query.get(id); o.status = st; db.session.commit()
    return redirect('/admin')

@app.route('/delete/<int:id>')
def delete_product(id):
    if session.get('is_admin'):
        p = Product.query.get(id); db.session.delete(p); db.session.commit()
    return redirect('/admin')

# --- AUTH & CART ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(phone=request.form['phone']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['user_id'], session['is_admin'], session['user_phone'] = user.id, user.is_admin, user.phone
            return redirect('/')
    return layout("<div class='card' style='max-width:400px; margin:auto;'><h2 class='pixel-font'>LOGIN</h2><form method='post'><input name='phone' placeholder='Phone'><input name='password' type='password' placeholder='Pass'><button class='btn btn-dark' style='width:100%'>ENTER</button></form><a href='/register'>Register Here</a></div>")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        u = User(phone=request.form['phone'], name=request.form['name'], password=generate_password_hash(request.form['password']))
        db.session.add(u); db.session.commit(); return redirect('/login')
    return layout("<div class='card' style='max-width:400px; margin:auto;'><h2 class='pixel-font'>REGISTER</h2><form method='post'><input name='name' placeholder='Name'><input name='phone' placeholder='Phone'><input name='password' type='password' placeholder='Pass'><button class='btn btn-accent' style='width:100%'>CREATE</button></form></div>")

@app.route('/add_to_cart/<int:id>')
def add_to_cart(id):
    if 'cart' not in session: session['cart'] = []
    p = Product.query.get(id)
    if p.stock == "Out of Stock": return "Item Out of Stock!"
    session['cart'].append({'id': p.id, 'name': p.name, 'price': p.price}); session.modified = True
    return redirect('/cart')

@app.route('/cart')
def cart():
    items = session.get('cart', [])
    total = sum(i['price'] for i in items)
    html = f"<div class='card' style='max-width:600px; margin:auto;'><h2 class='pixel-font'>SHOPPING BAG</h2>"
    for i in items: html += f"<p>+ {i['name']} ({i['price']} BDT)</p>"
    html += f"<hr><h3>TOTAL: {total} BDT</h3>"
    if items: html += "<form action='/checkout' method='post'><textarea name='addr' placeholder='Full Address' required></textarea><button class='btn btn-accent' style='width:100%'>CONFIRM ORDER</button></form>"
    return layout(html + "</div>")

@app.route('/checkout', methods=['POST'])
def checkout():
    if 'user_id' not in session: return redirect('/login')
    items = session.get('cart', [])
    new_o = Order(user_id=session['user_id'], user_phone=session['user_phone'], items=str([i['name'] for i in items]), total=sum(i['price'] for i in items), addr=request.form['addr'])
    db.session.add(new_o); db.session.commit(); session['cart'] = []
    return layout("<div class='card' style='text-align:center;'><h2>ORDER PLACED!</h2><a href='/' class='btn btn-main'>CONTINUE SHOPPING</a></div>")

@app.route('/logout')
def logout(): session.clear(); return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
