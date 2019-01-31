from flask import Flask
from flask_migrate import Migrate
from config import app_config
from src.models import db
from src.controllers.product_controller import product_api

def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.register_blueprint(product_api, url_prefix="/api")
    db.init_app(app)

    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    migrate = Migrate(app, db)
    from src.models.branch_model import Branch
    from src.models.product_model import Product
    from src.models.product_variant_model import ProductVariant
    from src.models.variant_properties_model import VariantProperty

    return app