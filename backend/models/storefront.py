# The Vault Campus Marketplace 
# CSC 405 Sp 26' 
# Created by Day Ekoi - Iteration 3 

"""
This is a full description of storefront.py file in the models folder
Purpose: This fine is responsible for defining the Storefront model for the Vault. 
A storefront = a brand owners page (store) and acts as the parent entity for all products
that belong to that brand. 
Storefront enable a marketplace strcuture where each brand owner can manage their own storefront and 
publish multiple listings. Listings are always associated with a storefront, and storefront are always
associated with their owner. It enforces the following hierarchy: User - Storefront - Listing

This file specifically is responsible for:
- defining the storefront databse table
- defining the relationships (brand owner & listings 
- provides methods to convert model data into JSON strctures for the API
"""


