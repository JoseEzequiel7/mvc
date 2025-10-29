from flask import Flask, redirect, url_for
from yourapp.config import Config
from yourapp.extensions import init_extensions, db , login_manager

from yourapp.auth.routes import auth_bp
from yourapp.controllers.user_controller import user_bp
from yourapp.controllers.product_controller import product_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    init_extensions(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(product_bp)

    from yourapp.auth.utils import load_user
    login_manager.user_loader(load_user) 
    
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

