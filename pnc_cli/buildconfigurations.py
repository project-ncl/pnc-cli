from argh import arg
from argh.exceptions import CommandError

import pnc_cli.common as common
import pnc_cli.cli_types as types
from pnc_cli import swagger_client
from pnc_cli import utils
from pnc_cli.swagger_client import BuildconfigurationsApi
from pnc_cli.swagger_client import RepositoryconfigurationsApi
from pnc_cli.swagger_client import EnvironmentsApi
from pnc_cli.swagger_client import ProductsApi
from pnc_cli.swagger_client import ProductversionsApi
from pnc_cli.swagger_client import ProjectsApi
import pnc_cli.user_config as uc

projects_api = ProjectsApi(uc.user.get_api_client())
configs_api = BuildconfigurationsApi(uc.user.get_api_client())
repos_api = RepositoryconfigurationsApi(uc.user.get_api_client())
envs_api = EnvironmentsApi(uc.user.get_api_client())
versions_api = ProductversionsApi(uc.user.get_api_client())
products_api = ProductsApi(uc.user.get_api_client())


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

def get_build_configuration_by_name(name):
    """
    Returns the build configuration matching the name
    :param name: name of build configuration
    :return: The matching build configuration, or None if no match found
    """
    response = utils.checked_api_call(configs_api, 'get_all', q='name==' + name).content
    if not response:
        return None
    return response[0]


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


@arg("-i", "--id", help="ID of the BuildConfiguration to trigger.", type=types.existing_bc_id)
@arg("-n", "--name", help="Name of the BuildConfiguration to trigger.", type=types.existing_bc_name)
def build(id=None, name=None):
    """
    Trigger a BuildConfiguration by name or ID
    """
    trigger_id = common.set_id(configs_api, id, name)

    response = utils.checked_api_call(configs_api, 'trigger', id=trigger_id)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfiguration to retrieve.", type=types.existing_bc_id)
@arg("-n", "--name", help="Name of the BuildConfiguration to retrieve.", type=types.existing_bc_name)
def get_build_configuration(id=None, name=None):
    """
    Retrieve a specific BuildConfiguration
    """
    found_id = common.set_id(configs_api, id, name)

    response = utils.checked_api_call(configs_api, 'get_specific', id=found_id)
    if response:
        return response.content


@arg("id", help="ID of the BuildConfiguration to update.", type=types.existing_bc_id)
@arg("-n", "--name", help="Name of the BuildConfiguration to update.", type=types.valid_unique_bc_name)
@arg("-pid", "--project", help="ID of the Project to associate the BuildConfiguration with.",
     type=types.existing_project_id)
@arg("-e", "--environment", help="ID of the Environment for the new BuildConfiguration.",
     type=types.existing_environment_id)
@arg("-d", "--description", help="Description of the new build configuration.")
@arg("-r", "--repository-configuration", help="ID of the RepositoryConfiguration for the BuildConfiguration.")
@arg("-pvi", "--product-version-id", help="Associated ProductVersion ID.")
@arg("-srev", "--scm-revision", help="Revision of the sources in scm-url for this BuildConfiguration.")
@arg("-bs", "--build-script", help="Script to execute for the BuildConfiguration.")
def update_build_configuration(id, **kwargs):
    """
    Update an existing BuildConfiguration with new information

    :param id: ID of BuildConfiguration to update
    :param name: Name of BuildConfiguration to update
    :return:
    """
    to_update_id = id

    bc_to_update = configs_api.get_specific(id=to_update_id).content

    project_id = kwargs.get('project')
    if project_id:
        project_rest = common.get_entity(projects_api, project_id)
        update_project = {'project': project_rest}
        kwargs.update(update_project)

    repository_id = kwargs.get('repository_configuration')
    if repository_id:
        repository_rest = common.get_entity(repos_api, repository_id)
        update_repository = {'repository_configuration': repository_rest}
        kwargs.update(update_repository)

    env_id = kwargs.get('environment')
    if env_id:
        env_rest = common.get_entity(envs_api, env_id)
        update_env = {'environment': env_rest}
        kwargs.update(update_env)

    for key, value in kwargs.items():
        if value is not None:
            setattr(bc_to_update, key, value)

    response = utils.checked_api_call(configs_api, 'update', id=to_update_id, body=bc_to_update)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfiguration to delete.", type=types.existing_bc_id)
@arg("-n", "--name", help="Name of the BuildConfiguration to delete.", type=types.existing_bc_name)
def delete_build_configuration(id=None, name=None):
    """
    Delete an existing BuildConfiguration
    :param id:
    :param name:
    :return:
    """

    to_delete_id = common.set_id(configs_api, id, name)
    # ensure that this build configuration is not a dependency of any other build configuration.
    # list_build_configurations is an insufficient check because eventually there will be too many entities to check them all.
    # a better REST method for dependency checking is needed
    for config in list_build_configurations(page_size=1000000000):
        dep_ids = [str(val) for val in config.dependency_ids]
        if dep_ids is not None and str(to_delete_id) in dep_ids:
            raise CommandError(
                "BuildConfiguration ID {} is a dependency of BuildConfiguration {}.".format(to_delete_id, config.name))

    response = utils.checked_api_call(configs_api, 'delete_specific', id=to_delete_id)
    if response:
        return response.content


@arg("name", help="Name for the new BuildConfiguration.", type=types.valid_bc_name)
# allow specifying project by name?
@arg("project", help="ID of the Project to associate the BuildConfiguration with.", type=types.existing_project_id)
@arg("environment", help="ID of the Environment for the new BuildConfiguration.",
     type=types.existing_environment_id)
@arg("repository_configuration", help="ID of the RepositoryConfiguration with the sources of the BuildConfiguration.")
@arg("scm_revision", help="Revision of the sources in scm-url for this BuildConfiguration.")
@arg("build_script", help="Script to execute for the BuildConfiguration.")
@arg("-d", "--description", help="Description of the new build configuration.")
@arg("-pvi", "--product-version-id", help="Associated ProductVersion ID.")
@arg("-dids", "--dependency-ids", type=int, nargs="+",
     help="List of BuildConfiguration IDs that are dependencies of this BuildConfiguration.")
# @arg("-bcsid", "--")
def create_build_configuration(**kwargs):
    """
    Create a new BuildConfiguration. BuildConfigurations represent the settings and configuration required to run a build of a specific version of the associated Project's source code.
    If a ProductVersion ID is provided, the BuildConfiguration will have access to artifacts which were produced for that version, but may not have been released yet.
    """
    project_id = kwargs.get('project')
    project_rest = common.get_entity(projects_api, project_id)
    kwargs['project'] = project_rest
    repository_id = kwargs.get('repository_configuration')
    repository_rest = common.get_entity(repos_api, repository_id)
    kwargs['repository_configuration'] = repository_rest
    env_id = kwargs.get('environment')
    env_rest = common.get_entity(envs_api, env_id)
    kwargs['environment'] = env_rest

    build_configuration = create_build_conf_object(**kwargs)
    response = utils.checked_api_call(
        configs_api, 'create_new', body=build_configuration)
    if response:
        return utils.format_json(response.content)


@arg("-i", "--id", help="ID of the Product to list BuildConfigurations for.", type=types.existing_product_id)
@arg("-n", "--name", help="Name of the Product to list BuildConfigurations for.", type=types.existing_bc_name)
@arg("-p", "--page-size", help="Limit the amount of build records returned", type=int)
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_build_configurations_for_product(id=None, name=None, page_size=200, page_index=0, sort="", q=""):
    """
    List all BuildConfigurations associated with the given Product.
    """
    found_id = common.set_id(products_api, id, name)
    response = utils.checked_api_call(configs_api, 'get_all_by_product_id', product_id=found_id, page_size=page_size, page_index=page_index,
                                      sort=sort, q=q)
    if response:
        return utils.format_json_list(response.content)


@arg("-i", "--id", help="ID of the Project to list BuildConfigurations for.", type=int)
@arg("-n", "--name", help="Name of the Project to list BuildConfigurations for.", type=types.valid_bc_name)
@arg("-p", "--page-size", help="Limit the amount of build records returned", type=int)
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_build_configurations_for_project(id=None, name=None, page_size=200, page_index=0, sort="", q=""):
    """
    List all BuildConfigurations associated with the given Project.
    """
    found_id = common.set_id(projects_api, id, name)
    response = utils.checked_api_call(configs_api, 'get_all_by_project_id', project_id=found_id, page_size=page_size, page_index=page_index,
                                      sort=sort, q=q)
    if response:
        return utils.format_json_list(response.content)


@arg("product_id", help="ID of the Product which contains the desired ProductVersion.",
     type=types.existing_product_id)
@arg("version_id", help="ID of the ProductVersion to list BuildConfigurations for.",
     type=types.existing_product_version)
@arg("-p", "--page-size", help="Limit the amount of build records returned")
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_build_configurations_for_product_version(product_id, version_id, page_size=200, page_index=0, sort="", q=""):
    """
    List all BuildConfigurations associated with the given ProductVersion
    """
    found_product_id = common.set_id(products_api, product_id, None)
    response = utils.checked_api_call(configs_api, 'get_all_by_product_version_id', product_id=found_product_id,
                                      version_id=version_id, page_size=page_size, page_index=page_index, sort=sort, q=q)
    if response:
        return utils.format_json_list(response.content)


@arg("-i", "--id", help="ID of the BuildConfiguration to list dependencies for.", type=types.existing_bc_id)
@arg("-n", "--name", help="Name of the BuildConfiguration to list dependencies for.", type=types.valid_bc_name)
@arg("-p", "--page-size", help="Limit the amount of build records returned")
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_dependencies(id=None, name=None, page_size=200, page_index=0, sort="", q=""):
    found_id = common.set_id(configs_api, id, name)
    response = utils.checked_api_call(configs_api, 'get_dependencies', id=found_id, page_size=page_size, page_index=page_index, sort=sort, q=q)
    if response:
        return utils.format_json_list(response.content)


@arg("-i", "--id", help="ID of the BuildConfiguration to add a dependency to.", type=types.existing_bc_id)
@arg("-n", "--name", help="Name of the BuildConfiguration to add a dependency to.", type=types.existing_bc_name)
@arg("-di", "--dependency-id", help="ID of an existing BuildConfiguration to add as a dependency.",
     type=types.existing_bc_id)
@arg("-dn", "--dependency-name", help="Name of an existing BuildConfiguration to add as a dependency.",
     type=types.existing_bc_name)
def add_dependency(id=None, name=None, dependency_id=None, dependency_name=None):
    """
    Add an existing BuildConfiguration as a dependency to another BuildConfiguration.
    """
    add_to = common.set_id(configs_api, id, name)
    to_add = common.set_id(configs_api, dependency_id, dependency_name)

    dependency = configs_api.get_specific(id=to_add).content
    response = utils.checked_api_call(configs_api, 'add_dependency', id=add_to, body=dependency)
    if response:
        return utils.format_json(response.content)


@arg("-i", "--id", help="ID of the BuildConfiguration to remove a dependency from.", type=types.existing_bc_id)
@arg("-n", "--name", help="Name of the BuildConfiguration to remove a dependency from.", type=types.existing_bc_name)
@arg("-di", "--dependency-id", help="ID of the dependency BuildConfiguration to remove.", type=types.existing_bc_id)
@arg("-dn", "--dependency-name", help="Name of the dependency BuildConfiguration to remove.",
     type=types.existing_bc_name)
def remove_dependency(id=None, name=None, dependency_id=None, dependency_name=None):
    """
    Remove a BuildConfiguration from the dependency list of another BuildConfiguration
    """

    found_id = common.set_id(configs_api, id, name)
    found_dep_id = common.set_id(configs_api, dependency_id, dependency_name)

    response = utils.checked_api_call(configs_api, 'remove_dependency', id=found_id, dependency_id=found_dep_id)
    if response:
        return utils.format_json(response.content)


@arg("-i", "--id", help="ID of the BuildConfiguration to list ProductVersions for.", type=types.existing_bc_id)
@arg("-n", "--name", help="Name of the BuildConfiguration to list ProductVersions for.", type=types.existing_bc_name)
@arg("-p", "--page-size", help="Limit the amount of build records returned", type=int)
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_product_versions_for_build_configuration(id=None, name=None, page_size=200, page_index=0, sort="", q=""):
    """
    List all ProductVersions associated with a BuildConfiguration
    """
    found_id = common.set_id(configs_api, id, name)
    response = utils.checked_api_call(configs_api, 'get_product_versions', id=found_id, page_size=page_size, page_index=page_index, sort=sort,
                                      q=q)
    if response:
        return utils.format_json_list(response.content)


@arg("-i", "--id", help="ID of the BuildConfiguration to add a ProductVersion to.", type=types.existing_bc_id)
@arg("-n", "--name", help="Name of the BuildConfiguration to add a ProductVersions to.", type=types.existing_bc_name)
@arg('product_version_id', help="ID of the ProductVersion to add.", type=types.existing_product_version)
def add_product_version_to_build_configuration(id=None, name=None, product_version_id=None):
    """
    Associate an existing ProductVersion with a BuildConfiguration
    """
    found_id = common.set_id(configs_api, id, name)

    to_add = common.get_entity(versions_api, product_version_id)
    response = utils.checked_api_call(configs_api, 'add_product_version', id=found_id, body=to_add)
    if response:
        return utils.format_json(response.content)


@arg("-i", "--id", help="ID of the BuildConfiguration to remove a ProductVersion from.", type=types.existing_bc_id)
@arg("-n", "--name", help="Name of the BuildConfiguration to remove a ProductVersions from.",
     type=types.existing_bc_name)
@arg('product_version_id', help="ID of the ProductVersion to remove.", type=types.existing_product_version)
def remove_product_version_from_build_configuration(id=None, name=None, product_version_id=None):
    """
    Remove a ProductVersion from association with a BuildConfiguration
    """
    found_id = common.set_id(configs_api, id, name)
    response = utils.checked_api_call(configs_api, 'remove_product_version', id=found_id,
                                      product_version_id=product_version_id)
    if response:
        return utils.format_json(response.content)


@arg("-i", "--id", help="ID of the BuildConfiguration to list audited revisions for.", type=types.existing_bc_id)
@arg("-n", "--name", help="Name of the BuildConfiguration to list audited revisions for.", type=types.existing_bc_name)
@arg("-p", "--page-size", help="Limit the amount of build records returned", type=int)
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
# TODO: PNC return BuildConfigurationAuditedPage instead of BuildConfigurationPage?
def list_revisions_of_build_configuration(id=None, name=None, page_size=200, page_index=0, sort=""):
    """
    List audited revisions of a BuildConfiguration
    """
    found_id = common.set_id(configs_api, id, name)
    response = utils.checked_api_call(configs_api, 'get_revisions', id=found_id, page_size=page_size, page_index=page_index, sort=sort)
    if response:
        return utils.format_json_list(response.content)


@arg("-i", "--id", help="ID of the BuildConfiguration to retrieve a revision from.", type=types.existing_bc_id)
@arg("-n", "--name", help="Name of the BuildConfiguration to retrieve a revision from.", type=types.existing_bc_name)
@arg("--revision_id", help="Number of the revision to retrieve.")
def get_revision_of_build_configuration(id=None, name=None, revision_id=None):
    """
    Get a specific audited revision of a BuildConfiguration
    """
    found_id = common.set_id(configs_api, id, name)
    response = utils.checked_api_call(configs_api, 'get_revision', id=found_id, rev=revision_id)
    if response:
        return utils.format_json(response.content)


@arg("-p", "--page-size", help="Limit the amount of build records returned", type=int)
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_build_configurations(page_size=200, page_index=0, sort="", q=""):
    """
    List all BuildConfigurations
    """
    response = utils.checked_api_call(configs_api, 'get_all', page_size=page_size, page_index=page_index, sort=sort, q=q)
    if response:
        return utils.format_json_list(response.content)
