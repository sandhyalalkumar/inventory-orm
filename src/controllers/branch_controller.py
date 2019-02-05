from flask import request, jsonify
from src.models import db
from flask import Blueprint
from src.models.branch_model import Branch
from src.models.branch_model import BranchSchema
from src.common.authentication import Auth
from sqlalchemy import exc
from flask import current_app as app

branch_api = Blueprint("branch_api", __name__)

branch_schema = BranchSchema()
branches_schema = BranchSchema(many=True)

@branch_api.route("/branch", methods=['POST'])
@Auth.auth_required
def add_branch():
    branch = Branch(request.json)
    try:
        db.session.add(branch)
        db.session.commit()
    except exc.SQLAlchemyError as ex:
        app.logger.debug(ex)
        return "encountered error adding branch", 404
    return jsonify(request.json), 200

@branch_api.route("/branches", methods=['GET'])
@Auth.auth_required
def get_branches():
    branches = Branch.query.all()
    if not branches:
        return "no branch registered", 404
    result = branches_schema.dump(branches)
    return jsonify(result.data), 200

@branch_api.route("/branch/<id>", methods=['GET'])
@Auth.auth_required
def get_branch(id):
    branch = Branch.query.get(id)
    if not branch:
        return "branch not registered", 404
    return branch_schema.jsonify(branch), 200

@branch_api.route("/branch/<id>", methods=["PUT"])
@Auth.auth_required
def update_branch(id):
    try:
        branch = Branch.query.get(id)
        for key, value in request.json.items():
            branch.__setattr__(key, value)
        db.session.commit()
    except exc.SQLAlchemyError as ex:
        app.logger.error(ex)
        return "error encountered updating branch", 404
    return branch_schema.jsonify(branch), 202

@branch_api.route("/branch/<id>", methods=["DELETE"])
@Auth.auth_required
def delete_branch(id):
    try:
        branch = Branch.query.get(id)
        db.session.delete(branch)
        db.session.commit()
    except exc.SQLAlchemyError as ex:
        app.logger.error(ex)
        return "error encountered deleting branch", 404
    return branch_schema.jsonify(branch), 200
