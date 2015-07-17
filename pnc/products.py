from argh import arg
import client
from client.ProductsApi import ProductsApi
import utils


__author__ = 'thauser'
def _create_product_object(name, description, abbreviation, product_code, system_code):
    """
    Create an instance of the Product object
    :param name:
    :param description:
    :param abbreviation:
    :param product_code:
    :param system_code:
    :return: new Product instance
    """
    created_product = client.models.Product.Product()
    created_product.name = name
    #TODO: better way to do this?
    if description: created_product.description = description
    if abbreviation: created_product.abbreviation = abbreviation
    if product_code: created_product.productCode = product_code
    if system_code: created_product.pgmSystemName = system_code
    return created_product

def _get_product_id_by_name(search_name):
    """
    Returns the id of the product in which name or abbreviation matches search_name
    :param search_name: the name or abbreviation to search for
    :return: the ID of the matching product
    """
    response = ProductsApi(utils.get_api_client()).getAll()
    for config in response.json():
        if config["name"] == search_name or config["abbreviation"] == search_name:
            return config["id"]
    return None

def _product_exists(search_id):
    """
    Test if product with id equal to search_id exists
    :param search_id: The id to test for
    :return: True if a product with search_id exists
    """
    response = ProductsApi(utils.get_api_client()).getSpecific(id=search_id)
    if response.ok:
        return True
    return False

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
    response = utils.pretty_format_response(ProductsApi(utils.get_api_client()).createNew(body=product).json())
    print(response)

@arg("product-id", help="ID of the product to update")
@arg("-n","--name", help="New name for the product")
@arg("-d","--description", help="New product description")
@arg("-a","--abbreviation", help="New abbreviation")
@arg("-p","--product-code", help="New product code")
@arg("-s","--system-code", help="New system code")
def update_product(product_id, name=None, description=None, abbreviation=None, product_code=None, system_code=None):
    """Update a product with the given id. Only provide values to update."""
    product = _create_product_object(name, description, abbreviation, product_code, system_code)
    if _product_exists(product_id):
        response = ProductsApi(utils.get_api_client()).update(id=product_id,body=product)
        if response.ok:
            print("Product {0} successfully updated.").format(product_id)
        else:
            print("Updating product {0} failed").format(product_id)
    else:
        print("There is no product with id {0}.").format(product_id)

@arg("-n","--name", help="Name of the product to retrieve")
@arg("-i","--id", help="ID of the product to retrieve")
def get_product(name=None, id=None):

    """List information on a specific product."""
    if id:
        response = ProductsApi(utils.get_api_client()).getSpecific(id=id)
        if response.ok:
            print(utils.pretty_format_response(response.json()))
        else:
            print("No product with id {0} exists.".format(id))
    elif name:
        id = _get_product_id_by_name(name)
        if id:
            print(utils.pretty_format_response(ProductsApi(utils.get_api_client()).getSpecific(id=id).json()))
        else:
            print("No product with name {0} exists.".format(name))
    else:
        print("Either a product name or ID is required.")

def create_product_version():
    pass

@arg("-n","--name", help="Name of the product to retrieve versions from")
@arg("-i","--id", help="ID of the product to retrieve versions from")
def list_product_versions(name=None, id=None):
    if id:
        response = ProductsApi(utils.get_api_client()).getProductVersions(id=id)
        if response.ok:
            print(utils.pretty_format_response(response.json()))
        else:
            print("No product with id {0} exists.".format(id))
    elif name:
        found_id = _get_product_id_by_name(name)
        if found_id:
            print(utils.pretty_format_response(ProductsApi(utils.get_api_client()).getProductVersions(id=found_id)))
        else:
            print("No product with name {0} exists.".format(name))
    else:
        print("Either a product name or ID is required.")

def list_products():
    """List all products."""
    response = utils.pretty_format_response(ProductsApi(utils.get_api_client()).getAll().json())
    print(response)
