from flask import request, jsonify
from src.models import db
from flask import Blueprint
from src.models.variants_model import VariantsSchema
from src.models.variants_model import Variants

variants_api = Blueprint("variants_api", __name__)

variant_schema = VariantsSchema()
variants_schema = VariantsSchema(many=True)

@variants_api.route("/variants", methods=['POST'])
def add_variant():

    variants = Variants(request.json)
    db.session.add(variants)
    db.session.commit()

    return jsonify(request.json)

@variants_api.route("/variants", methods=['GET'])
def get_variants():
    variants = Variants.query.all()
    result = variants_schema.dump(variants)
    return jsonify(result.data)

@variants_api.route("/variants/<id>", methods=['GET'])
def get_variant(id):
    variants = Variants.query.get(id)
    return variant_schema.jsonify(variants)

@variants_api.route("/variants/<id>", methods=["PUT"])
def update_variant(id):
    variants = Variants.query.get(id)
    for key, value in request.json.items():
        variants.__setattr__(key, value)
    db.session.commit()
    return variant_schema.jsonify(variants)

@variants_api.route("/variants/<id>", methods=["DELETE"])
def delete_variant(id):
    variants = Variants.query.get(id)
    db.session.delete(variants)
    db.session.commit()
    return variant_schema.jsonify(variants)
