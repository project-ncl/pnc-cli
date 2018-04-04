from argh import arg
from argh.exceptions import CommandError

import ast
import pnc_cli.common as common
import pnc_cli.cli_types as types
from pnc_cli import swagger_client
from pnc_cli import utils
from pnc_cli.pnc_api import pnc_api

import sys


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
    response = utils.checked_api_call(pnc_api.build_configs, 'get_all', q='name==' + name).content
    if not response:
        return None
    return response[0].id


def get_build_configuration_by_name(name):
    """
    Returns the build configuration matching the name
    :param name: name of build configuration
    :return: The matching build configuration, or None if no match found
    """
    response = utils.checked_api_call(pnc_api.build_configs, 'get_all', q='name==' + name).content
    if not response:
        return None
    return response[0]


def config_id_exists(search_id):
    """
    Test if a build configuration matching search_id exists
    :param search_id: id to test for
    :return: True if a build configuration with search_id exists, False otherwise
    """
    response = utils.checked_api_call(pnc_api.build_configs, 'get_specific', id=search_id)
    if not response:
        return False
    return True


@arg("-i", "--id", help="ID of the BuildConfiguration to trigger.", type=types.existing_bc_id)
@arg("-n", "--name", help="Name of the BuildConfiguration to trigger.", type=types.existing_bc_name)
@arg("--temporary-build", help="Temporary build")
@arg("--timestamp-alignment", help="Enable timestamp alignment for temporary build")
@arg("--no-build-dependencies", help="Don't build dependencies of this build configuration")
@arg("--keep-pod-on-failure", help="Keep pod on failure")
@arg("-f", "--force-rebuild", help="Force Rebuild")
def build(id=None, name=None,
          temporary_build=False, timestamp_alignment=False,
          no_build_dependencies=False,
          keep_pod_on_failure=False,
          force_rebuild=False):
    """
    Trigger a BuildConfiguration by name or ID
    """
    data = build_raw(id, name, temporary_build, timestamp_alignment, no_build_dependencies,
              keep_pod_on_failure, force_rebuild)
    if data:
        return utils.format_json(data)

def build_raw(id=None, name=None,
          temporary_build=False, timestamp_alignment=False,
          no_build_dependencies=False,
          keep_pod_on_failure=False,
          force_rebuild=False):
    if temporary_build is False and timestamp_alignment is True:
        print("Error: You can only activate timestamp alignment with the temporary build flag!")
        sys.exit(1)

    trigger_id = common.set_id(pnc_api.build_configs, id, name)


    response = utils.checked_api_call(pnc_api.build_configs, 'trigger',
                                      id=trigger_id,
                                      temporary_build=temporary_build,
                                      timestamp_alignment=timestamp_alignment,
                                      build_dependencies=not no_build_dependencies,
                                      keep_pod_on_failure=keep_pod_on_failure,
                                      force_rebuild=force_rebuild)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfiguration to retrieve.", type=types.existing_bc_id)
@arg("-n", "--name", help="Name of the BuildConfiguration to retrieve.", type=types.existing_bc_name)
def get_build_configuration(id=None, name=None):
    """
    Retrieve a specific BuildConfiguration
    """
    data = get_build_configuration_raw(id, name)
    if data:
        return utils.format_json(data)

def get_build_configuration_raw(id=None, name=None):
    found_id = common.set_id(pnc_api.build_configs, id, name)
    response = utils.checked_api_call(pnc_api.build_configs, 'get_specific', id=found_id)
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
@arg("-gp", "--generic-parameters", help="Set of arbitrary additional key=value pairs, such as CUSTOM_PME_PARAMETERS")
def update_build_configuration(id, **kwargs):
    """
    Update an existing BuildConfiguration with new information

    :param id: ID of BuildConfiguration to update
    :param name: Name of BuildConfiguration to update
    :return:
    """
    data = update_build_configuration_raw(id, **kwargs)
    if data:
        return utils.format_json(data)

def update_build_configuration_raw(id, **kwargs):
    to_update_id = id

    bc_to_update = pnc_api.build_configs.get_specific(id=to_update_id).content

    project_id = kwargs.get('project')
    if project_id:
        project_rest = common.get_entity(pnc_api.projects, project_id)
        update_project = {'project': project_rest}
        kwargs.update(update_project)

    repository_id = kwargs.get('repository_configuration')
    if repository_id:
        repository_rest = common.get_entity(pnc_cli.repositories, repository_id)
        update_repository = {'repository_configuration': repository_rest}
        kwargs.update(update_repository)

    env_id = kwargs.get('environment')
    if env_id:
        env_rest = common.get_entity(pnc_api.environments, env_id)
        update_env = {'environment': env_rest}
        kwargs.update(update_env)

    if isinstance(kwargs.get("generic_parameters"), str):
        kwargs["generic_parameters"] = ast.literal_eval(kwargs.get("generic_parameters"))

    for key, value in kwargs.items():
        if value is not None:
            setattr(bc_to_update, key, value)

    response = utils.checked_api_call(pnc_api.build_configs, 'update', id=to_update_id, body=bc_to_update)
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
    data = delete_build_configuration_raw(id, name)
    if data:
        return utils.format_json(data)

def delete_build_configuration_raw(id=None, name=None):
    to_delete_id = common.set_id(pnc_api.build_configs, id, name)
    # ensure that this build configuration is not a dependency of any other build configuration.
    # list_build_configurations is an insufficient check because eventually there will be too many entities to check them all.
    # a better REST method for dependency checking is needed
    for config in list_build_configurations_raw(page_size=1000000000):
        dep_ids = [str(val) for val in config.dependency_ids]
        if dep_ids is not None and str(to_delete_id) in dep_ids:
            raise CommandError(
                "BuildConfiguration ID {} is a dependency of BuildConfiguration {}.".format(to_delete_id, config.name))

    response = utils.checked_api_call(pnc_api.build_configs, 'delete_specific', id=to_delete_id)
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
@arg("-gp", "--generic-parameters", help="Set of arbitrary additional key=value pairs, such as CUSTOM_PME_PARAMETERS")
@arg("-dids", "--dependency-ids", type=int, nargs="+",
     help="List of BuildConfiguration IDs that are dependencies of this BuildConfiguration.")
# @arg("-bcsid", "--")
def create_build_configuration(**kwargs):
    """
    Create a new BuildConfiguration. BuildConfigurations represent the settings and configuration required to run a build of a specific version of the associated Project's source code.
    If a ProductVersion ID is provided, the BuildConfiguration will have access to artifacts which were produced for that version, but may not have been released yet.
    """
    data = create_build_configuration_raw(**kwargs)
    if data:
        return utils.format_json(data)


def create_build_configuration_raw(**kwargs):
    project_id = kwargs.get('project')
    project_rest = common.get_entity(pnc_api.projects, project_id)
    kwargs['project'] = project_rest
    repository_id = kwargs.get('repository_configuration')
    repository_rest = common.get_entity(pnc_api.repositories, repository_id)
    kwargs['repository_configuration'] = repository_rest
    env_id = kwargs.get('environment')
    env_rest = common.get_entity(pnc_api.environments, env_id)
    kwargs['environment'] = env_rest

    if kwargs.get("generic_parameters"):
        kwargs["generic_parameters"] = ast.literal_eval(kwargs.get("generic_parameters"))

    build_configuration = create_build_conf_object(**kwargs)
    response = utils.checked_api_call(
        pnc_api.build_configs, 'create_new', body=build_configuration)
    if response:
        return response.content


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
    data = list_build_configurations_for_product_raw(id, name, page_size, page_index, sort, q)
    if data:
        return utils.format_json(data)

def list_build_configurations_for_product_raw(id=None, name=None, page_size=200, page_index=0, sort="", q=""):
    found_id = common.set_id(pnc_api.products, id, name)
    response = utils.checked_api_call(pnc_api.build_configs, 'get_all_by_product_id', product_id=found_id, page_size=page_size,
                                      page_index=page_index,
                                      sort=sort, q=q)
    if response:
        return response.content


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
    data = list_build_configurations_for_project_raw(id, name, page_size, page_index, sort, q)
    if data:
        return utils.format_json_list(data)

def list_build_configurations_for_project_raw(id=None, name=None, page_size=200, page_index=0, sort="", q=""):
    found_id = common.set_id(pnc_api.projects, id, name)
    response = utils.checked_api_call(pnc_api.build_configs, 'get_all_by_project_id', project_id=found_id, page_size=page_size,
                                      page_index=page_index,
                                      sort=sort, q=q)
    if response:
        return response.content


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
    data = list_build_configurations_for_project_raw(product_id, version_id, page_size, page_index, sort, q)
    if data:
        return utils.format_json_list(data)

def list_build_configurations_for_product_version_raw(product_id, version_id, page_size=200, page_index=0, sort="", q=""):
    found_product_id = common.set_id(pnc_api.products, product_id, None)
    response = utils.checked_api_call(pnc_api.build_configs, 'get_all_by_product_version_id', product_id=found_product_id,
                                      version_id=version_id, page_size=page_size, page_index=page_index, sort=sort, q=q)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfiguration to list dependencies for.", type=types.existing_bc_id)
@arg("-n", "--name", help="Name of the BuildConfiguration to list dependencies for.", type=types.valid_bc_name)
@arg("-p", "--page-size", help="Limit the amount of build records returned")
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_dependencies(id=None, name=None, page_size=200, page_index=0, sort="", q=""):
    data = list_dependencies_raw(id, name, page_size, page_size, sort, q)
    if data:
        return utils.format_json_list(data)

def list_dependencies_raw(id=None, name=None, page_size=200, page_index=0, sort="", q=""):
    found_id = common.set_id(pnc_api.build_configs, id, name)
    response = utils.checked_api_call(pnc_api.build_configs, 'get_dependencies', id=found_id, page_size=page_size,
                                      page_index=page_index, sort=sort, q=q)
    if response:
        return response.content


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
    data = add_dependency_raw(id, name, dependency_id, dependency_name)
    if data:
        return utils.format_json_list(data)

def add_dependency_raw(id=None, name=None, dependency_id=None, dependency_name=None):
    add_to = common.set_id(pnc_api.build_configs, id, name)
    to_add = common.set_id(pnc_api.build_configs, dependency_id, dependency_name)

    dependency = pnc_api.build_configs.get_specific(id=to_add).content
    response = utils.checked_api_call(pnc_api.build_configs, 'add_dependency', id=add_to, body=dependency)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfiguration to remove a dependency from.", type=types.existing_bc_id)
@arg("-n", "--name", help="Name of the BuildConfiguration to remove a dependency from.", type=types.existing_bc_name)
@arg("-di", "--dependency-id", help="ID of the dependency BuildConfiguration to remove.", type=types.existing_bc_id)
@arg("-dn", "--dependency-name", help="Name of the dependency BuildConfiguration to remove.",
     type=types.existing_bc_name)
def remove_dependency(id=None, name=None, dependency_id=None, dependency_name=None):
    """
    Remove a BuildConfiguration from the dependency list of another BuildConfiguration
    """
    data = remove_dependency_raw(id, name, dependency_id, dependency_name)
    if data:
        return utils.format_json_list(data)

def remove_dependency_raw(id=None, name=None, dependency_id=None, dependency_name=None):
    found_id = common.set_id(pnc_api.build_configs, id, name)
    found_dep_id = common.set_id(pnc_api.build_configs, dependency_id, dependency_name)

    response = utils.checked_api_call(pnc_api.build_configs, 'remove_dependency', id=found_id, dependency_id=found_dep_id)
    if response:
        return response.content

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
    data = list_product_versions_for_build_configuration_raw(id, name, page_size, page_index, sort, q)
    if data:
        return utils.format_json_list(data)

def list_product_versions_for_build_configuration_raw(id=None, name=None, page_size=200, page_index=0, sort="", q=""):
    found_id = common.set_id(pnc_api.build_configs, id, name)
    response = utils.checked_api_call(pnc_api.build_configs, 'get_product_versions', id=found_id, page_size=page_size,
                                      page_index=page_index, sort=sort,
                                      q=q)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfiguration to add a ProductVersion to.", type=types.existing_bc_id)
@arg("-n", "--name", help="Name of the BuildConfiguration to add a ProductVersions to.", type=types.existing_bc_name)
@arg('product_version_id', help="ID of the ProductVersion to add.", type=types.existing_product_version)
def add_product_version_to_build_configuration(id=None, name=None, product_version_id=None):
    """
    Associate an existing ProductVersion with a BuildConfiguration
    """
    data = remove_product_version_from_build_configuration_raw(id, name, product_version_id)
    if data:
        return utils.format_json_list(data)

def add_product_version_to_build_configuration_raw(id=None, name=None, product_version_id=None):
    found_id = common.set_id(pnc_api.build_configs, id, name)

    to_add = common.get_entity(pnc_api.product_versions, product_version_id)
    response = utils.checked_api_call(pnc_api.build_configs, 'add_product_version', id=found_id, body=to_add)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfiguration to remove a ProductVersion from.", type=types.existing_bc_id)
@arg("-n", "--name", help="Name of the BuildConfiguration to remove a ProductVersions from.",
     type=types.existing_bc_name)
@arg('product_version_id', help="ID of the ProductVersion to remove.", type=types.existing_product_version)
def remove_product_version_from_build_configuration(id=None, name=None, product_version_id=None):
    """
    Remove a ProductVersion from association with a BuildConfiguration
    """
    data = remove_product_version_from_build_configuration_raw(id, name, product_version_id)
    if data:
        return utils.format_json_list(data)

def remove_product_version_from_build_configuration_raw(id=None, name=None, product_version_id=None):
    found_id = common.set_id(pnc_api.build_configs, id, name)
    response = utils.checked_api_call(pnc_api.build_configs, 'remove_product_version', id=found_id,
                                      product_version_id=product_version_id)
    if response:
        return response.content


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
    data = list_revisions_of_build_configuration_raw(id, name, page_size, page_index, sort)
    if data:
        return utils.format_json_list(data)

def list_revisions_of_build_configuration_raw(id=None, name=None, page_size=200, page_index=0, sort=""):
    found_id = common.set_id(pnc_api.build_configs, id, name)
    response = utils.checked_api_call(pnc_api.build_configs, 'get_revisions', id=found_id, page_size=page_size,
                                      page_index=page_index, sort=sort)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfiguration to retrieve a revision from.", type=types.existing_bc_id)
@arg("-n", "--name", help="Name of the BuildConfiguration to retrieve a revision from.", type=types.existing_bc_name)
@arg("--revision_id", help="Number of the revision to retrieve.")
def get_revision_of_build_configuration(id=None, name=None, revision_id=None):
    """
    Get a specific audited revision of a BuildConfiguration
    """
    data = get_revision_of_build_configuration_raw(id, name, revision_id)
    if data:
        return utils.format_json_list(data)

def get_revision_of_build_configuration_raw(id=None, name=None, revision_id=None):
    found_id = common.set_id(pnc_api.build_configs, id, name)
    response = utils.checked_api_call(pnc_api.build_configs, 'get_revision', id=found_id, rev=revision_id)
    if response:
        return response.content


@arg("-p", "--page-size", help="Limit the amount of build records returned", type=int)
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_build_configurations(page_size=200, page_index=0, sort="", q=""):
    """
    List all BuildConfigurations
    """
    data = list_build_configurations_raw(page_size, page_index, sort, q)
    if data:
        return utils.format_json_list(data)


def list_build_configurations_raw(page_size=200, page_index=0, sort="", q=""):
    response = utils.checked_api_call(pnc_api.build_configs, 'get_all', page_size=page_size, page_index=page_index, sort=sort,
                                      q=q)
    if response:
        return response.content
