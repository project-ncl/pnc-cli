from pprint import pprint
import sys

from argh import arg
import swagger_client
from swagger_client.apis.products_api import ProductsApi
import utils

api = ProductsApi(utils.get_api_client())

__author__ = 'thauser'
def _create_product_object(**kwargs):
    created_product = swagger_client.models.product.Product()
    for key, value in kwargs.iteritems():
        setattr(created_product, key, value)
    return created_product

def get_product_id(prod_id, name):
    if prod_id:
        return prod_id
    elif name:
        return get_product_id_by_name(name)
    else:
        print("Either a product ID or product name is required.")
        return

def get_product_id_by_name(search_name):
    """
    Returns the id of the product in which name or abbreviation matches search_name
    :param search_name: the name or abbreviation to search for
    :return: the ID of the matching product
    """
    response = api.get_all()
    for config in response:
        if config.name == search_name:
            return config.id
    return None

@arg("name", help="Name for the product")
@arg("-d","--description", help="Detailed description of the new product")
@arg("-a","--abbreviation", help="The abbreviation or \"short name\" of the new product")
@arg("-p","--product-code", help="The product code for the new product")
@arg("-sn","--pgm-system-name", help="The system code for the new product")
#@arg("--product-version-ids", type=int, nargs='+', help="Space separated list of associated product version ids.")
def create_product(name, **kwargs):
    """Define a new product"""
    kwargs['name'] = name
    product = _create_product_object(**kwargs)
    response = api.create_new(body=product)
    print(response)
    #utils.print_json_result(sys._getframe().f_code.co_name,response)

@arg("product-id", help="ID of the product to update")
@arg("-n","--name", help="New name for the product")
@arg("-d","--description", help="New product description")
@arg("-a","--abbreviation", help="New abbreviation")
@arg("-p","--product-code", help="New product code")
@arg("-sn","--pgm-system-name", help="New system name")
#@arg("--product-version-ids", type=int, nargs='+', help="Space separated list of associated product version ids.")
def update_product(product_id, **kwargs):
    """Update a product with the given id. Only provide values to update."""
    product = _create_product_object(**kwargs)
    def callback(response):
        if response:
            pprint(response)
    thread = api.update(id=product_id, body=product, callback=callback)

@arg("-i","--id", help="ID of the product to retrieve")
@arg("-n","--name", help="Name of the product to retrieve")
def get_product(id=None, name=None):
    """List information on a specific product."""
    prod_id = get_product_id(id,name)
    if not prod_id: return
    print(api.get_specific(id=prod_id))

@arg("-i","--id", help="ID of the product to retrieve versions from")
@arg("-n","--name", help="Name of the product to retrieve versions from")
def list_versions_for_product(id=None, name=None):
    prod_id = get_product_id(id,name)
    if not prod_id: return
    print(api.get_product_versions(id=prod_id))

def list_products():
    """
    List all products
    :return:
    """
    def callback(response):
        pprint(response)
    thread = api.get_all(callback=callback)

