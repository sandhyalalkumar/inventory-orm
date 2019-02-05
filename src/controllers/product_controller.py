from flask import request, jsonify
from src.models import db
from src.models.product_model import Product
from flask import Blueprint
from src.models.product_model import ProductSchema
from src.common.authentication import Auth
from sqlalchemy import exc
from flask import current_app as app

product_api = Blueprint("product_api", __name__)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

@product_api.route("/product", methods=['POST'])
@Auth.auth_required
def add_product():
    product = Product(request.json)
    try:
        db.session.add(product)
        db.session.commit()
    except exc.SQLAlchemyError as ex:
        app.logger.error(ex)
        return "encounterd error adding a product", 404
    return jsonify(request.json), 200

@product_api.route("/products", methods=['GET'])
@Auth.auth_required
def get_products():
    products = Product.query.all()
    if not products:
        return "no products found", 404
    result = products_schema.dump(products)
    return jsonify(result.data), 200

@product_api.route("/product/<id>", methods=['GET'])
@Auth.auth_required
def get_product(id):
    product = Product.query.get(id)
    if not product:
        return "no product found", 404
    return product_schema.jsonify(product), 200

@product_api.route("/product/<id>", methods=["PUT"])
@Auth.auth_required
def update_product(id):
    try:
        product = Product.query.get(id)
        for key, value in request.json.items():
            product.__setattr__(key, value)
        db.session.commit()
    except exc.SQLAlchemyError as ex:
        app.logger.error(ex)
        return "error encountered updating product", 404
    return product_schema.jsonify(product), 200

@product_api.route("/product/<id>", methods=["DELETE"])
@Auth.auth_required
def delete_product(id):
    try:
        product = Product.query.get(id)
        db.session.delete(product)
        db.session.commit()
    except exc.SQLAlchemyError as ex:
        app.logger.error(ex)
        return "error encountered deleting product", 404
    return product_schema.jsonify(product), 200
