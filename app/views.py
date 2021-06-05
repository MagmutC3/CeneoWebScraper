from app import app
from app.models.product import Product
from flask import render_template, redirect, url_for
from os import listdir

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html.jinja')

@app.route('/extract/<product_id>')
def extract(product_id):
    product = Product(product_id)
    product.extract_product()
    product.save_to_json()
    return redirect(url_for('opinions', product_id=product_id))

@app.route('/products')
def products():
    products_list = [product.split('.')[0] for product in listdir("app/products")]
    return render_template('products.html.jinja', products=products_list)

@app.route('/opinions/<product_id>')
def opinions(product_id):
    product = Product(product_id)
    product.read_from_json()
    return render_template('opinions.html.jinja', product=str(product))

@app.route('/charts/<productId>')
def charts(product_id):
    pass

@app.route('/about')
def about():
    pass
