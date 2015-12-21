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


def get_project_id(proj_id, name):
    """
    :param proj_id: id to check existence
    :param name: name to resolve to ID
    :return: a valid ID of a project
    """
    if proj_id:
        if not _project_exists(proj_id):
            print("No Project with ID {} exists.".format(proj_id))
            return
        found_id = proj_id
    elif name:
        found_id = _get_project_id_by_name(name)
        if not found_id:
            print("No project with name {0} exists.".format(name))
            return
    else:
        print("Either a project name or id is required")
        return
    return found_id

def _get_project_id_by_name(search_name):
    """
    Returns the id of the project in which name matches search_name
    :param search_name: name of the project
    :return: id of the matching project, or None if no match found
    """
    for project in projects_api.get_all().content:
        if project.name == search_name:
            return project.id
    return None


def _project_exists(search_id):
    """
    Test if a project with the given id exists
    :param search_id: id to test for
    :return: True if a project with search_id exists
    """
    existing_ids = [str(x.id) for x in projects_api.get_all(page_size=search_id).content]
    return str(search_id) in existing_ids


@arg("name", help="Name for the project")
@arg("-c", "--configuration-ids", type=int, nargs='+',
     help="Space separated list of BuildConfigurationIDs this Project should be associated with.")
@arg("-d", "--description", help="Detailed description of the new project")
@arg("-p", "--project_url", help="SCM Url for the project")
@arg("-i", "--issue-tracker-url", help="Issue tracker URL for the new project")
@arg("-l", "--license_id", help="License ID for the new project")
def create_project(**kwargs):
    """
    Create a new Project
    """
    project = _create_project_object(**kwargs)
    response = utils.checked_api_call(projects_api, 'create_new', body=project)
    if response:
        return response.content


@arg("id", help="ID for the project that will be updated.")
@arg("-n", "--name", help="New name for the project that will be updated.")
@arg("-c", "--configuration-ids", type=int, nargs='+',
     help="Space separated list of BuildConfiguration IDs this Project should be associated with.")
@arg("-d", "--description", help="Detailed description of the new project.")
@arg("-p", "--project_url", help="SCM Url for the project.")
@arg("-i", "--issue_url", help="Issue tracker URL for the new project")
@arg("-l", "--license_id", help="License ID for the new project")
def update_project(id, **kwargs):
    """
    Update an existing Project with new information
    """
    if not id:
        logging.warn("A Project ID must be specified.")
        return
    to_udpate = projects_api.get_specific(id=id).content
    for key, value in iteritems(kwargs):
        setattr(to_udpate, key, value)
    response = utils.checked_api_call(projects_api, 'update', id=id, body=to_udpate)
    if response:
        return response.content


@arg("-id", "--id", help="ID of the project to retrieve")
@arg("-n", "--name", help="Name of the project to retrieve")
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


@arg("-id", "--id", help="ID of the project to delete")
@arg("-n", "--name", help="Name of the project to delete")
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
