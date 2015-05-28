import requests, json
import argh
from argh import arg

from client import *
from client import swagger
from client.BuildconfigurationsApi import BuildconfigurationsApi
from client.LicensesApi import LicensesApi
from client.ProductsApi import ProductsApi
from client.ProjectsApi import ProjectsApi
from client.models.BuildConfigurationSet import BuildConfigurationSet
from client.models.Configuration import Configuration
from client.models.License import License
from client.models.Product import *
from client.models.Project import *

#TODO: load this from a config file
base_pnc_url = 'http://localhost:8080/pnc-rest/rest'
client = swagger.ApiClient(base_pnc_url)

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
    created_product = Product()
    created_product.name = name
    #TODO: better way to do this?
    if description: created_product.description = description
    if abbreviation: created_product.abbreviation = abbreviation
    if product_code: created_product.productCode = product_code
    if system_code: created_product.pgmSystemName = system_code
    return created_product

def _create_project_object(name, configuration_ids, description, issue_url, project_url, license_id):
    """
    Create an instance of the Project object
    :param name:
    :param configuration_ids:
    :param description:
    :param issue_url:
    :param project_url:
    :param license_id:
    :return: new Project instance
    """
    created_project = Project()
    created_project.name = name
    if configuration_ids: created_project.configurationIds = configuration_ids
    if description: created_project.description = description
    if issue_url: created_project.issueTrackerUrl = issue_url
    if project_url: created_project.projectUrl = project_url
    if license_id: created_project.licenseId = license_id
    return created_project

def _create_license_object(name, content, reference_url, abbreviation, project_ids):
    created_license = License()
    created_license.fullName = name
    created_license.fullContent = content
    if reference_url: created_license.refUrl = reference_url
    if abbreviation: created_license.shortName = abbreviation
    if project_ids: created_license.projectsIds = project_ids
    return created_license


def _create_build_configuration(name, project_id, environment, description, scm_url, scm_revision, patches_url,
                                build_script):
    created_build_configuration = Configuration()
    created_build_configuration.name = name
    created_build_configuration.projecId = project_id


def pretty_format_response(input_json):
    """
    Pretty formats the input json for printing to the user
    :param input_json:
    :return:
    """
    return json.dumps(input_json, indent=4, separators=[',',': '])


#localize?
#refine text
@arg('name', help='Name for the product')
@arg('-d','--description', help="Detailed description of the new product")
@arg('-a','--abbreviation', help="The abbreviation or \"short name\" of the new product")
@arg('-p','--product_code', help="The product code for the new product")
@arg('-s','--system_code', help="The system code for the new product")
def create_product(name, description=None, abbreviation=None, product_code=None, system_code=None):
    "Create a new product definition on the configured PNC instance"
    product = _create_product_object(name, description, abbreviation, product_code, system_code)
    response = pretty_format_response(ProductsApi(client).createNew(body=product))
    print(response)

def create_project(name, configuration_ids=None, description=None, issue_url=None, project_url=None, license_id=None):
    project = _create_project_object(name, configuration_ids, description, issue_url, project_url, license_id)
    response = pretty_format_response(ProjectsApi(client).createNew(body=project))
    print(response)

def create_license(name, content, reference_url=None, abbreviation=None, project_ids=None):
    license = _create_license_object(name, content, reference_url, abbreviation, project_ids)
    response = pretty_format_response(LicensesApi(client).createNew(body=license))
    print(response)

def list_licenses():
    response = pretty_format_response(LicensesApi(client).getAll())
    print(response)

def list_products():
    response = pretty_format_response(ProductsApi(client).getAll())
    print(response)

def list_projects():
    response = pretty_format_response(ProjectsApi(client).getAll())
    print(response)

def create_build_configuration(name, project_id, environment, description='', scm_url='', scm_revision='', patches_url='',
                               build_script=''):
    #check for existing project_ids, fail out if the project id doesn't exist
    build_configuration = _create_build_configuration(name, project_id, environment, description, scm_url, scm_revision, patches_url, build_script)
    response = pretty_format_response(BuildconfigurationsApi(client).createNew(body=build_configuration))
    print(response)


parser = argh.ArghParser()
parser.add_commands([create_product,create_project,create_license,list_products,list_projects,list_licenses])

if __name__ == '__main__':
    parser.dispatch()