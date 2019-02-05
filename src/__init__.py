from flask import Flask
from flask_migrate import Migrate
from config import app_config
from src.models import db
from src.models import bcrypt
from src.controllers.product_controller import product_api
from src.controllers.variants_controller import variants_api
from src.controllers.variants_property_controller import variants_property_api
from src.controllers.branch_controller import branch_api
from src.controllers.user_controller import user_api

def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.register_blueprint(product_api, url_prefix="/api")
    app.register_blueprint(variants_api, url_prefix="/api")
    app.register_blueprint(variants_property_api, url_prefix="/api")
    app.register_blueprint(branch_api, url_prefix="/api")
    app.register_blueprint(user_api, url_prefix="/api")
    db.init_app(app)
    bcrypt.init_app(app)

    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    migrate = Migrate(app, db)
    from src.models.branch_model import Branch
    from src.models.product_model import Product
    from src.models.variants_model import Variants
    from src.models.variants_property_model import VariantsProperty

    return app