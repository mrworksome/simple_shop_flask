from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# from application.models import Order, Dish, Category
# from application.models_user import User

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    db.init_app(app)
    # admin.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from application.blueprint import home
        from application.blueprint import auth
        # from .assets import compile_assets

        # Register Blueprints
        app.register_blueprint(home.main_bp)
        app.register_blueprint(auth.auth_bp)

        # # Admin Views
        # admin.add_view(ModelView(User, db.session))
        # admin.add_view(ModelView(Order, db.session))
        # admin.add_view(ModelView(Dish, db.session))
        # admin.add_view(ModelView(Category, db.session))

        db.create_all()  # Create database tables for our data models

        return app
