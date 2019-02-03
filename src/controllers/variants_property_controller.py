from flask import request, jsonify
from src.models import db
from flask import Blueprint
from src.models.variants_property_model import  VariantsPropertySchema
from src.models.variants_property_model import VariantsProperty

variants_property_api = Blueprint("variants_property_api", __name__)

variants_property_schema = VariantsPropertySchema()
variantss_property_schema = VariantsPropertySchema(many=True)

@variants_property_api.route("/properties", methods=['POST'])
def add_variant():

    variants_property = VariantsProperty(request.json)
    db.session.add(variants_property)
    db.session.commit()

    return jsonify(request.json)

@variants_property_api.route("/properties", methods=['GET'])
def get_variants():
    variants_properties = VariantsProperty.query.all()
    result = variantss_property_schema.dump(variants_properties)
    return jsonify(result.data)

@variants_property_api.route("/properties/<id>", methods=['GET'])
def get_variant(id):
    variants_property = VariantsProperty.query.get(id)
    return variants_property_schema.jsonify(variants_property)

@variants_property_api.route("/properties/<id>", methods=["PUT"])
def update_variant(id):
    variants_property = VariantsProperty.query.get(id)
    for key, value in request.json.items():
        variants_property.__setattr__(key, value)
    db.session.commit()
    return variants_property_schema.jsonify(variants_property)

@variants_property_api.route("/properties/<id>", methods=["DELETE"])
def delete_variant(id):
    variants_property = VariantsProperty.query.get(id)
    db.session.delete(variants_property)
    db.session.commit()
    return variants_property_schema.jsonify(variants_property)
