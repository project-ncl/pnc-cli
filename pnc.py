import requests, json
import argh

from client import *
from client import swagger
from client.ProductsApi import ProductsApi
from client.models.Product import Product


#TODO: load this from a config file
base_pnc_url = 'http://localhost:8080/pnc-rest/rest'


def _create_product_object(name, description, abbreviation, product_code, system_code):
    returnvalue = Product()
    returnvalue.name = name
    if description: returnvalue.description = description
    if abbreviation: returnvalue.abbreviation = abbreviation
    if product_code: returnvalue.productCode = product_code
    if system_code: returnvalue.pgmSystemName = system_code
    return returnvalue

def create_product(name, description=None, abbreviation=None, product_code=None, system_code=None):
    "Create a new product definition on the configured PNC instance"
    client = swagger.ApiClient(base_pnc_url)
    product = _create_product_object(name, description, abbreviation, product_code, system_code)
    json = ProductsApi(client).createNew(body=product)


def create_project(name, configuration_ids=None, description=None, issue_url=None, project_url=None, license_id=None):
    pass

def get_existing_licenses():
    pass

def get_existing_projects():
    pass

def create_license(name, content, reference_url=None, abbreviation=None, project_ids=None):
    pass

def create_build_configuration(name, project, environment, description='', scm_url='', scm_revision='', patches_url='',
                               build_script=''):
    pass


def list_products():
    pass


def list_product_info(id):
    pass


parser = argh.ArghParser()
parser.add_commands([create_product])

if __name__ == '__main__':
    parser.dispatch()