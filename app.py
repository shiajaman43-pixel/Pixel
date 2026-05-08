from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# Data storage (Temporary)
products = []
orders = []

# HTML Design (Single file e rakhar jonno)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>PixelUltra Store</title>
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Press Start 2P', cursive; background: #fdfae6; padding: 20px; font-size: 10px; line-height: 1.6; }
        .box { border: 4px solid #000; background: white; padding: 20px; margin-bottom: 20px; box-shadow: 6px 6px 0px #000; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 15px; }
        .card { border: 3px solid #333; padding: 10px; text-align: center; background: #fff; }
        .card img { width: 80px; height: 80px; object-fit: contain; image-rendering: pixelated; }
        button { font-family: 'Press Start 2P'; cursor: pointer; background: #ff4757; color: white; border: 3px solid #000; padding: 8px; font-size: 8px; }
        input { font-family: 'Press Start 2P'; padding: 8px; margin: 5px 0; width: 80%; font-size: 8px; border: 2px solid #000; }
        h1 { background: #2f3542; color: white; padding: 10px; display: block; text-align: center; font-size: 14px; margin-top: 0; }
        .order-box { background: #eccc68; padding: 10px; border: 2px dashed #000; margin-top: 10px; }
    </style>
</head>
<body>
    <h1>PIXELULTRA STATIONARY</h1>

    <div class="box">
        <h3>[+] ADMIN: ADD PRODUCT</h3>
        <form action="/add_product" method="post">
            <input type="text" name="name" placeholder="Item Name" required><br>
            <input type="text" name="price" placeholder="Price (BDT)" required><br>
            <input type="text" name="img_url" placeholder="Direct Image URL" required><br>
            <button type="submit">POST TO SHOP</button>
        </form>
    </div>

    <div class="box">
        <h3>[*] SHOP GALLERY</h3>
        <div class="grid">
            {% for i in range(products|length) %}
            <div class="card">
                <img src="{{ products[i].image }}">
                <p>{{ products[i].name }}</p>
                <p>{{ products[i].price }} BDT</p>
                <a href="/place_order/{{ i }}"><button>ORDER</button></a>
            </div>
            {% endfor %}
        </div>
    </div>

    <div class="box">
        <h3>[!] INCOMING ORDERS</h3>
        {% for order in orders %}
        <div class="order-box">
            NEW ORDER: {{ order.item }} <br> STATUS: <span style="color:red;">{{ order.status }}</span>
        </div>
        {% else %}
        <p>No orders yet.</p>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, products=products, orders=orders)

@app.route('/add_product', methods=['POST'])
def add_product():
    name = request.form.get('name')
    price = request.form.get('price')
    img_url = request.form.get('img_url')
    if name and price and img_url:
        products.append({'name': name, 'price': price, 'image': img_url})
    return redirect(url_for('home'))

@app.route('/place_order/<int:product_id>')
def place_order(product_id):
    if 0 <= product_id < len(products):
        product = products[product_id]
        orders.append({'item': product['name'], 'status': 'Pending'})
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
