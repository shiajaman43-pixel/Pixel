from flask import Flask, render_template_string, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "pixel_ultra_pro_max_v4"

# --- CONFIG & DATABASE ---
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'premium_store.db')
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
    image = db.Column(db.String(500)) # Will store file path or URL
    desc = db.Column(db.Text)
    stock = db.Column(db.String(20), default="In Stock")

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    items = db.Column(db.Text)
    total = db.Column(db.Integer)
    status = db.Column(db.String(20), default="Pending") # Pending, Packaging, Delivered, Cancelled
    addr = db.Column(db.Text)

with app.app_context():
    db.create_all()
    if not User.query.filter_by(phone="01700000000").first():
        db.session.add(User(phone="01700000000", name="Admin", password=generate_password_hash("admin123"), is_admin=True))
        db.session.commit()

# --- PREMIUM CSS ---
STYLE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap');
    :root { --main: #ff4757; --bg: #f8f9fa; --dark: #2d3436; }
    body { font-family: 'VT323', monospace; background: var(--bg); margin: 0; font-size: 18px; }
    .pixel-font { font-family: 'Press Start 2P', cursive; font-size: 10px; }
    .nav { background: var(--dark); color: white; padding: 15px 5%; display: flex; justify-content: space-between; border-bottom: 4px solid var(--main); }
    .btn { padding: 8px 15px; border: 2px solid #000; cursor: pointer; text-decoration: none; display: inline-block; color: white; font-family: 'Press Start 2P'; font-size: 8px; margin: 2px; }
    .btn-red { background: #ff4757; } .btn-green { background: #2ecc71; } .btn-blue { background: #3498db; } .btn-orange { background: #f39c12; } .btn-black { background: #000; }
    .container { padding: 20px 5%; }
    .card { background: white; border: 3px solid #000; padding: 15px; margin-bottom: 20px; box-shadow: 6px 6px 0px #000; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 20px; }
    input, textarea, select { width: 100%; padding: 10px; margin: 10px 0; border: 2px solid #000; font-family: 'VT323'; font-size: 18px; }
    .status-Pending { color: #f39c12; } .status-Packaging { color: #3498db; } .status-Delivered { color: #2ecc71; } .status-Cancelled { color: #e74c3c; }
</style>
"""

# --- UTILS ---
def wrap(content):
    return render_template_string(f"<html><head>{STYLE}</head><body><div class='nav'><div class='pixel-font'><a href='/' style='color:white;'>PIXELULTRA PRO</a></div><div><a href='/cart' style='color:white; margin-right:10px;'>BAG</a>{'<a href=\"/admin\" style=\"color:yellow; margin-right:10px;\">ADMIN</a>' if session.get('is_admin') else ''}<a href='/logout' style='color:#ff7675;'>LOGOUT</a></div></div><div class='container'>{content}</div></body></html>")

# --- ROUTES ---

@app.route('/')
def home():
    prods = Product.query.all()
    html = '<div class="grid">'
    for p in prods:
        html += f'<div class="card"><img src="{p.image}" style="width:100%; height:150px; object-fit:contain;"><h3 class="pixel-font">{p.name}</h3><p>{p.price} BDT</p><a href="/product/{p.id}" class="btn btn-blue">DETAILS</a></div>'
    html += '</div>'
    return wrap(html)

@app.route('/product/<int:id>')
def details(id):
    p = Product.query.get(id)
    return wrap(f"<div class='card'><img src='{p.image}' style='width:300px;'><h1 class='pixel-font'>{p.name}</h1><p>{p.desc}</p><h3>{p.price} BDT ({p.stock})</h3><a href='/add_to_cart/{p.id}' class='btn btn-green'>ADD TO BAG</a></div>")

# --- ADMIN PANEL (Gallery Upload & Order Management) ---
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('is_admin'): return redirect('/login')
    
    if request.method == 'POST':
        if 'add_p' in request.form:
            name, price, desc, stock = request.form['name'], request.form['price'], request.form['desc'], request.form['stock']
            # Gallery Upload Logic
            file = request.files['image_file']
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                img_path = '/static/uploads/' + filename
            else:
                img_path = request.form['image_url']
            
            db.session.add(Product(name=name, price=price, image=img_path, desc=desc, stock=stock))
            db.session.commit()

    prods = Product.query.all()
    ords = Order.query.all()
    
    html = """<div class="card"><h3>ADD PRODUCT</h3><form method="post" enctype="multipart/form-data">
        <input name="name" placeholder="Name"><input name="price" placeholder="Price">
        <p>Upload from Gallery: <input type="file" name="image_file"></p>
        <p>OR Paste URL: <input name="image_url" placeholder="Image URL"></p>
        <textarea name="desc" placeholder="Description"></textarea>
        <select name="stock"><option>In Stock</option><option>Out of Stock</option></select>
        <button name="add_p" class="btn btn-black">SAVE</button></form></div>"""
    
    html += "<h3>MANAGE PRODUCTS</h3><div class='grid'>"
    for p in prods:
        html += f"<div class='card' style='font-size:12px;'>{p.name}<br><a href='/delete_p/{p.id}' class='btn btn-red' style='font-size:6px;'>DELETE</a></div>"
    html += "</div>"
    
    html += "<h3>MANAGE ORDERS</h3>"
    for o in ords:
        html += f"""<div class='card'>Order #{o.id} | Items: {o.items} | <span class='status-{o.status}'>{o.status}</span><br>
        <a href='/update_status/{o.id}/Packaging' class='btn btn-blue'>PACKAGING</a>
        <a href='/update_status/{o.id}/Delivered' class='btn btn-green'>DELIVERED</a>
        <a href='/update_status/{o.id}/Cancelled' class='btn btn-red'>CANCEL</a></div>"""
        
    return wrap(html)

@app.route('/update_status/<int:id>/<string:status>')
def update_status(id, status):
    if session.get('is_admin'):
        o = Order.query.get(id); o.status = status; db.session.commit()
    return redirect('/admin')

@app.route('/delete_p/<int:id>')
def delete_p(id):
    if session.get('is_admin'):
        p = Product.query.get(id); db.session.delete(p); db.session.commit()
    return redirect('/admin')

# --- Baki Login/Cart logic stays same ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(phone=request.form['phone']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['user_id'], session['is_admin'] = user.id, user.is_admin
            return redirect('/')
    return wrap("<form method='post' class='card'><input name='phone' placeholder='Phone'><input name='password' type='password'><button class='btn btn-black'>LOGIN</button></form>")

@app.route('/logout')
def logout(): session.clear(); return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
