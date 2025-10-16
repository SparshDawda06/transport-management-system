from flask import Flask, render_template
from .config import DevelopmentConfig
from .extensions import db, migrate, csrf
import os
import logging


def create_app(config_class: type = None) -> Flask:
    app = Flask(__name__, static_folder="static", template_folder="templates")
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)
    
    # Use DevelopmentConfig by default if no config specified
    if config_class is None:
        config_class = DevelopmentConfig
    
    app.config.from_object(config_class)

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    
    # Create default user if not exists
    with app.app_context():
        try:
            from .auth import create_default_user_if_not_exists
            create_default_user_if_not_exists()
            app.logger.info("Default user creation completed")
        except Exception as e:
            app.logger.error(f"Error creating default user: {e}")

    # Blueprints
    from .main.routes import bp as main_bp
    app.register_blueprint(main_bp)
    from .blueprints.orders import bp as orders_bp
    app.register_blueprint(orders_bp)
    from .blueprints.builty import bp as builty_bp
    app.register_blueprint(builty_bp)
    from .blueprints.api import bp as api_bp
    app.register_blueprint(api_bp)
    from .blueprints.entities import bp as entities_bp
    app.register_blueprint(entities_bp)
    from .blueprints.fleet import bp as fleet_bp
    app.register_blueprint(fleet_bp)
    from .blueprints.system import bp as system_bp
    app.register_blueprint(system_bp)
    from .blueprints.phonebook import bp as phonebook_bp
    app.register_blueprint(phonebook_bp)
    from .blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    # CLI
    from .cli import create_db as create_db_command, seed_data as seed_data_command
    app.cli.add_command(create_db_command)
    app.cli.add_command(seed_data_command)

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    return app
