from flask import Flask
from controllers.listing_controller import listing_bp
from controllers.storefront_controller import storefront_bp


def create_app():
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(listing_bp)
    app.register_blueprint(storefront_bp)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
