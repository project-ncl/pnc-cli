from argh import arg
from six import iteritems

import logging
from pnc_cli.swagger_client import ProductRest
from pnc_cli.swagger_client import ProductsApi
from pnc_cli import utils

products_api = ProductsApi(utils.get_api_client())

__author__ = 'thauser'


def _create_product_object(**kwargs):
    created_product = ProductRest()
    for key, value in iteritems(kwargs):
        setattr(created_product, key, value)
    return created_product


def _product_exists(prod_id):
    """
    Checks for an existing Product with ID prod_id
    :param prod_id: the ID to test for
    :return: True if found, False otherwise
    """
    response = utils.checked_api_call(products_api, 'get_specific', id=prod_id)
    return response is not None


def get_product_id(prod_id, name):
    if prod_id:
        if not _product_exists(prod_id):
            logging.error("No Product with id {0} exists.".format(prod_id))
            return
    elif name:
        prod_id = get_product_id_by_name(name)
        if not prod_id:
            logging.error("No Product with the name {0} exists.".format(name))
            return
    else:
        logging.error("Either a Product ID or Product name is required.")
        return
    return prod_id


def get_product_id_by_name(search_name):
    """
    Returns the id of the Product in which name or abbreviation matches search_name
    :param search_name: the name or abbreviation to search for
    :return: the ID of the matching Product
    """
    products = products_api.get_all(q='name=='+search_name).content
    if products:
        product = products[0]
        return product.id
    return


@arg("name", help="Name for the Product")
@arg("-d", "--description", help="Detailed description of the new Product")
@arg("-a", "--abbreviation",
     help="The abbreviation or \"short name\" of the new Product")
@arg("-p", "--product-code", help="The Product code for the new Product")
@arg("-sn", "--pgm-system-name", help="The system code for the new Product")
@arg("-pvids", "--product-version-ids", type=int, nargs='+',
     help="Space separated list of associated ProductVersion ids.")
def create_product(name, **kwargs):
    """
    Create a new Product
    """
    if get_product_id_by_name(name):
        logging.error("Product with the name {0} already exists.".format(name))
        return

    product = _create_product_object(name=name, **kwargs)
    response = utils.checked_api_call(products_api, 'create_new', body=product)
    if response:
        return response.content


@arg("product-id", help="ID of the Product to update")
@arg("-n", "--name", help="New name for the Product")
@arg("-d", "--description", help="New Product description")
@arg("-a", "--abbreviation", help="New abbreviation")
@arg("-p", "--product-code", help="New Product code")
@arg("-sn", "--pgm-system-name", help="New system name")
# @arg("--product-version-ids", type=int, nargs='+', help="Space separated list of associated ProductVersion ids.")
def update_product(product_id, **kwargs):
    """
    Update a Product with new information
    """
    found_id = get_product_id(product_id, None)
    if not found_id:
        return

    to_update = products_api.get_specific(id=found_id).content

    for key, value in iteritems(kwargs):
        if key is 'name':
             if get_product_id_by_name(value):
                 logging.error("Product with the name {0} already exists.".format(value))
                 return
        if value is not None:
            setattr(to_update, key, value)

    response = utils.checked_api_call(
        products_api, 'update', id=product_id, body=to_update)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the Product to retrieve")
@arg("-n", "--name", help="Name of the Product to retrieve")
def get_product(id=None, name=None):
    """
    Get a specific Product by name or ID
    """
    prod_id = get_product_id(id, name)
    if not prod_id:
        return
    response = utils.checked_api_call(products_api, 'get_specific', id=prod_id)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the Product to retrieve versions from")
@arg("-n", "--name", help="Name of the Product to retrieve versions from")
@arg("-p", "--page-size", help="Limit the amount of Product Versions returned")
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_versions_for_product(id=None, name=None, page_size=200, sort='', q=''):
    """
    List all ProductVersions for a given Product
    """
    prod_id = get_product_id(id, name)
    if not prod_id:
        return
    response = utils.checked_api_call(
        products_api, 'get_product_versions', id=prod_id)
    if response:
        return response.content


@arg("-p", "--page-size", help="Limit the amount of Products returned")
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_products(page_size=200, sort="", q=""):
    """
    List all Products
    """
    response = utils.checked_api_call(products_api, 'get_all', page_size=page_size, q=q, sort=sort)
    if response:
        return response.content
