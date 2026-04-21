# The Vault Campus Marketplace
# CSC 405 Sp 26'

"""
checkout_service.py

Purpose:
This file contains system rules + validation logic for checkout.

This file handles:
- User validation
- Cart validation
- Total cost calculation
- Inventory checks
- Saved user checkout info retrieval
- Multi-step checkout processing
- Calls model functions to run SQL queries

Rules enforced:
- User must be logged in to checkout
- Cart cannot be empty
- ACTIVE listings only can be purchased
- IN_STOCK listings must have enough quantity available
- PREORDER listings do not require quantity_on_hand
- Order total is calculated from current listing prices
- Cart is cleared only after successful order creation
"""

from models.checkout_model import (
    get_checkout_user_info,
    get_cart_items_for_user,
    create_order,
    create_order_item,
    clear_cart_for_user,
    update_listing_inventory
)


def calculate_cart_total(cart_items):
    """
    Calculates total price of all cart items.
    """
    total = 0.0

    for item in cart_items:
        total += float(item["price"]) * int(item["quantity"])

    return round(total, 2)


def get_checkout_screen_data_service(current_user):
    """
    Retrieves all data needed to render the checkout screen.

    Returns:
    - saved user checkout info
    - cart items
    - calculated total
    """
    if current_user is None:
        raise Exception("Unauthorized user.")

    user_id = current_user.get("id")
    if user_id is None:
        raise Exception("Invalid user session.")

    user_info = get_checkout_user_info(user_id)
    if user_info is None:
        raise Exception("User not found.")

    cart_items = get_cart_items_for_user(user_id)
    total_amount = calculate_cart_total(cart_items)

    return {
        "user_info": user_info,
        "cart_items": cart_items,
        "total_amount": total_amount
    }


def _validate_cart_items(cart_items):
    """
    Validates cart items before checkout.
    """
    if not cart_items:
        raise Exception("Cart is empty.")

    for item in cart_items:
        if item["status"] != "ACTIVE":
            raise Exception(f"Listing '{item['title']}' is not available for purchase.")

        if item["price"] is None:
            raise Exception(f"Listing '{item['title']}' is missing a valid price.")

        if int(item["quantity"]) <= 0:
            raise Exception(f"Listing '{item['title']}' has an invalid cart quantity.")

        fulfillment_type = item["fulfillment_type"]

        if fulfillment_type == "IN_STOCK":
            quantity_on_hand = item["quantity_on_hand"]

            if quantity_on_hand is None:
                raise Exception(f"Listing '{item['title']}' is missing inventory data.")

            if int(item["quantity"]) > int(quantity_on_hand):
                raise Exception(
                    f"Not enough inventory for '{item['title']}'. "
                    f"Requested {item['quantity']}, available {quantity_on_hand}."
                )


def complete_transaction_service(current_user):
    """
    Completes the checkout transaction.

    Steps:
    - verify logged in user
    - retrieve saved user info
    - retrieve cart items
    - validate cart/inventory
    - calculate total
    - create order
    - create order item rows
    - update inventory where needed
    - clear cart
    - return order summary
    """
    if current_user is None:
        raise Exception("Unauthorized user.")

    user_id = current_user.get("id")
    if user_id is None:
        raise Exception("Invalid user session.")

    user_info = get_checkout_user_info(user_id)
    if user_info is None:
        raise Exception("User not found.")

    cart_items = get_cart_items_for_user(user_id)
    _validate_cart_items(cart_items)

    total_amount = calculate_cart_total(cart_items)

    order = create_order(
        user_id=user_id,
        total_amount=total_amount,
        order_status="SUBMITTED"
    )

    order_items = []

    for item in cart_items:
        order_item = create_order_item(
            order_id=order["id"],
            listing_id=item["listing_id"],
            quantity=item["quantity"],
            price_at_purchase=item["price"],
            selected_size=item["selected_size"]
        )
        order_items.append(order_item)

        if item["fulfillment_type"] == "IN_STOCK":
            new_quantity = int(item["quantity_on_hand"]) - int(item["quantity"])

            new_status = None
            if new_quantity == 0:
                new_status = "SOLD_OUT"

            update_listing_inventory(
                listing_id=item["listing_id"],
                new_quantity=new_quantity,
                new_status=new_status
            )

    clear_cart_for_user(user_id)

    return {
        "message": "Order submitted successfully.",
        "order": order,
        "order_items": order_items,
        "user_info": user_info,
        "total_amount": total_amount
    }