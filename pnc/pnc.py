#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
import argh, json
from argh import arg
import client.swagger
from client.BuildconfigurationsApi import BuildconfigurationsApi
from client.LicensesApi import LicensesApi
from client.ProductsApi import ProductsApi
from client.ProjectsApi import ProjectsApi
from client.models.Configuration import Configuration
from client.models.License import License
import client.models.Product

from pnc_help_formatter import PNCFormatter

#TODO: load this from a config file
base_pnc_url = 'http://localhost:8080/pnc-rest/rest'
apiclient = client.swagger.ApiClient(base_pnc_url)

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
    created_project = client.models.Project.Project()
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

def _remove_nulls(input_json):
     keys = input_json.keys()
     if keys:
         for k in keys:
             if input_json[k] == None:
                  del input_json[k]

def pretty_format_response(input_json):
    """
    prints the json dump in a more readable format.
    does not print null values
    :param input_json:
    :return:
    """
    if type(input_json) is list:
        for item in input_json:
            _remove_nulls(item)
    else:
        _remove_nulls(input_json)
    return json.dumps(input_json, indent=4, separators=[',',': '], sort_keys=True)


def _find_product_by_name(search_name):
    response = ProductsApi(apiclient).getAll()
    for config in response.json():
        if config['name'] == search_name:
            return config['id']

def _find_product_by_id(search_id):
    response = ProductsApi(apiclient).getAll()
    for config in response.json():
        if config['id'] == int(search_id):
            return True

def _find_build_configuration_by_name(name):
    response = BuildconfigurationsApi(apiclient).getAll()
    for config in response.json():
        if config['name'] == name:
            return config['id']
    return None

def _find_build_configuration_by_id(search_id):
    response = BuildconfigurationsApi(apiclient).getAll()
    for config in response.json():
        if config['id'] == int(search_id):
            return True

#localize?
#refine text
@arg('name', help='Name for the product')
@arg('-d','--description', help="Detailed description of the new product")
@arg('-a','--abbreviation', help="The abbreviation or \"short name\" of the new product")
@arg('-p','--product-code', help="The product code for the new product")
@arg('-s','--system-code', help="The system code for the new product")
def create_product(name, description=None, abbreviation=None, product_code=None, system_code=None):
    "Create a new product"
    product = _create_product_object(name, description, abbreviation, product_code, system_code)
    response = pretty_format_response(ProductsApi(apiclient).createNew(body=product).json())
    print(response)

@arg('id', help='ID of the product to update')
@arg('-n','--name', help="New name for the product")
@arg('-d','--description', help="New product description")
@arg('-a','--abbreviation', help="New abbreviation")
@arg('-p','--product-code', help="New product code")
@arg('-s','--system-code', help="New system code")
def update_product(id, name=None, description=None, abbreviation=None, product_code=None, system_code=None):
    "Update a product. Only provide values that need updating."
    product = _create_product_object(name, description, abbreviation, product_code, system_code)
    if _find_product_by_id(id):
        response = ProductsApi(apiclient).update(id=id,body=product)
        if response.status_code == 200:
            print('Product id: {0} successfully updated.').format(id)
        else:
            print('Updating product: {0} failed').format(id)
    else:
        print('There is no product with id {0}.').format(id)

@arg('-n','--name', help="Name of the product to retrieve")
@arg('-i','--id', help="ID of the product to retrieve")
def get_product(name=None, id=None):
    if id:
        if (_find_product_by_id(id)):
            print(pretty_format_response(BuildconfigurationsApi(apiclient).trigger(id=id).json()))
        else:
            print 'There is no product with id {0}.'.format(id)
    elif name:
        build_id = _find_product_by_name(name)
        if build_id:
            print(pretty_format_response(BuildconfigurationsApi(apiclient).trigger(id=build_id).json()))
        else:
            print 'There is no product with name {0}.'.format(name)
    else:
        print 'Trigger build requires either a name or an ID of a build configuration to trigger.'


@arg('name', help='Name for the project')
@arg('-c','--configuration-ids', help="List of configuration IDs this project should be associated with")
@arg('-d','--description', help="Detailed description of the new project")
@arg('-p','--project_url', help="SCM Url for the project")
@arg('-i','--issue_url', help="Issue tracker URL for the new project")
@arg('-l','--license_id', help="License ID for the new project")
def create_project(name, configuration_ids=None, description=None, issue_url=None, project_url=None, license_id=None):
    "Create a new project "
    project = _create_project_object(name, configuration_ids, description, issue_url, project_url, license_id)
    response = pretty_format_response(ProjectsApi(apiclient).createNew(body=project).json())
    print(response)

@arg('name', help='Name for the new license')
@arg('content', help='Full textual content of the new license')
@arg('-r','--reference-url', help='URL containing a reference for the license')
@arg('-a','--abbreviation', help='Abbreviation or \"short name\" for the license')
@arg('-p','--project-ids', help='List of project ids that should be associated with the new license. IDs must denote existing projects')
def create_license(name, content, reference_url=None, abbreviation=None, project_ids=None):
    "Create a new license"
    license = _create_license_object(name, content, reference_url, abbreviation, project_ids)
    response = pretty_format_response(LicensesApi(apiclient).createNew(body=license).json())
    print(response)

def list_licenses():
    "Get a JSON object containing existing licenses"
    response = pretty_format_response(LicensesApi(apiclient).getAll().json())
    print(response)

def list_products():
    "Get a JSON object containing existing products"
    response = pretty_format_response(ProductsApi(apiclient).getAll().json())
    print(response)

def list_projects():
    "Get a JSON object containing existing projects"
    response = pretty_format_response(ProjectsApi(apiclient).getAll().json())
    print(response)

def list_build_configurations():
    "Get a JSON object containing existing build configurations"
    response = pretty_format_response(BuildconfigurationsApi(apiclient).getAll().json())
    print(response)

@arg('-n', '--name', help='Name of the build configuration to trigger')
@arg('-i', '--id', help='ID of the build configuration to trigger')
def trigger_build(name=None,id=None):
    "Trigger a build giving either the name or ID of the build configuration."
    if id:
        if (_find_build_configuration_by_id(id)):
            print(pretty_format_response(BuildconfigurationsApi(apiclient).trigger(id=id).json()))
        else:
            print 'There is no build configuration with id {0}.'.format(id)
    elif name:
        build_id = _find_build_configuration_by_name(name)
        if build_id:
            print(pretty_format_response(BuildconfigurationsApi(apiclient).trigger(id=build_id).json()))
        else:
            print 'There is no build configuration with name {0}.'.format(name)
    else:
        print 'Trigger build requires either a name or an ID of a build configuration to trigger.'


def create_build_configuration(name, project_id, environment, description='', scm_url='', scm_revision='', patches_url='',
                               build_script=''):
    #check for existing project_ids, fail out if the project id doesn't exist
    build_configuration = _create_build_configuration(name, project_id, environment, description, scm_url, scm_revision, patches_url, build_script)
    response = pretty_format_response(BuildconfigurationsApi(apiclient).createNew(body=build_configuration).json())
    print(response)

parser = argh.ArghParser()
parser.add_commands([create_product,update_product,get_product,create_project,create_license,list_products,list_projects,list_licenses,list_build_configurations,trigger_build], func_kwargs={'formatter_class': PNCFormatter})
parser.autocomplete()

if __name__ == '__main__':
    parser.dispatch()