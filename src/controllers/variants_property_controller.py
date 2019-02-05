from flask import request, jsonify
from src.models import db
from flask import Blueprint
from src.models.variants_property_model import  VariantsPropertySchema
from src.models.variants_property_model import VariantsProperty
from sqlalchemy import exc
from flask import current_app as app
from src.common.authentication import Auth

variants_property_api = Blueprint("variants_property_api", __name__)

variants_property_schema = VariantsPropertySchema()
variantss_property_schema = VariantsPropertySchema(many=True)

@variants_property_api.route("/properties", methods=['POST'])
@Auth.auth_required
def add_variants_property():
    variants_property = VariantsProperty(request.json)
    try:
        db.session.add(variants_property)
        db.session.commit()
    except exc.SQLAlchemyError as ex:
        app.logger.error(ex)
        return "failed to add variants property", 404
    return jsonify(request.json), 200

@variants_property_api.route("/properties/many", methods=['POST'])
@Auth.auth_required
def add_variants_properties():
    variants_properties = []
    try:
        for p in request.json:
            variants_properties.append(VariantsProperty(p))
        db.session.add_all(variants_properties)
        db.session.commit()
    except exc.SQLAlchemyError as ex:
        app.logger.error(ex)
        return "failed to add variants properties(many)", 404
    return jsonify(request.json), 200

@variants_property_api.route("/properties", methods=['GET'])
@Auth.auth_required
def get_variants_properties():
    variants_properties = VariantsProperty.query.all()
    if not variants_properties:
        return "variants propeties not found", 404
    result = variantss_property_schema.dump(variants_properties)
    return jsonify(result.data), 200

@variants_property_api.route("/properties/<id>", methods=['GET'])
@Auth.auth_required
def get_variants_property(id):
    variants_property = VariantsProperty.query.get(id)
    if not variants_property:
        return "variants property not found", 404
    return variants_property_schema.jsonify(variants_property), 200

@variants_property_api.route("/properties/all/<variants_id>", methods=['GET'])
@Auth.auth_required
def get_variants_properties_(variants_id):
    variants_property = VariantsProperty.query.filter_by(variantsId=variants_id).all()
    if not variants_property:
        return "variants property not found", 404
    return variantss_property_schema.jsonify(variants_property), 200

@variants_property_api.route("/properties/<id>", methods=["PUT"])
@Auth.auth_required
def update_variants_property(id):
    try:
        variants_property = VariantsProperty.query.get(id)
        for key, value in request.json.items():
            variants_property.__setattr__(key, value)
        db.session.commit()
    except exc.SQLAlchemyError as ex:
        app.logger.debug(ex)
        return "failed to update variants property", 404
    return variants_property_schema.jsonify(variants_property), 200

@variants_property_api.route("/properties/<id>", methods=["DELETE"])
@Auth.auth_required
def delete_variants_property(id):
    try:
        variants_property = VariantsProperty.query.get(id)
        db.session.delete(variants_property)
        db.session.commit()
    except exc.SQLAlchemyError as ex:
        app.logger.debug(ex)
        return "failed to delete variants property", 404
    return variants_property_schema.jsonify(variants_property), 200
