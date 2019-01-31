from flask import request, jsonify
from src.models import db
from flask import Blueprint
from src.models.product_variant_model import ProductVariantSchema
from src.models.product_variant_model import ProductVariant

variant_api = Blueprint("variant_api", __name__)

product_schema = ProductVariantSchema()
products_schema = ProductVariantSchema(many=True)

@variant_api.route("/variant", methods=['POST'])
def add_variant():

    product_variant = ProductVariant(request.json)
    db.session.add(product_variant)
    db.session.commit()

    return jsonify(request.json)

@variant_api.route("/variants", methods=['GET'])
def get_variants():
    product_variants = ProductVariant.query.all()
    result = products_schema.dump(product_variants)
    return jsonify(result.data)

@variant_api.route("/variant/<id>", methods=['GET'])
def get_variant(id):
    product_variant = ProductVariant.query.get(id)
    return product_schema.jsonify(product_variant)

@variant_api.route("/variant/<id>", methods=["PUT"])
def update_variant(id):
    product_variant = ProductVariant.query.get(id)
    for key, value in request.json.items():
        product_variant.__setattr__(key, value)
    db.session.commit()
    return product_schema.jsonify(product_variant)

@variant_api.route("/variant/<id>", methods=["DELETE"])
def delete_variant(id):
    product = ProductVariant.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)
