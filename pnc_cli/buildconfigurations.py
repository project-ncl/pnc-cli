from argh import arg

from pnc_cli import utils

from pnc_cli import swagger_client
from pnc_cli.swagger_client.apis.buildconfigurations_api import BuildconfigurationsApi
from pnc_cli import products
from pnc_cli import productversions
from pnc_cli import projects

configs_api = BuildconfigurationsApi(utils.get_api_client())


def create_build_conf_object(**kwargs):
    created_build_configuration = swagger_client.BuildConfigurationRest()
    for key, value in kwargs.items():
        setattr(created_build_configuration, str(key), value)
    # workaround for current REST client
    if "build_status" not in kwargs.keys():
        setattr(created_build_configuration, "build_status", "UNKNOWN")
    return created_build_configuration

#TODO: use rsql to streamline this
def get_build_configuration_id_by_name(name):
    """
    Returns the id of the build configuration matching name
    :param name: name of build configuration
    :return: id of the matching build configuration, or None if no match found
    """
    for config in configs_api.get_all(page_size=10000000).content:
        if config.name == name:
            return config.id
    return None


def config_id_exists(search_id):
    """
    Test if a build configuration matching search_id exists
    :param search_id: id to test for
    :return: True if a build configuration with search_id exists, False otherwise
    """
    existing_ids = [str(x.id) for x in configs_api.get_all(page_size=search_id).content]
    return str(search_id) in existing_ids


def get_config_id(search_id, name):
    """
    Given an ID or name, checks for existence then returns an ID
    :param search_id: ID to check for existence
    :param name: name to map to ID
    :return: Valid ID if it exists. None otherwise
    """
    if search_id:
        if not config_id_exists(search_id):
            print("No BuildConfiguration with ID {} exists.".format(search_id))
            return
        config_id = search_id
    elif name:
        config_id = get_build_configuration_id_by_name(name)
        if not config_id:
            print("No BuildConfiguration with the name {} exists.".format(name))
            return
    else:
        print("Either a name or an ID of a BuildConfiguration is required.")
        return
    return config_id


@arg("-i", "--id", help="ID of the BuildConfiguration to trigger.")
@arg("-n", "--name", help="Name of the BuildConfiguration to trigger.")
def build(id=None, name=None):
    """
    Trigger a BuildConfiguration by name or ID
    """
    trigger_id = get_config_id(id, name)
    if not trigger_id:
        return
    response = utils.checked_api_call(configs_api, 'trigger', id=trigger_id)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfiguration to retrieve.")
@arg("-n", "--name", help="Name of the BuildConfiguration to retrieve.")
def get_build_configuration(id=None, name=None):
    """
    Get a specific BuildConfiguration
    """
    found_id = get_config_id(id, name)
    if not found_id:
        return
    response = utils.checked_api_call(configs_api, 'get_specific', id=found_id)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfiguration to update.")
@arg("-n", "--name", help="Name of the BuildConfiguration to update.")
# allow specifying project by name?
@arg("-pid", "--project-id", help="ID of the Project to associate the BuildConfiguration with.")
@arg("-e", "--environment", help="ID of the Environment for the new BuildConfiguration.")
@arg("-d", "--description", help="Description of the new build configuration.")
@arg("-surl", "--scm-url", help="URL to the sources of the BuildConfiguration.")
@arg("-srev", "--scm-revision", help="Revision of the sources in scm-url for this BuildConfiguration.")
@arg("-bs", "--build-script", help="Script to execute for the BuildConfiguration.")
def update_build_configuration(id=None, name=None, **kwargs):
    to_update_id = get_config_id(id, name)
    if not to_update_id:
        return

    bc_to_update = configs_api.get_specific(id=to_update_id).content
    for key, value in kwargs.items():
        if value is not None:
            setattr(bc_to_update, key, value)

    response = utils.checked_api_call(configs_api, 'update', id=to_update_id, body=bc_to_update)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfiguration to delete.")
@arg("-n", "--name", help="Name of the BuildConfiguration to delete.")
def delete_build_configuration(id=None, name=None):
    to_delete_id = get_config_id(id, name)
    if not to_delete_id:
        return

    response = utils.checked_api_call(configs_api, 'delete_specific', id=to_delete_id)
    if response:
        return response.content


@arg("name", help="Name for the new BuildConfiguration.")
# allow specifying project by name?
@arg("project_id", help="ID of the Project to associate the BuildConfiguration with.")
@arg("environment_id", help="ID of the Environment for the new BuildConfiguration.")
@arg("-d", "--description", help="Description of the new build configuration.")
@arg("-surl", "--scm-repo-url", help="URL to the sources of the BuildConfiguration.")
@arg("-srev", "--scm-revision", help="Revision of the sources in scm-url for this BuildConfiguration.")
@arg("-bs", "--build-script", help="Script to execute for the BuildConfiguration.")
def create_build_configuration(**kwargs):
    """
    Create a new BuildConfiguration
    """
    #TODO: non alphanum not allowed: [a-zA-Z0-9]
    build_configuration = create_build_conf_object(**kwargs)
    response = utils.checked_api_call(
        configs_api, 'create_new', body=build_configuration)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the Product to list BuildConfigurations for.")
@arg("-n", "--name", help="Name of the Product to list BuildConfigurations for.")
@arg("-p", "--page-size", help="Limit the amount of build records returned")
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

@arg("-i", "--id", help="ID of the Project to list BuildConfigurations for.")
@arg("-n", "--name", help="Name of the Project to list BuildConfigurations for.")
@arg("-p", "--page-size", help="Limit the amount of build records returned")
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_build_configurations_for_project(id=None, name=None, page_size=200, sort="", q=""):
    """
    List all BuildConfigurations associated with the given Product.
    """
    found_id = projects.get_project_id(id,name)
    if not found_id:
        return

    response = utils.checked_api_call(configs_api, 'get_all_by_project_id', project_id=found_id, page_size=page_size,
                                      sort=sort, q=q)
    if response:
        return response.content



# TODO: allow specifying product name / version 'version'?
@arg("product_id", help="ID of the Product which contains the desired ProductVersion.")
@arg("version_id", help="ID of the ProductVersion to list BuildConfigurations for.")
@arg("-p", "--page-size", help="Limit the amount of build records returned")
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_build_configurations_for_product_version(product_id, version_id, page_size=20, sort="", q=""):
    """
    List all BuildConfigurations associated with the given ProductVersion
    """
    found_product_id = products.get_product_id(product_id,None)
    if not found_product_id:
        return

    if not productversions.version_exists(version_id):
        print("No ProductVersion with ID {} exists.".format(version_id))
        return

    response = utils.checked_api_call(configs_api, 'get_all_by_product_version_id', product_id=found_product_id,
                                      version_id=version_id, page_size=page_size, sort=sort, q=q)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfiguration to list dependencies for.")
@arg("-n", "--name", help="Name of the BuildConfiguration to list dependencies for.")
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


@arg("-i", "--id", help="ID of the BuildConfiguration to add a dependency to.")
@arg("-n", "--name", help="Name of the BuildConfiguration to add a dependency to.")
@arg("-di", "--dependency-id", help="ID of an existing BuildConfiguration to add as a dependency.")
@arg("-dn", "--dependency-name", help="Name of an existing BuildConfiguration to add as a dependency.")
def add_dependency(id=None, name=None, dependency_id=None, dependency_name=None):
    """
    Add an existing BuildConfiguration as a dependency to another BuildConfiguration.
    """
    add_to = get_config_id(id, name)
    if not add_to:
        return

    to_add = get_config_id(dependency_id, dependency_name)
    if not to_add:
        return

    dependency = configs_api.get_specific(id=to_add).content
    response = utils.checked_api_call(configs_api, 'add_dependency', id=add_to, body=dependency)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfiguration to remove a dependency from.")
@arg("-n", "--name", help="Name of the BuildConfiguration to remove a dependency from.")
@arg("-di", "--dependency-id", help="ID of the dependency BuildConfiguration to remove.")
@arg("-dn", "--dependency-name", help="Name of the dependency BuildConfiguration to remove.")
def remove_dependency(id=None, name=None, dependency_id=None, dependency_name=None):
    """
    Remove a BuildConfiguration from the dependency list of another BuildConfiguration
    """
    found_id = get_config_id(id, name)
    if not found_id:
        return

    found_dep_id = get_config_id(dependency_id, dependency_name)
    if not found_dep_id:
        return

    response = utils.checked_api_call(configs_api, 'remove_dependency', id=found_id, dependency_id=found_dep_id)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfiguration to list ProductVersions for.")
@arg("-n", "--name", help="Name of the BuildConfiguration to list ProductVersions for.")
@arg("-p", "--page-size", help="Limit the amount of build records returned")
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


@arg("-i", "--id", help="ID of the BuildConfiguration to add a ProductVersion to.")
@arg("-n", "--name", help="Name of the BuildConfiguration to add a ProductVersions to.")
@arg('product_version_id', help="ID of the ProductVersion to add.")
def add_product_version_to_build_configuration(id=None, name=None, product_version_id=None):
    """
    Associate an existing ProductVersion with a BuildConfiguration
    """
    found_id = get_config_id(id, name)
    if not found_id:
        return

    if not productversions.version_exists(product_version_id):
        print("No ProductVersion with ID {} exists.".format(product_version_id))
        return

    to_add = productversions.get_product_version(id=product_version_id).content
    response = utils.checked_api_call(configs_api, 'add_product_version', id=found_id, body=to_add)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfiguration to remove a ProductVersion from.")
@arg("-n", "--name", help="Name of the BuildConfiguration to remove a ProductVersions from.")
@arg('product_version_id', help="ID of the ProductVersion to remove.")
def remove_product_version_from_build_configuration(id=None, name=None, product_version_id=None):
    """
    Remove a ProductVersion from association with a BuildConfiguration
    """
    found_id = get_config_id(id, name)
    if not found_id:
        return

    if product_version_id not in [x.id for x in configs_api.get_product_versions(id=found_id).content]:
        print("The specified ProductVersion is not associated with BuildConfiguration {}.".format(found_id))
        return

    response = utils.checked_api_call(configs_api, 'remove_product_version', id=found_id,
                                      product_version_id=product_version_id)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfiguration to list audited revisions for.")
@arg("-n", "--name", help="Name of the BuildConfiguration to list audited revisions for.")
@arg("-p", "--page-size", help="Limit the amount of build records returned")
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
# TODO: PNC return BuildConfigurationAuditedPage instead of BuildConfigurationPage?
def list_revisions_of_build_configuration(id=None, name=None, page_size=200, sort="", q=""):
    """
    List audited revisions of a BuildConfiguration
    """
    found_id = get_config_id(id, name)
    if not found_id:
        return

    response = utils.checked_api_call(configs_api, 'get_revisions', id=found_id, page_size=page_size, sort=sort, q=q)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfiguration to retrieve a revision from.")
@arg("-n", "--name", help="Name of the BuildConfiguration to retrieve a revision from. ")
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


@arg("-i", "--id", help="ID of the Project to list BuildConfigurations for.")
@arg("-n", "--name", help="Name of the Project to list BuildConfigurations for.")
@arg("-p", "--page-size", help="Limit the amount of build records returned")
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_build_configurations_for_project(id=None, name=None, page_size=200, sort="", q=""):
    """
    List all BuildConfigurations associated with the given Project
    """
    found_id = projects.get_project_id(id, name)
    if not found_id:
        return

    response = utils.checked_api_call(configs_api, 'get_all_by_project_id', project_id=found_id, page_size=page_size,
                                      sort=sort, q=q)
    if response:
        return response.content

@arg("-p", "--page-size", help="Limit the amount of build records returned")
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_build_configurations(page_size=200, sort="", q=""):
    """
    List all BuildConfigurations
    """
    response = utils.checked_api_call(configs_api, 'get_all', page_size=page_size, sort=sort, q=q)
    if response:
        return response.content
