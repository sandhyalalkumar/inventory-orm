from flask import request, jsonify
from src.models import db
from src.models.product_model import Product
from flask import Blueprint
from src.models.product_model import ProductSchema

product_api = Blueprint("product_api", __name__)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

@product_api.route("/product", methods=['POST'])
def add_product():

    product = Product(request.json)
    db.session.add(product)
    db.session.commit()

    return jsonify(request.json)

@product_api.route("/products", methods=['GET'])
def get_products():
    products = Product.query.all()
    result = products_schema.dump(products)
    return jsonify(result.data)

@product_api.route("/product/<id>", methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

@product_api.route("/product/<id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get(id)
    for key, value in request.json.items():
        product.__setattr__(key, value)
    db.session.commit()
    return product_schema.jsonify(product)

@product_api.route("/product/<id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)
