# The Vault Campus Marketplace
# CSC 405 Sp 26'
# Created by Day Ekoi - Iteration 3

"""
storefront_service.py

Purpose: This file enforces rules such as ownership checks, validation, and permissions

What it does: 
- checks permissions (owner vs admin)
- Enforces any rules (ex: a user can only have 1 storefront)
- Validates required input (ex: Brand name)
- Calls the model file (storefront_model.py) to run SQL queries

Addtionally, this service experecs image URLs (S3) to be stored in the DB.
"""

from models.storefront_model import(
    create_storefront,
    get_storefront_by_id,
    get_storefront_by_owner_id,
    update_storefront,
    set_storefront_active
)

def is_admin(current_user): 
  
    """ returns True is the logged-in user is an admin. 
    this function is here so there we dont have to constantly do role validation checks 
    """

return current_user.get("role") == "admin"

def create_storefront_service(current_user, data):

    """
    Creates a storefront for a current user.

    The rules enforced include:
    - user must be logged in
    - user can only create one storefront
    - brand_name is required
    """



#_________________________________________________________________________________
#                 RULE ENFORCEMENT 
#_________________________________________________________________________________

# Rule 1. Must be logged in to create a storefront

if not current_user:
  raise Exception("Error! Unauthorized user.")

# Rule 2. Prevention of duplicate storefronts 

existing = get_storefront_by_owner_id(current_user["id"])
if existing:
  raise Exception("Storefront already created.")

# Rule 3. Validate required input
brand_name = (data.get("brand_name") or "").strip()
if not brand_name:
  raise Exception("brand_name is required")

# Rule 4. Calling of model file to inseet into database 
return create_storefront(
    owner_id=current_user["id"],
    brand_name=brand_name,
    bio=data.get("bio"),
    logo_url=data.get("logo_url"),
    banner_url=data.get("banner_url"),
 )






def get_my_storefront_service(current_user):
    """
    Returns the storefront owned by the current user.
    Used for "My Storefront" views and owner dashboards.
    """
    if not current_user:
        raise Exception("Error! Unauthorized user.")
  

    # Pull storefront based on the user’s id
    return get_storefront_by_owner_id(current_user["id"])



def update_storefront_service(current_user, storefront_id, data):
    """
    Updates an existing storefront.

    Permissions:
    - The storefront owner can update their storefront
    - Admins can update any storefront
    """
  
    if not current_user:
        raise Exception("Error! Unauthorized user.")

    storefront = get_storefront_by_id(storefront_id)
    if not storefront:
        raise Exception("Storefront not found.")

    # Owner/admin check
    is_owner = (storefront["owner_id"] == current_user["id"])
    if not is_owner and not is_admin(current_user):
        raise Exception("Unauthorized action.")

    # Allows for only these fields to be updated
    # Prevention of restricted column manipulation 
    allowed_fields = {"brand_name", "bio", "logo_url", "banner_url"}

    # Build clean values to pass to the model
    clean = {k: data.get(k) for k in allowed_fields}

    # If brand_name is being updated, enforce non-empty
    if clean.get("brand_name") is not None:
        clean["brand_name"] = clean["brand_name"].strip()
        if not clean["brand_name"]:
            raise Exception("brand_name cannot be empty.")

    # Call model update
    return update_storefront(
        storefront_id=storefront_id,
        brand_name=clean.get("brand_name"),
        bio=clean.get("bio"),
        logo_url=clean.get("logo_url"),
        banner_url=clean.get("banner_url"),
        instagram_handle=clean.get("instagram_handle")
    )


def deactivate_storefront_service(current_user, storefront_id):
    """
    Soft-deactivates a storefront (sets is_active = False).

    Purpose of soft-deactivation:
    - Keeps database history intact
    - Preserves relationships (listings, purchases, etc.)
    - Allows admin moderation or temp shutdown
    """
  
    if not current_user:
        raise Exception(" Error! Unauthorized User.")

    storefront = get_storefront_by_id(storefront_id)
    if not storefront:
        raise Exception("Storefront not found.")

    is_owner = (storefront["owner_id"] == current_user["id"])
    if not is_owner and not is_admin(current_user):
        raise Exception("Unauthorized action.")

    # Update is_active flag 
    return set_storefront_active(storefront_id, False)
