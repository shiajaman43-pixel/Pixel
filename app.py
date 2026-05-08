from flask import Flask, render_template_string, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "pixel_ultra_premium_v99"

# --- CONFIG ---
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'store_v2.db')
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

# --- CSS (Premium Pixel Art) ---
STYLE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap');
    :root { --main: #ff4757; --accent: #2ed573; --dark: #1e272e; }
    body { font-family: 'VT323', monospace; background: #dfe4ea; margin: 0; font-size: 20px; color: var(--dark); }
    .pixel { font-family: 'Press Start 2P', cursive; font-size: 10px; }
    .nav { background: var(--dark); color: white; padding: 15px 5%; display: flex; justify-content: space-between; border-bottom: 5px solid var(--main); position: sticky; top:0; z-index:100; }
    .card { background: white; border: 4px solid #000; padding: 20px; box-shadow: 6px 6px 0px #000; margin-bottom: 20px; transition: 0.2s; }
    .card:hover { transform: translate(-2px, -2px); box-shadow: 10px 10px 0px #000; }
    .btn { padding: 10px 15px; border: 3px solid #000; cursor: pointer; text-decoration: none; display: inline-block; font-family: 'Press Start 2P'; font-size: 8px; color: white; margin: 5px; }
    .btn-main { background: var(--main); } .btn-accent { background: var(--accent); } .btn-dark { background: var(--dark); }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 25px; padding: 20px; }
    input, textarea, select { width: 100%; padding: 10px; margin: 5px 0; border: 2px solid #000; font-family: 'VT323'; font-size: 20px; box-sizing: border-box; }
    .badge { padding: 3px 8px; border: 2px solid #000; font-size: 14px; background: white; }
    .st-Pending { background: #ffa502; color: #fff; } .st-Packaging { background: #1e90ff; color: #fff; }
    .st-Delivered { background: #2ed573; color: #fff; } .st-Cancelled { background: #ff4757; color: #fff; }
</style>
"""

def wrap(content):
    cart_len = len(session.get('cart', []))
    admin_btn = '<a href="/admin" style="color:yellow; margin-right:15px;">ADMIN</a>' if session.get('is_admin') else ''
    auth_btn = '<a href="/logout" style="color:#ff7675;">LOGOUT</a>' if 'user_id' in session else '<a href="/login" style="color:#55efc4;">LOGIN</a>'
    return render_template_string(f"""
    <html><head>{STYLE}</head><body>
    <div class="nav">
        <div class="pixel" style="font-size:16px;"><a href="/" style="color:white; text-decoration:none;">PIXELULTRA</a></div>
        <div>{admin_btn} <a href="/cart" style="color:white; margin-right:15px;">BAG({cart_len})</a> {auth_btn}</div>
    </div>
    <div style="padding: 20px 5%;">{content}</div>
    </body></html>""")

# --- ROUTES ---

@app.route('/')
def home():
    products = Product.query.all()
    html = '<div class="grid">'
    for p in products:
        html += f"""<div class="card" style="text-align:center;">
            <div class="badge" style="float:right;">{p.stock}</div><br>
            <a href="/product/{p.id}"><img src="{p.image}" style="width:100%; height:150px; object-fit:contain;"></a>
            <h3 class="pixel">{p.name}</h3><p style="color:var(--main);">{p.price} BDT</p>
            <a href="/add_to_cart/{p.id}" class="btn btn-main" style="width:100%; box-sizing:border-box;">+ BAG</a>
        </div>"""
    html += '</div>'
    return wrap(html)

@app.route('/product/<int:id>')
def details(id):
    p = Product.query.get(id)
    html = f"""<div style="display:flex; flex-wrap:wrap; gap:30px;">
        <div class="card" style="flex:1; min-width:300px;"><img src="{p.image}" style="width:100%;"></div>
        <div style="flex:1; min-width:300px;">
            <h1 class="pixel">{p.name}</h1><span class="badge">{p.stock}</span>
            <h2 style="color:var(--main); font-size:35px;">{p.price} BDT</h2>
            <div class="card" style="font-size:22px;">{p.desc}</div>
            <a href="/add_to_cart/{p.id}" class="btn btn-accent" style="font-size:12px; padding:15px;">ADD TO BAG</a>
        </div>
    </div>"""
    return wrap(html)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('is_admin'): return redirect('/login')
    
    if request.method == 'POST' and 'add_p' in request.form:
        name, price, desc, stock = request.form['name'], request.form['price'], request.form['desc'], request.form['stock']
        file = request.files.get('image_file')
        img_url = request.form.get('image_url')
        
        if file and file.filename != '':
            fname = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
            img_url = '/static/uploads/' + fname
            
        db.session.add(Product(name=name, price=price, image=img_url, desc=desc, stock=stock))
        db.session.commit()
        return redirect('/admin')

    prods, ords = Product.query.all(), Order.query.all()
    
    admin_html = """<div class="card"><h2 class="pixel">ADD PRODUCT</h2><form method="post" enctype="multipart/form-data">
        <input name="name" placeholder="Name"><input name="price" placeholder="Price">
        <p>Gallery: <input type="file" name="image_file"></p><input name="image_url" placeholder="OR Paste URL">
        <textarea name="desc" placeholder="Details"></textarea>
        <select name="stock"><option>In Stock</option><option>Out of Stock</option></select>
        <button name="add_p" class="btn btn-dark" style="width:100%;">SAVE PRODUCT</button></form></div>"""
    
    admin_html += "<h2 class='pixel'>ORDERS</h2>"
    for o in ords:
        admin_html += f"""<div class="card"><b>Order #{o.id}</b> | {o.user_phone} | <span class="badge st-{o.status}">{o.status}</span><br><br>
        <a href="/st/{o.id}/Packaging" class="btn btn-dark">PACKING</a>
        <a href="/st/{o.id}/Delivered" class="btn btn-accent">DELIVERED</a>
        <a href="/st/{o.id}/Cancelled" class="btn btn-main">CANCEL</a></div>"""
        
    admin_html += "<h2 class='pixel'>STOCK</h2><div class='grid'>"
    for p in prods:
        admin_html += f"<div class='card' style='font-size:14px;'>{p.name}<br><a href='/del/{p.id}' style='color:red;'>DELETE</a></div>"
    admin_html += "</div>"
    return wrap(admin_html)

@app.route('/st/<int:id>/<string:s>')
def update_st(id, s):
    if session.get('is_admin'):
        Order.query.get(id).status = s; db.session.commit()
    return redirect('/admin')

@app.route('/del/<int:id>')
def del_p(id):
    if session.get('is_admin'):
        db.session.delete(Product.query.get(id)); db.session.commit()
    return redirect('/admin')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = User.query.filter_by(phone=request.form['phone']).first()
        if u and check_password_hash(u.password, request.form['password']):
            session['user_id'], session['is_admin'], session['u_phone'] = u.id, u.is_admin, u.phone
            return redirect('/')
    return wrap("<div class='card' style='max-width:400px; margin:auto;'><h2 class='pixel'>LOGIN</h2><form method='post'><input name='phone' placeholder='Phone'><input name='password' type='password'><button class='btn btn-dark' style='width:100%'>ENTER</button></form></div>")

@app.route('/add_to_cart/<int:id>')
def add_to_cart(id):
    if 'cart' not in session: session['cart'] = []
    p = Product.query.get(id)
    if p.stock == "In Stock":
        session['cart'].append({'id': p.id, 'name': p.name, 'price': p.price}); session.modified = True
    return redirect('/cart')

@app.route('/cart')
def cart():
    items = session.get('cart', [])
    total = sum(i['price'] for i in items)
    html = f"<div class='card' style='max-width:600px; margin:auto;'><h2 class='pixel'>BAG</h2>"
    for i in items: html += f"<p>+ {i['name']} ({i['price']} BDT)</p>"
    html += f"<h3>TOTAL: {total} BDT</h3>"
    if items: html += "<form action='/checkout' method='post'><textarea name='addr' placeholder='Address' required></textarea><button class='btn btn-accent' style='width:100%'>ORDER</button></form>"
    return wrap(html + "</div>")

@app.route('/checkout', methods=['POST'])
def checkout():
    if 'user_id' not in session: return redirect('/login')
    items = session.get('cart', [])
    new_o = Order(user_id=session['user_id'], user_phone=session['u_phone'], items_list=str(items), total=sum(i['price'] for i in items), addr=request.form['addr'])
    db.session.add(new_o); db.session.commit(); session['cart'] = []
    return wrap("<div class='card' style='text-align:center;'><h2>ORDER PLACED!</h2><a href='/'>CONTINUE</a></div>")

@app.route('/logout')
def logout(): session.clear(); return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
