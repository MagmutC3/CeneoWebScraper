from app import app
from app.models.product import Product
from flask import render_template, redirect, url_for, request
from os import listdir
import json
from flask.helpers import send_file

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html.jinja')

@app.route('/extract', methods=['GET', 'POST'])
def extract():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        product = Product(product_id)
        product.extract_product()
        if product.product_name == "empty_product_name":
            return render_template('extract_error.html.jinja')
        product.save_to_json()
        product.save_stats_file()
        return redirect(url_for('opinions', product_id=product_id))
    return render_template('extract.html.jinja')

@app.route('/products')
def products():
    products_list = [product.split('.')[0] for product in listdir("app/products")]
    product_stats = {}
    for stat_file in listdir("app/products_stats"):
        with open(f"app/products_stats/{stat_file}") as file:
            data = file.read()
            product_stats[f"{stat_file.split('_')[0]}"] = json.loads(data)
    return render_template('products.html.jinja', products = products_list, stats = product_stats)

@app.route('/download/<file_name>')
def download_json(file_name):
    path = app.root_path + "/products/" + file_name + ".json"
    return send_file(path, as_attachment=True)

@app.route('/opinions/<product_id>')
def opinions(product_id):
    print(product_id)
    product = Product(product_id)
    print(", ".join(op.opinion_id for op in product.opinions))
    product.read_from_json()
    return render_template('opinions.html.jinja', product=str(product))

@app.route('/charts/<productId>')
def charts(product_id):
    pass

@app.route('/about')
def about():
    return render_template('about.html.jinja')
