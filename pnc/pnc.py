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
from client.EnvironmentsApi import EnvironmentsApi
from client.models.EnvironmentRest import EnvironmentRest

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

#TODO: Error checking configuration_ids is necessary, since it must consist of a list of valid build_configuration ids
def _create_project_object(name, description, configuration_ids, issue_url, project_url, license_id):
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
    created_build_configuration.projectId = project_id

def _create_environment_object(build_type, operational_system):
    created_environment = EnvironmentRest()
    created_environment.buildType = build_type
    created_environment.operationalSystem = operational_system
    return created_environment


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

def _get_product_id_by_name(search_name):
    """
    Returns the id of the product in which name or abbreviation matches search_name
    :param search_name: the name or abbreviation to search for
    :return: the ID of the matching product
    """
    response = ProductsApi(apiclient).getAll()
    for config in response.json():
        if config['name'] == search_name or config['abbreviation'] == search_name:
            return config['id']
    return None

def _product_exists(search_id):
    """
    Test if product with id equal to search_id exists
    :param search_id: The id to test for
    :return: True if a product with search_id exists
    """
    response = ProductsApi(apiclient).getSpecific(id=search_id)
    if (response.status_code == 200):
        return True
    return False

def _get_project_id_by_name(search_name):
    """
    Returns the id of the project in which name matches search_name
    :param search_name: name of the project
    :return: id of the matching project, or None if no match found
    """
    response = ProjectsApi(apiclient).getAll()
    for config in response:
        if config['name'] == search_name:
            return config['id']
    return None

def _project_exists(search_id):
    """
    Test if a project with the given id exists
    :param search_id: id to test for
    :return: True if a project with search_id exists
    """
    response = ProjectsApi(apiclient).getSpecific(id=search_id)
    if (response.status_code == 200):
        return True
    return False

def _get_build_configuration_id_by_name(name):
    """
    Returns the id of the build configuration matching name
    :param name: name of build configuration
    :return: id of the matching build configuration, or None if no match found
    """
    response = BuildconfigurationsApi(apiclient).getAll()
    for config in response.json():
        if config['name'] == name:
            return config['id']
    return None

def _build_configuration_exists(search_id):
    """
    Test if a build configuration matching search_id exists
    :param search_id: id to test for
    :return: True if a build configuration with search_id exists
    """
    response = BuildconfigurationsApi(apiclient).getSpecific(id=search_id)
    if response.status_code == 200:
        return True
    return False

#localize?
#refine text
@arg('name', help='Name for the product')
@arg('-d','--description', help="Detailed description of the new product")
@arg('-a','--abbreviation', help="The abbreviation or \"short name\" of the new product")
@arg('-p','--product-code', help="The product code for the new product")
@arg('-s','--system-code', help="The system code for the new product")
def create_product(name, description=None, abbreviation=None, product_code=None, system_code=None):
    "Define a new product"
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
    "Update a product with the given id. Only provide values to update."
    product = _create_product_object(name, description, abbreviation, product_code, system_code)
    if _product_exists(id):
        response = ProductsApi(apiclient).update(id=id,body=product)
        if response.status_code == 200:
            print('Product {0} successfully updated.').format(id)
        else:
            print('Updating product {0} failed').format(id)
    else:
        print('There is no product with id {0}.').format(id)

@arg('-n','--name', help="Name of the product to retrieve")
@arg('-i','--id', help="ID of the product to retrieve")
def get_product(name=None, id=None):
    "List information on a specific product."
    if id:
        response = ProductsApi(apiclient).getSpecific(id=id)
        if (response.status_code == 200):
            print(pretty_format_response(response.json()))
        else:
            print 'There is no product with id {0}.'.format(id)
    elif name:
        product_id = _get_product_id_by_name(name)
        if product_id:
            print(pretty_format_response(ProductsApi(apiclient).getSpecific(id=product_id).json()))
        else:
            print 'There is no product with name {0}.'.format(name)
    else:
        print 'Either a product name or ID is required.'

def list_products():
    "List all products."
    response = pretty_format_response(ProductsApi(apiclient).getAll().json())
    print(response)

@arg('name', help='Name for the project')
@arg('-c','--configuration-ids', help="List of configuration IDs this project should be associated with")
@arg('-d','--description', help="Detailed description of the new project")
@arg('-p','--project_url', help="SCM Url for the project")
@arg('-i','--issue_url', help="Issue tracker URL for the new project")
@arg('-l','--license_id', help="License ID for the new project")
def create_project(name, configuration_ids=None, description=None, issue_url=None, project_url=None, license_id=None):
    "Create a new project"
    project = _create_project_object(name, configuration_ids, description, issue_url, project_url, license_id)
    response = pretty_format_response(ProjectsApi(apiclient).createNew(body=project).json())
    print(response)

def update_project(id, name=None, description=None, issue_tracker_url=None, project_url=None, configuration_ids=None,license_id=None):
    project = _create_project_object(name, description, issue_tracker_url, project_url, configuration_ids, license_id)
    if _project_exists(id):
        response = ProjectsApi(apiclient).update(id=id,body=project)
        if response.status_code == 200:
            print('Project {0} successfully updated.').format(id)
        else:
            print('Updating project with id {0} failed').format(id)
    else:
        print('There is no project with id {0}.').format(id)

def delete_project(id=None, name=None):
    if id:
        if not _project_exists(id):
            print("There is no project with id {0}.").format(id)
            return
        project_id = id
    elif name:
        project_id = _get_project_id_by_name(name)
        if not project_id:
            print("There is no project with name {0}.").format(name)
            return
    else:
        print("Either a project name or id is required.")
        return

    response = ProjectsApi(apiclient).deleteSpecific(id=project_id)
    if (response.status_code == 200):
        print("Project {0} successfully deleted.").format(project_id)
    else:
        print("Failed to delete Project {0}").format(project_id)


@arg('name', help='Name for the new license')
@arg('content', help='Full textual content of the new license')
@arg('-r','--reference-url', help='URL containing a reference for the license')
@arg('-a','--abbreviation', help='Abbreviation or \"short name\" for the license')
@arg('-p','--project-ids', help='List of project ids that should be associated with the new license. IDs must denote existing projects')
def create_license(name, content, reference_url=None, abbreviation=None, project_ids=None):
    "Create a new license"
    license = _create_license_object(name, content, reference_url, abbreviation, project_ids)
    response = LicensesApi(apiclient).createNew(body=license)
    print(pretty_format_response(response.json()))

def list_licenses():
    "Get a JSON object containing existing licenses"
    response = LicensesApi(apiclient).getAll()
    print(pretty_format_response(response.json()))

def list_projects():
    "Get a JSON object containing existing projects"
    response = ProjectsApi(apiclient).getAll()
    print(pretty_format_response(response.json()))

def list_build_configurations():
    "Get a JSON object containing existing build configurations"
    response = BuildconfigurationsApi(apiclient).getAll()
    print(pretty_format_response(response.json()))


@arg("build-type", help="Type of build for this build environment")
@arg("operating-system", help="Operating system for this build environment")
def create_environment(build_type, operating_system):
    environment = _create_environment_object(build_type, operating_system)
    response = EnvironmentsApi(apiclient).createNew(body=environment)
    print(pretty_format_response(response.json()))

def update_environment():
    pass

def delete_environment():
    pass

def get_environment():
    pass

def list_environments():
    response = EnvironmentsApi(apiclient).getAll()
    print(pretty_format_response(response.json()))

@arg('-n', '--name', help='Name of the build configuration to trigger')
@arg('-i', '--id', help='ID of the build configuration to trigger')
def build(name=None,id=None):
    "Trigger a build configuration giving either the name or ID."
    if id:
        if (_build_configuration_exists(id)):
            print(pretty_format_response(BuildconfigurationsApi(apiclient).trigger(id=id).json()))
        else:
            print 'There is no build configuration with id {0}.'.format(id)
    elif name:
        build_id = _get_build_configuration_id_by_name(name)
        if build_id:
            print(pretty_format_response(BuildconfigurationsApi(apiclient).trigger(id=build_id).json()))
        else:
            print 'There is no build configuration with name {0}.'.format(name)
    else:
        print 'Build requires either a name or an ID of a build configuration to trigger.'


def create_build_configuration(name, project_id, environment, description='', scm_url='', scm_revision='', patches_url='',
                               build_script=''):
    #check for existing project_ids, fail out if the project id doesn't exist
    build_configuration = _create_build_configuration(name, project_id, environment, description, scm_url, scm_revision, patches_url, build_script)
    response = pretty_format_response(BuildconfigurationsApi(apiclient).createNew(body=build_configuration).json())
    print(response)

parser = argh.ArghParser()
parser.add_commands([create_product,
                     update_product,
                     get_product,
                     list_products,
                     create_project,
                     delete_project,
                     update_project,
                    # get_project,
                     list_projects,
                     create_license,
                     #update_license,
                    # get_license,
                     list_licenses,
                     create_build_configuration,
                   #  update_build_configuration,
                     list_build_configurations,
                     list_environments,
                     create_environment,
                     build],
                    func_kwargs={'formatter_class': PNCFormatter})
parser.autocomplete()

if __name__ == '__main__':
    parser.dispatch()