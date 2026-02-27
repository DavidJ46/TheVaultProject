from flask import Flask

from controllers.storefront_controller import storefront_bp
from controllers.listing_controller import listing_bp
from controllers.listing_image_controller import listing_image_bp
from controllers.listing_size_controller import listing_size_bp


def create_app():
    app = Flask(__name__)

    # Register API controllers (Blueprints)
    app.register_blueprint(storefront_bp)
    app.register_blueprint(listing_bp)
    app.register_blueprint(listing_image_bp)
    app.register_blueprint(listing_size_bp)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
