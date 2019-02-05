from flask import request, jsonify
from src.models import db
from flask import Blueprint
from src.models.variants_model import VariantsSchema
from src.models.variants_model import Variants
from sqlalchemy import exc
from flask import current_app as app
from src.common.authentication import Auth

variants_api = Blueprint("variants_api", __name__)

variant_schema = VariantsSchema()
variants_schema = VariantsSchema(many=True)

@variants_api.route("/variants", methods=['POST'])
@Auth.auth_required
def add_variant():
    variants = Variants(request.json)
    try:
        db.session.add(variants)
        db.session.commit()
    except exc.SQLAlchemyError as ex:
        app.logger.error(ex)
        return "failed to add variant", 404
    return jsonify(request.json), 200

@variants_api.route("/variants", methods=['GET'])
@Auth.auth_required
def get_variants():
    variants = Variants.query.all()
    if not variants:
        return "variants not found", 404
    result = variants_schema.dump(variants)
    return jsonify(result.data), 200

@variants_api.route("/variants/<id>", methods=['GET'])
@Auth.auth_required
def get_variant(id):
    variants = Variants.query.get(id)
    if not variants:
        return "variants not found", 404
    return variant_schema.jsonify(variants)

@variants_api.route("/variants/<id>", methods=["PUT"])
@Auth.auth_required
def update_variant(id):
    try:
        variants = Variants.query.get(id)
        for key, value in request.json.items():
            variants.__setattr__(key, value)
        db.session.commit()
    except exc.SQLAlchemyError as ex:
        app.logger.error(ex)
        return "failed to update variants", 404
    return variant_schema.jsonify(variants), 200

@variants_api.route("/variants/<id>", methods=["DELETE"])
@Auth.auth_required
def delete_variant(id):
    try:
        variants = Variants.query.get(id)
        db.session.delete(variants)
        db.session.commit()
    except exc.SQLAlchemyError as ex:
        app.logger.debug(ex)
        return "failed to delete variants", 404
    return variant_schema.jsonify(variants), 200
