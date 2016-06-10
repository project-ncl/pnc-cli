import argparse
import logging
from six import iteritems
from argh import arg

from pnc_cli.swagger_client import ProjectRest
from pnc_cli.swagger_client import ProjectsApi
from pnc_cli import utils

projects_api = ProjectsApi(utils.get_api_client())


def _create_project_object(**kwargs):
    created_project = ProjectRest()
    for key, value in iteritems(kwargs):
        setattr(created_project, key, value)
    return created_project


def existing_project_id(id_input):
    utils.valid_id(id_input)
    if not _project_exists(id_input):
        raise argparse.ArgumentTypeError("no Project with ID {} exists".format(id_input))
    return id_input



def get_project_id(proj_id, name):
    """
    :param proj_id: id to check existence
    :param name: name to resolve to ID
    :return: a valid ID of a Project
    """
    if proj_id:
        if not _project_exists(proj_id):
            logging.error("No Project with ID {} exists.".format(proj_id))
            return
        found_id = proj_id
    elif name:
        found_id = _get_project_id_by_name(name)
        if not found_id:
            logging.error("No Project with name {0} exists.".format(name))
            return
    else:
        logging.warn("Either a Project name or id is required")
        return
    return found_id


def _get_project_id_by_name(search_name):
    """
    Returns the id of the Project in which name matches search_name
    :param search_name: name of the Project
    :return: id of the matching Project, or None if no match found
    """
    response = utils.checked_api_call(projects_api, 'get_all', q='name==' + search_name)
    if not response.content:
        return None
    else:
        return response.content[0].id


def _project_exists(search_id):
    """
    Test if a Project with the given id exists
    :param search_id: id to test for
    :return: True if a Project with search_id exists
    """
    response = utils.checked_api_call(projects_api, 'get_specific', id=str(search_id))
    if not response:
        return False
    return True


@arg("name", help="Name for the Project")
@arg("-c", "--configuration-ids", type=int, nargs='+',
     help="Space separated list of BuildConfigurationIDs this Project should be associated with.")
@arg("-d", "--description", help="Detailed description of the new Project")
@arg("-p", "--project-url", help="SCM Url for the Project")
@arg("-i", "--issue-tracker-url", help="Issue tracker URL for the new Project")
@arg("-l", "--license-id", help="License ID for the new Project")
def create_project(**kwargs):
    """
    Create a new Project. Typically, a Project represents a single source code repository, as well as the information related to development of those sources.
    """
    project = _create_project_object(**kwargs)
    response = utils.checked_api_call(projects_api, 'create_new', body=project)
    if response:
        return response.content


@arg("id", help="ID for the Project that will be updated.")
@arg("-n", "--name", help="New name for the Project that will be updated.")
@arg("-c", "--configuration-ids", type=int, nargs='+',
     help="Space separated list of BuildConfiguration IDs this Project should be associated with.")
@arg("-d", "--description", help="Detailed description of the new Project.")
@arg("-p", "--project-url", help="SCM Url for the Project.")
@arg("-i", "--issue-url", help="Issue tracker URL for the new Project")
@arg("-l", "--license-id", help="License ID for the new Project")
def update_project(id, **kwargs):
    """
    Update an existing Project with new information
    """
    if not id:
        logging.error("A Project ID must be specified.")
        return
    if utils.contains_only_none_values(kwargs):
        logging.error("Updating a Project requires at least one modified field.")
        return
    response = utils.checked_api_call(projects_api, 'get_specific', id=id)
    if not response:
        logging.error("No Project with ID {} exists.".format(id))
        return
    to_update = response.content
    for key, value in iteritems(kwargs):
        if value is not None:
            setattr(to_update, key, value)
    response = utils.checked_api_call(projects_api, 'update', id=id, body=to_update)
    return response


@arg("-id", "--id", help="ID of the Project to retrieve")
@arg("-n", "--name", help="Name of the Project to retrieve")
def get_project(id=None, name=None):
    """
    Get a specific Project by ID or name
    """
    proj_id = get_project_id(id, name)
    if not proj_id:
        return
    response = utils.checked_api_call(projects_api, 'get_specific', id=proj_id)
    if response:
        return response.content


@arg("-id", "--id", help="ID of the Project to delete")
@arg("-n", "--name", help="Name of the Project to delete")
def delete_project(id=None, name=None):
    """
    Delete a Project by ID or name.
    """
    proj_id = get_project_id(id, name)
    if not proj_id:
        return
    response = utils.checked_api_call(projects_api, 'delete_specific', id=proj_id)
    if response:
        return response.content


@arg("-p", "--page-size", help="Limit the amount of build records returned")
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_projects(page_size=200, sort="", q=""):
    """
    List all Projects
    """
    response = utils.checked_api_call(projects_api, 'get_all', page_size=page_size, sort=sort, q=q)
    if response:
        return response.content
