import argh
from argh import arg
from six import iteritems

import pnc_cli.common as common
import pnc_cli.cli_types as types
import pnc_cli.utils as utils
from pnc_cli.swagger_client import ProjectRest
from pnc_cli.pnc_api import pnc_api


def _create_project_object(**kwargs):
    created_project = ProjectRest()
    for key, value in iteritems(kwargs):
        setattr(created_project, key, value)
    return created_project


@arg("name", help="Name for the Project", type=types.unique_project_name)
@arg("-d", "--description", help="Detailed description of the new Project")
@arg("-p", "--project-url", help="SCM Url for the Project", type=types.valid_url)
@arg("-i", "--issue-tracker-url", help="Issue tracker URL for the new Project", type=types.valid_url)
@arg("-l", "--license-id", help="License ID for the new Project", type=types.existing_license)
def create_project(**kwargs):
    """
    Create a new Project. Typically, a Project represents a single source code repository, as well as the information related to development of those sources.
    """
    content = create_project_raw(**kwargs)
    if content:
        return utils.format_json(content)

def create_project_raw(**kwargs):
    project = _create_project_object(**kwargs)
    response = utils.checked_api_call(pnc_api.projects, 'create_new', body=project)
    if response:
        return response.content

@arg("id", help="ID for the Project that will be updated.", type=types.existing_project_id)
@arg("-n", "--name", help="New name for the Project that will be updated.", type=types.unique_project_name)
@arg("-d", "--description", help="Detailed description of the new Project.")
@arg("-p", "--project-url", help="SCM Url for the Project.", type=types.valid_url)
@arg("-i", "--issue-url", help="Issue tracker URL for the new Project", type=types.valid_url)
@arg("-l", "--license-id", help="License ID for the new Project", type=types.existing_license)
def update_project(id, **kwargs):
    """
    Update an existing Project with new information
    """
    content = update_project_raw(id, **kwargs)
    if content:
        return utils.format_json(content)

def update_project_raw(id, **kwargs):
    if utils.contains_only_none_values(kwargs):
        raise argh.exceptions.CommandError("Updating a Project requires at least one modified field.")

    to_update = utils.checked_api_call(pnc_api.projects, 'get_specific', id=id).content
    for key, value in iteritems(kwargs):
        if value is not None:
            setattr(to_update, key, value)
    response = utils.checked_api_call(pnc_api.projects, 'update', id=id, body=to_update)
    if response:
        return response.content
    else:
        return utils.checked_api_call(pnc_api.projects, 'get_specific', id=id).content


@arg("-id", "--id", help="ID of the Project to retrieve", type=types.existing_project_id)
@arg("-n", "--name", help="Name of the Project to retrieve", type=types.existing_project_name)
def get_project(id=None, name=None):
    """
    Get a specific Project by ID or name
    """
    content = get_project_raw(id, name)
    if content:
        return utils.format_json(content)

def get_project_raw(id=None, name=None):
    proj_id = common.set_id(pnc_api.projects, id, name)
    response = utils.checked_api_call(pnc_api.projects, 'get_specific', id=proj_id)
    if response:
        return response.content

@arg("-id", "--id", help="ID of the Project to delete", type=types.existing_project_id)
@arg("-n", "--name", help="Name of the Project to delete", type=types.existing_project_name)
def delete_project(id=None, name=None):
    """
    Delete a Project by ID or name.
    """
    content = delete_project_raw(id, name)
    if content:
        return utils.format_json(content)

def delete_project_raw(id=None, name=None):
    proj_id = common.set_id(pnc_api.projects, id, name)
    response = utils.checked_api_call(pnc_api.projects, 'delete_specific', id=proj_id)
    if response:
        return response.content


@arg("-p", "--page-size", help="Limit the amount of Projects returned", type=int)
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_projects(page_size=200, page_index=0, sort="", q=""):
    """
    List all Projects
    """
    content = list_projects_raw(page_size=page_size, page_index=page_index, sort=sort, q=q)
    if content:
        return utils.format_json_list(content)

def list_projects_raw(page_size=200, page_index=0, sort="", q=""):
    response = utils.checked_api_call(pnc_api.projects, 'get_all', page_size=page_size, page_index=page_index, sort=sort, q=q)
    if response:
        return response.content
