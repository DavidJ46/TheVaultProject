from flask import Flask
from controllers.listing_controller import listing_bp
from controllers.storefront_controller import storefront_bp

from controllers.storefront_controller import storefront_bp
from controllers.listing_controller import listing_bp
from controllers.listing_image_controller import listing_image_bp
from controllers.listing_size_controller import listing_size_bp


def create_app():
    app = Flask(__name__)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
