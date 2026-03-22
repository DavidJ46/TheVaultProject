import sys
import os
from flask import Flask, render_template

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend'))) # Updated 3/19/2026 by Ryan Grimes

from controllers.listing_controller import listing_bp
from controllers.storefront_controller import storefront_bp
from controllers.purchase_controller import purchase_bp
from controllers.wishlist_controller import wishlist_bp
from controllers.admin_controller import admin_bp
from controllers.auth_controller import auth_bp # Updated 3/19/2026 by Ryan Grimes


def create_app():
    app = Flask(__name__, 
                template_folder='templates', 
                static_folder='static')

    app.secret_key = 'vault_secure_key_2026'

    #The Welcome Screen (Default) Ryan Grimes 3/19/2026
    @app.route('/')
    def index():
        return render_template('index.html')

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(listing_bp)
    app.register_blueprint(storefront_bp)
    app.register_blueprint(purchase_bp)
    app.register_blueprint(wishlist_bp)
    app.register_blueprint(admin_bp) # Updated 3/19/2026 by Ryan Grimes

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
