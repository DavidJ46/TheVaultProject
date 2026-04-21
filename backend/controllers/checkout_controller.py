# controllers/checkout_controller.py

from flask import Blueprint, render_template, request, redirect, url_for, session

from services.checkout_service import (
    get_checkout_screen_data_service,
    complete_transaction_service
)

checkout_bp = Blueprint("checkout", __name__)


@checkout_bp.route("/checkout", methods=["GET", "POST"])
def checkout():
    current_user = {"id": session.get("user_id")}

    try:
        # When user clicks "Complete Transaction"
        if request.method == "POST":
            complete_transaction_service(current_user)
            return redirect(url_for("checkout.order_confirmation"))

        # Load checkout page
        checkout_data = get_checkout_screen_data_service(current_user)

        return render_template(
            "checkout.html",
            user_info=checkout_data["user_info"],
            cart_items=checkout_data["cart_items"],
            total_amount=checkout_data["total_amount"]
        )

    except Exception as e:
        return render_template("checkout.html", error=str(e))


@checkout_bp.route("/order-confirmation")
def order_confirmation():
    return render_template("order_confirmation.html")