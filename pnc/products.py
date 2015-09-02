import sys

from argh import arg
import swagger_client
from swagger_client.apis.products_api import ProductsApi
import utils


__author__ = 'thauser'
def _create_product_object(**kwargs):
    created_product = swagger_client.models.product.Product()
    for key, value in kwargs.iteritems():
        setattr(created_product, key, value)
    return created_product

def get_product_id(id,name):
    if id:
        prod_id = id
        if not product_exists(prod_id):
            print("No product with id {0} exists.".format(prod_id))
            return
    elif name:
        prod_id = get_product_id_by_name(name)
        if not prod_id:
            print("No product with name {0} exists.".format(name))
            return
    else:
        print("Either a product name or ID is required.")
    return prod_id

def get_product_id_by_name(search_name):
    """
    Returns the id of the product in which name or abbreviation matches search_name
    :param search_name: the name or abbreviation to search for
    :return: the ID of the matching product
    """
    response = get_all()
    for config in response.json():
        if config["name"] == search_name or config["abbreviation"] == search_name:
            return config["id"]
    return None

def product_exists(search_id):
    """
    Test if product with id equal to search_id exists
    :param search_id: The id to test for
    :return: True if a product with search_id exists
    """
    return get_specific(search_id).ok

#localize?
#refine text
@arg("name", help="Name for the product")
@arg("-d","--description", help="Detailed description of the new product")
@arg("-a","--abbreviation", help="The abbreviation or \"short name\" of the new product")
@arg("-p","--product-code", help="The product code for the new product")
@arg("-s","--system-code", help="The system code for the new product")
def create_product(name, description=None, abbreviation=None, product_code=None, system_code=None):
    """Define a new product"""
    product = _create_product_object(name, description, abbreviation, product_code, system_code)
    response = create(product)
    utils.print_json_result(sys._getframe().f_code.co_name,response)

@arg("product-id", help="ID of the product to update")
@arg("-n","--name", help="New name for the product")
@arg("-d","--description", help="New product description")
@arg("-a","--abbreviation", help="New abbreviation")
@arg("-p","--product-code", help="New product code")
@arg("-s","--system-code", help="New system code")
def update_product(product_id, name=None, description=None, abbreviation=None, product_code=None, system_code=None):
    """Update a product with the given id. Only provide values to update."""
    product = _create_product_object(name, description, abbreviation, product_code, system_code)
    if product_exists(product_id):
        response = update(product_id, product)
        if not response.ok:
            utils.print_error(sys._getframe().f_code.co_name,response)
            return

        print("Product {0} successfully updated.").format(product_id)
    else:
        print("There is no product with id {0}.").format(product_id)

@arg("-i","--id", help="ID of the product to retrieve")
@arg("-n","--name", help="Name of the product to retrieve")
def get_product(id=None, name=None):
    """List information on a specific product."""
    if name:
        prod_id = get_product_id_by_name(name)
    else:
        prod_id = id

    response = get_specific(prod_id)
    print(response)
#    utils.print_json_result(sys._getframe().f_code.co_name,
#                           response)

@arg("-i","--id", help="ID of the product to retrieve versions from")
@arg("-n","--name", help="Name of the product to retrieve versions from")
@arg("-a","--attributes", help="Comma separated list of attributes to print for each product version")
def list_versions_for_product(id=None, name=None, attributes=None):
    prod_id = get_product_id(id,name)
    if not prod_id:
        return
    response = get_product_versions(prod_id)
    utils.print_json_result(sys._getframe().f_code.co_name,
                            response,
                            attributes,
                            swagger_client.models.product_version.ProductVersion().attribute_map)

@arg("-a","--attributes", help="Comma separated list of attributes to print for each product")
def list_products(attributes=None):
    print (get_all())
    #response = get_all()
    #utils.print_json_result(sys._getframe().f_code.co_name,
    #                        response,
    #                        attributes,
    #                        swagger_client.models.product.Product().attribute_map)

def get_all():
    return ProductsApi(utils.get_api_client()).get_all()

def get_specific(prod_id):
    return ProductsApi(utils.get_api_client()).get_specific(id=prod_id)

def create(product):
    return ProductsApi(utils.get_api_client()).create_new(body=product)

def update(prod_id, product):
    return ProductsApi(utils.get_api_client()).update(id=prod_id,body=product)

def delete(prod_id):
    return ProductsApi(utils.get_api_client()).delete(id=prod_id)

def get_product_versions(prod_id):
    return ProductsApi(utils.get_api_client()).get_product_versions(id=prod_id)
