import argparse

from argh import arg

import logging
import re
from pnc_cli import utils

from pnc_cli import swagger_client
from pnc_cli.swagger_client.apis.buildconfigurations_api import BuildconfigurationsApi
from pnc_cli.swagger_client.apis.environments_api import EnvironmentsApi
from pnc_cli.swagger_client.apis.projects_api import ProjectsApi
from pnc_cli import products
from pnc_cli import productversions
from pnc_cli import projects
from pnc_cli import environments

projects_api = ProjectsApi(utils.get_api_client())
envs_api = EnvironmentsApi(utils.get_api_client())
configs_api = BuildconfigurationsApi(utils.get_api_client())
bc_name_regex = "^[a-zA-Z0-9_.][a-zA-Z0-9_.-]*(?!\.git)+$"

def create_build_conf_object(**kwargs):
    created_build_configuration = swagger_client.BuildConfigurationRest()
    for key, value in kwargs.items():
        setattr(created_build_configuration, str(key), value)
    return created_build_configuration


def get_build_configuration_id_by_name(name):
    """
    Returns the id of the build configuration matching name
    :param name: name of build configuration
    :return: id of the matching build configuration, or None if no match found
    """
    response = utils.checked_api_call(configs_api, 'get_all', q='name==' + name).content
    if not response:
        return None
    return response[0].id


def config_id_exists(search_id):
    """
    Test if a build configuration matching search_id exists
    :param search_id: id to test for
    :return: True if a build configuration with search_id exists, False otherwise
    """
    response = utils.checked_api_call(configs_api, 'get_specific', id=search_id)
    if not response:
        return False
    return True


def get_config_id(search_id, name):
    """
    Given an ID or name, checks for existence then returns an ID
    :param search_id: ID to check for existence
    :param name: name to map to ID
    :return: Valid ID if it exists. None otherwise
    """
    if search_id:
        if not config_id_exists(search_id):
            logging.error("No BuildConfiguration with ID {} exists.".format(search_id))
            return
        config_id = search_id
    elif name:
        config_id = get_build_configuration_id_by_name(name)
        if not config_id:
            logging.error("No BuildConfiguration with the name {} exists.".format(name))
            return
    else:
        logging.error("Either a name or an ID of a BuildConfiguration is required.")
        return
    return config_id

def _valid_name(name_input):
    pattern = re.compile(bc_name_regex)
    if not pattern.match(name_input):
        raise argparse.ArgumentTypeError("name contains invalid characters")
    return name_input

def _unique_name(name_input):
    response = utils.checked_api_call(configs_api, 'get_all', q='name=='+name_input)
    if response.content:
        raise argparse.ArgumentTypeError("name is already in use")
    return name_input

def _valid_unique_name(name_input):
    _unique_name(_valid_name(name_input))
    return name_input


def _valid_existing_name(name_input):
    _valid_name(name_input)
    if not get_build_configuration_id_by_name(name_input):
        raise argparse.ArgumentTypeError("no BuildConfiguration with the name {} exists.".format(name_input))
    return name_input

def _valid_id(id_input):
    if not id_input.isdigit():
        raise argparse.ArgumentTypeError("an ID must be a positive integer")
    return id_input

def _existing_id(id_input):
    _valid_id(id_input)
    if not config_id_exists(id_input):
        raise argparse.ArgumentTypeError("no BuildConfiguration with ID {} exists.".format(id_input))
    return id_input


@arg("-i", "--id", help="ID of the BuildConfiguration to trigger.", type=_existing_id)
@arg("-n", "--name", help="Name of the BuildConfiguration to trigger.", type=_valid_existing_name)
def build(id=None, name=None):
    """
    Trigger a BuildConfiguration by name or ID
    """
    trigger_id = id
    if name:
        trigger_id = get_build_configuration_id_by_name(name)

    response = utils.checked_api_call(configs_api, 'trigger', id=trigger_id)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfiguration to retrieve.", type=_existing_id)
@arg("-n", "--name", help="Name of the BuildConfiguration to retrieve.", type=_valid_existing_name)
def get_build_configuration(id=None, name=None):
    """
    Retrieve a specific BuildConfiguration
    """
    found_id = id
    if name:
        found_id = get_build_configuration_id_by_name(name)

    response = utils.checked_api_call(configs_api, 'get_specific', id=found_id)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfiguration to update.", type=_existing_id)
@arg("-n", "--name", help="Name of the BuildConfiguration to update.", type=_valid_unique_name)
# allow specifying project by name?
@arg("-pid", "--project", help="ID of the Project to associate the BuildConfiguration with.", type=int)
@arg("-e", "--environment", help="ID of the Environment for the new BuildConfiguration.", type=int)
@arg("-d", "--description", help="Description of the new build configuration.")
@arg("-surl", "--scm-url", help="URL to the sources of the BuildConfiguration.")
@arg("-srev", "--scm-revision", help="Revision of the sources in scm-url for this BuildConfiguration.")
@arg("-bs", "--build-script", help="Script to execute for the BuildConfiguration.")
def update_build_configuration(id=None, name=None, **kwargs):
    """
    Update an existing BuildConfiguration with new information

    :param id: ID of BuildConfiguration to update
    :param name: Name of BuildConfiguration to update
    :return:
    """
    to_update_id = get_config_id(id, name)
    if not to_update_id:
        return

    bc_to_update = configs_api.get_specific(id=to_update_id).content

    project_id = kwargs.get('project')
    if project_id:
        project_rest = projects.get_project(id=project_id)
        if not project_rest:
            return
        update_project = {'project': project_rest}
        kwargs.update(update_project)

    env_id = kwargs.get('environment')
    if env_id:
        env_rest = environments.get_environment(id=env_id)
        if not env_rest:
            return
        update_env = {'environment': env_rest}
        kwargs.update(update_env)

    for key, value in kwargs.items():
        if value is not None:
            setattr(bc_to_update, key, value)

    response = utils.checked_api_call(configs_api, 'update', id=to_update_id, body=bc_to_update)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfiguration to delete.", type=int)
@arg("-n", "--name", help="Name of the BuildConfiguration to delete.", type=_valid_name)
def delete_build_configuration(id=None, name=None):
    """
    Delete an existing BuildConfiguration
    :param id:
    :param name:
    :return:
    """

    to_delete_id = get_config_id(id, name)
    if not to_delete_id:
        return

    #ensure that this build configuration is not a dependency of any other build configuration.
    isDep = False
    for config in list_build_configurations():
        dep_ids = [str(val) for val in config.dependency_ids]
        if dep_ids is not None and to_delete_id in dep_ids:
            isDep = True
            logging.error("BuildConfiguration ID {} is a dependency of BuildConfiguration {}.".format(to_delete_id, config.name))


    if not isDep:
        response = utils.checked_api_call(configs_api, 'delete_specific', id=to_delete_id)
        if response:
            return response.content
    else:
        logging.warn("No action taken.")


@arg("name", help="Name for the new BuildConfiguration.", type=_valid_name)
# allow specifying project by name?
@arg("project", help="ID of the Project to associate the BuildConfiguration with.")
@arg("environment", help="ID of the Environment for the new BuildConfiguration.")
@arg("scm_repo_url", help="URL to the sources of the BuildConfiguration.")
@arg("scm_revision", help="Revision of the sources in scm-url for this BuildConfiguration.")
@arg("build_script", help="Script to execute for the BuildConfiguration.")
@arg("-d", "--description", help="Description of the new build configuration.")
@arg("-pvi", "--product-version-id", help="Associated ProductVersion ID.")
@arg("-dids", "--dependency-ids", type=int, nargs="+", help="List of BuildConfiguration IDs that are dependencies of this BuildConfiguration.")
#@arg("-bcsid", "--")
def create_build_configuration(**kwargs):
    """
    Create a new BuildConfiguration. BuildConfigurations represent the settings and configuration required to run a build of a specific version of the associated Project's source code.
    If a ProductVersion ID is provided, the BuildConfiguration will have access to artifacts which were produced for that version, but may not have been released yet.
    """
    project_id = kwargs.get('project')
    project_rest = projects.get_project(id=project_id)
    if not project_rest:
        return
    kwargs['project'] = project_rest
    env_id = kwargs.get('environment')
    env_rest = environments.get_environment(id=env_id)
    if not env_rest:
        return
    kwargs['environment'] = env_rest

    build_configuration = create_build_conf_object(**kwargs)
    response = utils.checked_api_call(
        configs_api, 'create_new', body=build_configuration)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the Product to list BuildConfigurations for.", type=int)
@arg("-n", "--name", help="Name of the Product to list BuildConfigurations for.", type=_valid_name)
@arg("-p", "--page-size", help="Limit the amount of build records returned", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_build_configurations_for_product(id=None, name=None, page_size=200, sort="", q=""):
    """
    List all BuildConfigurations associated with the given Product.
    """
    found_id = products.get_product_id(id, name)
    if not found_id:
        return

    response = utils.checked_api_call(configs_api, 'get_all_by_product_id', product_id=found_id, page_size=page_size,
                                      sort=sort, q=q)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the Project to list BuildConfigurations for.", type=int)
@arg("-n", "--name", help="Name of the Project to list BuildConfigurations for.", type=_valid_name)
@arg("-p", "--page-size", help="Limit the amount of build records returned", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_build_configurations_for_project(id=None, name=None, page_size=200, sort="", q=""):
    """
    List all BuildConfigurations associated with the given Project.
    """
    found_id = projects.get_project_id(id, name)
    if not found_id:
        return

    response = utils.checked_api_call(configs_api, 'get_all_by_project_id', project_id=found_id, page_size=page_size,
                                      sort=sort, q=q)
    if response:
        return response.content


# TODO: allow specifying product name / version 'version'?
@arg("product_id", help="ID of the Product which contains the desired ProductVersion.", type=int)
@arg("version_id", help="ID of the ProductVersion to list BuildConfigurations for.", type=int)
@arg("-p", "--page-size", help="Limit the amount of build records returned")
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_build_configurations_for_product_version(product_id, version_id, page_size=20, sort="", q=""):
    """
    List all BuildConfigurations associated with the given ProductVersion
    """
    found_product_id = products.get_product_id(product_id, None)
    if not found_product_id:
        return

    if not productversions.version_exists(version_id):
        logging.error("No ProductVersion with ID {} exists.".format(version_id))
        return

    response = utils.checked_api_call(configs_api, 'get_all_by_product_version_id', product_id=found_product_id,
                                      version_id=version_id, page_size=page_size, sort=sort, q=q)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfiguration to list dependencies for.", type=int)
@arg("-n", "--name", help="Name of the BuildConfiguration to list dependencies for.", type=_valid_name)
@arg("-p", "--page-size", help="Limit the amount of build records returned")
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_dependencies(id=None, name=None, page_size=200, sort="", q=""):
    found_id = get_config_id(id, name)
    if not found_id:
        return

    response = utils.checked_api_call(configs_api, 'get_dependencies', id=found_id, page_size=page_size, sort=sort, q=q)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfiguration to add a dependency to.", type=int)
@arg("-n", "--name", help="Name of the BuildConfiguration to add a dependency to.", type=_valid_name)
@arg("-di", "--dependency-id", help="ID of an existing BuildConfiguration to add as a dependency.", type=int)
@arg("-dn", "--dependency-name", help="Name of an existing BuildConfiguration to add as a dependency.", type=_valid_name)
def add_dependency(id=None, name=None, dependency_id=None, dependency_name=None):
    """
    Add an existing BuildConfiguration as a dependency to another BuildConfiguration.
    """
    if not id and not name:
        logging.error("Please provide the name or ID of the BuildConfiguration to add a dependency to.")
        return;
    add_to = get_config_id(id, name)
    if not add_to:
        return

    if not dependency_id and not dependency_name:
        logging.error("Please provide the name or ID of the BuildConfiguration to add as a dependency.")
        return
    to_add = get_config_id(dependency_id, dependency_name)
    if not to_add:
        return

    dependency = configs_api.get_specific(id=to_add).content
    response = utils.checked_api_call(configs_api, 'add_dependency', id=add_to, body=dependency)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfiguration to remove a dependency from.", type=int)
@arg("-n", "--name", help="Name of the BuildConfiguration to remove a dependency from.", type=_valid_name)
@arg("-di", "--dependency-id", help="ID of the dependency BuildConfiguration to remove.", type=int)
@arg("-dn", "--dependency-name", help="Name of the dependency BuildConfiguration to remove.", type=_valid_name)
def remove_dependency(id=None, name=None, dependency_id=None, dependency_name=None):
    """
    Remove a BuildConfiguration from the dependency list of another BuildConfiguration
    """

    if not id and not name:
        logging.error("Please provide the name or ID of the BuildConfiguration to remove a dependency from.")
        return;
    found_id = get_config_id(id, name)
    if not found_id:
        return

    if not dependency_id and not dependency_name:
        logging.error("Please provide the name or ID of the BuildConfiguration to remove as a dependency.")
        return
    found_dep_id = get_config_id(dependency_id, dependency_name)
    if not found_dep_id:
        return

    response = utils.checked_api_call(configs_api, 'remove_dependency', id=found_id, dependency_id=found_dep_id)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfiguration to list ProductVersions for.", type=int)
@arg("-n", "--name", help="Name of the BuildConfiguration to list ProductVersions for.", type=_valid_name)
@arg("-p", "--page-size", help="Limit the amount of build records returned", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_product_versions_for_build_configuration(id=None, name=None, page_size=200, sort="", q=""):
    """
    List all ProductVersions associated with a BuildConfiguration
    """
    found_id = get_config_id(id, name)
    if not found_id:
        return

    response = utils.checked_api_call(configs_api, 'get_product_versions', id=found_id, page_size=page_size, sort=sort,
                                      q=q)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfiguration to add a ProductVersion to.", type=int)
@arg("-n", "--name", help="Name of the BuildConfiguration to add a ProductVersions to.", type=_valid_name)
@arg('product_version_id', help="ID of the ProductVersion to add.")
def add_product_version_to_build_configuration(id=None, name=None, product_version_id=None):
    """
    Associate an existing ProductVersion with a BuildConfiguration
    """
    found_id = get_config_id(id, name)
    if not found_id:
        return

    if not productversions.version_exists(product_version_id):
        logging.error("No ProductVersion with ID {} exists.".format(product_version_id))
        return

    to_add = productversions.get_product_version(id=product_version_id)
    response = utils.checked_api_call(configs_api, 'add_product_version', id=found_id, body=to_add)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfiguration to remove a ProductVersion from.", type=int)
@arg("-n", "--name", help="Name of the BuildConfiguration to remove a ProductVersions from.", type=_valid_name)
@arg('product_version_id', help="ID of the ProductVersion to remove.")
def remove_product_version_from_build_configuration(id=None, name=None, product_version_id=None):
    """
    Remove a ProductVersion from association with a BuildConfiguration
    """
    found_id = get_config_id(id, name)
    if not found_id:
        return

    if product_version_id not in [x.id for x in configs_api.get_product_versions(id=found_id).content]:
        logging.error("The specified ProductVersion is not associated with BuildConfiguration {}.".format(found_id))
        return

    response = utils.checked_api_call(configs_api, 'remove_product_version', id=found_id,
                                      product_version_id=product_version_id)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfiguration to list audited revisions for.", type=int)
@arg("-n", "--name", help="Name of the BuildConfiguration to list audited revisions for.", type=_valid_name)
@arg("-p", "--page-size", help="Limit the amount of build records returned", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
# TODO: PNC return BuildConfigurationAuditedPage instead of BuildConfigurationPage?
def list_revisions_of_build_configuration(id=None, name=None, page_size=200, sort=""):
    """
    List audited revisions of a BuildConfiguration
    """
    found_id = get_config_id(id, name)
    if not found_id:
        return

    response = utils.checked_api_call(configs_api, 'get_revisions', id=found_id, page_size=page_size, sort=sort)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfiguration to retrieve a revision from.", type=int)
@arg("-n", "--name", help="Name of the BuildConfiguration to retrieve a revision from.", type=_valid_name)
@arg("--revision_id", help="Number of the revision to retrieve.")
def get_revision_of_build_configuration(id=None, name=None, revision_id=None):
    """
    Get a specific audited revision of a BuildConfiguration
    """
    found_id = get_config_id(id, name)
    if not found_id:
        return

    response = utils.checked_api_call(configs_api, 'get_revision', id=found_id, rev=revision_id)
    if response:
        return response.content


@arg("-p", "--page-size", help="Limit the amount of build records returned", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_build_configurations(page_size=200, sort="", q=""):
    """
    List all BuildConfigurations
    """
    response = utils.checked_api_call(configs_api, 'get_all', page_size=page_size, sort=sort, q=q)
    if response:
        return response.content
