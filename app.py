from flask import Flask, render_template_string, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = "pixel_ultra_secure_99"

# --- DATABASE CONFIG (Permanent Storage) ---
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_BIT_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'shop.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- MODELS ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(50))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.String(20))
    image = db.Column(db.String(200))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    item_name = db.Column(db.String(100))
    status = db.Column(db.String(20), default="Pending")

with app.app_context():
    db.create_all()
    # Initial Product if empty
    if not Product.query.first():
        db.session.add(Product(name="Pixel Pen", price="150", image="https://img.icons8.com/pixel-line/100/pencil.png"))
        db.session.commit()

# --- DESIGN ---
BASE_CSS = """
<style>
    body { font-family: 'Press Start 2P', cursive; background: #fdfae6; padding: 20px; font-size: 10px; color: #2f3542; }
    .box { border: 4px solid #000; background: white; padding: 15px; margin-bottom: 20px; box-shadow: 6px 6px 0px #000; }
    .btn { font-family: 'Press Start 2P'; cursor: pointer; background: #ff4757; color: white; border: 3px solid #000; padding: 8px; font-size: 8px; text-decoration: none; display: inline-block; margin: 5px 0; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 15px; }
    .card { border: 3px solid #333; padding: 10px; text-align: center; background: #fff; }
    input { font-family: 'Press Start 2P'; padding: 10px; border: 2px solid #000; margin: 5px 0; width: 85%; font-size: 8px; }
    .nav { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-bottom: 4px solid #000; padding-bottom: 10px; }
</style>
"""

# --- ROUTES ---

@app.route('/')
def home():
    items = Product.query.all()
    return render_template_string(f"""
    <html><head><link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">{BASE_CSS}</head>
    <body>
        <div class="nav">
            <div>PIXELULTRA</div>
            <div>
                {% if session.get('user_id') %}
                    <a href="/history" class="btn" style="background:blue">MY ORDERS</a>
                    <a href="/logout" class="btn" style="background:gray">LOGOUT</a>
                {% else %}
                    <a href="/login" class="btn" style="background:#2ed573">LOGIN / SIGNUP</a>
                {% endif %}
            </div>
        </div>

        <div class="box">
            <h3>[*] SHOP</h3>
            <div class="grid">
                {% for p in items %}
                <div class="card">
                    <img src="{{{{ p.image }}}}" width="60">
                    <p>{{{{ p.name }}}}</p>
                    <p style="color:green">{{{{ p.price }}}} BDT</p>
                    <a href="/add_to_cart/{{{{ p.id }}}}" class="btn">ADD TO BAG</a>
                </div>
                {% endfor %}
            </div>
        </div>
    </body></html>
    """, items=items)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']
        user = User.query.filter_by(phone=phone).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            return redirect('/')
        return "Invalid Credentials! <a href='/login'>Try Again</a>"
    
    return render_template_string(f"""
    <html><head>{BASE_CSS}</head><body style="text-align:center; padding-top:50px;">
        <div class="box" style="display:inline-block; width:300px;">
            <h3>LOGIN</h3>
            <form method="post">
                <input name="phone" placeholder="Phone Number" required>
                <input name="password" type="password" placeholder="Password" required>
                <button type="submit" class="btn" style="background:#2ed573; width:95%">ENTER</button>
            </form>
            <p style="font-size:7px;">New user? <a href="/register">Register Here</a></p>
        </div>
    </body></html>
    """)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        phone = request.form['phone']
        name = request.form['name']
        password = generate_password_hash(request.form['password'])
        
        if User.query.filter_by(phone=phone).first():
            return "Phone already exists! <a href='/register'>Try Again</a>"
        
        new_user = User(phone=phone, name=name, password=password)
        db.session.add(new_user)
        db.session.commit()
        return "Registration Success! <a href='/login'>Login Now</a>"
        
    return render_template_string(f"""
    <html><head>{BASE_CSS}</head><body style="text-align:center; padding-top:50px;">
        <div class="box" style="display:inline-block; width:300px;">
            <h3>REGISTER</h3>
            <form method="post">
                <input name="name" placeholder="Full Name" required>
                <input name="phone" placeholder="Mobile Number" required>
                <input name="password" type="password" placeholder="Create Password" required>
                <button type="submit" class="btn" style="background:#70a1ff; width:95%">SIGN UP</button>
            </form>
        </div>
    </body></html>
    """)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# --- Baki functionality (Cart, History, Admin) Optimized ---
# ... (Cart logic stays same but uses session['user_id']) ...

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
