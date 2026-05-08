from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Dummy Database (Shuru korar jonno simple list bebohar kora hoyeche)
products = []
orders = []

@app.route('/')
def home():
    return render_template('index.html', products=products, orders=orders)

@app.route('/add_product', methods=['POST'])
def add_product():
    name = request.form.get('name')
    price = request.form.get('price')
    img_url = request.form.get('img_url')
    if name and price:
        products.append({'name': name, 'price': price, 'image': img_url})
    return redirect(url_for('home'))

@app.route('/place_order/<int:product_id>')
def place_order(product_id):
    product = products[product_id]
    orders.append({'item': product['name'], 'status': 'Pending'})
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
