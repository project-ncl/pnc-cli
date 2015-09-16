from pprint import pprint
import sys

from argh import arg
import swagger_client
from swagger_client.apis.products_api import ProductsApi
import utils

products_api = ProductsApi(utils.get_api_client())

__author__ = 'thauser'
def _create_product_object(**kwargs):
    created_product = swagger_client.ProductRest()
    for key, value in kwargs.iteritems():
        setattr(created_product, key, value)
    return created_product

def _product_exists(prod_id):
    """
    Checks for an existing Product with ID prod_id
    :param prod_id: the ID to test for
    :return: True if found, False otherwise
    """
    existing_ids = [str(x.id) for x in products_api.get_all().content]
    return str(prod_id) in existing_ids

def get_product_id(prod_id, name):
    if prod_id:
        if not _product_exists(prod_id):
            print("No product with id {0} exists.").format(prod_id)
            return
    elif name:
        prod_id = get_product_id_by_name(name)
        if not prod_id:
            print("No product with the name {0} exists.").format(name)
            return
    else:
        print("Either a product ID or product name is required.")
        return
    return prod_id

def get_product_id_by_name(search_name):
    """
    Returns the id of the product in which name or abbreviation matches search_name
    :param search_name: the name or abbreviation to search for
    :return: the ID of the matching product
    """
    products = products_api.get_all().content
    for product in products:
        if product.name == search_name:
            return product.id
    return None

@arg("name", help="Name for the product")
@arg("-d","--description", help="Detailed description of the new product")
@arg("-a","--abbreviation", help="The abbreviation or \"short name\" of the new product")
@arg("-p","--product-code", help="The product code for the new product")
@arg("-sn","--pgm-system-name", help="The system code for the new product")
#@arg("--product-version-ids", type=int, nargs='+', help="Space separated list of associated product version ids.")
def create_product(name, **kwargs):
    """
    Create a new Product
    """
    product = _create_product_object(name=name, **kwargs)
    response = utils.checked_api_call(products_api, 'create_new',body=product)
    if response: return response.content

@arg("product-id", help="ID of the product to update")
@arg("-n","--name", help="New name for the product")
@arg("-d","--description", help="New product description")
@arg("-a","--abbreviation", help="New abbreviation")
@arg("-p","--product-code", help="New product code")
@arg("-sn","--pgm-system-name", help="New system name")
#@arg("--product-version-ids", type=int, nargs='+', help="Space separated list of associated product version ids.")
#TODO: Get existing product at product_id and modify relevant fields
def update_product(product_id, **kwargs):
    """
    Update a Product with new information
    """
    product = _create_product_object(**kwargs)
    response = utils.checked_api_call(products_api,'update', id=product_id, body=product)
    if response: return response.content

@arg("-i","--id", help="ID of the product to retrieve")
@arg("-n","--name", help="Name of the product to retrieve")
def get_product(id=None, name=None):
    """
    Get a specific Product by name or ID
    """
    prod_id = get_product_id(id,name)
    if not prod_id: return
    response = utils.checked_api_call(products_api, 'get_specific', id=prod_id)
    if response: return response.content

@arg("-i","--id", help="ID of the product to retrieve versions from")
@arg("-n","--name", help="Name of the product to retrieve versions from")
def list_versions_for_product(id=None, name=None):
    prod_id = get_product_id(id,name)
    if not prod_id: return
    response = utils.checked_api_call(products_api, 'get_product_versions', id=prod_id)
    if response: return response.content

def list_products():
    """
    List all Products
    """
    response = utils.checked_api_call(products_api,'get_all')
    if response: return response.content
