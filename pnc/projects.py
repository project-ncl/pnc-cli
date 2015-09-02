from argh import arg

import client
from client.ProjectsApi import ProjectsApi
import utils


__author__ = 'thauser'
def _create_project_object(**kwargs):
    created_project = client.models.Project.Project()
    for key, value in kwargs.iteritems():
        setattr(created_project, key, value)
    return created_project

def get_project_id(id,name):
    """
    Confirms the existence of a project ID and / or finds an existing ID for a project from a name
    Prints errors if nothing useful was found.
    :param id: id to check existence
    :param name: name to resolve to ID
    :return: a valid ID of a project
    """
    if id:
        proj_id = id
        if not _project_exists(proj_id):
            print("No project with ID {0} exists.").format(proj_id)
            return
    elif name:
        proj_id =_get_project_id_by_name(name)
        if not proj_id:
            print("No project with name {0} exists.").format(name)
            return
    else:
        print("Either a project name or id is required")
        return


def _get_project_id_by_name(search_name):
    """
    Returns the id of the project in which name matches search_name
    :param search_name: name of the project
    :return: id of the matching project, or None if no match found
    """
    response = ProjectsApi(utils.get_api_client()).getAll()
    for config in response.json():
        if config["name"] == search_name:
            return config["id"]
    return None

def _project_exists(search_id):
    """
    Test if a project with the given id exists
    :param search_id: id to test for
    :return: True if a project with search_id exists
    """
    response = ProjectsApi(utils.get_api_client()).getSpecific(id=search_id)
    if response.ok:
        return True
    return False

@arg("name", help="Name for the project")
@arg("-c","--configuration-ids", help="List of configuration IDs this project should be associated with")
@arg("-d","--description", help="Detailed description of the new project")
@arg("-p","--project_url", help="SCM Url for the project")
@arg("-i","--issue_url", help="Issue tracker URL for the new project")
@arg("-l","--license_id", help="License ID for the new project")
def create_project(name, configuration_ids=None, description=None, issue_url=None, project_url=None, license_id=None):
    project = _create_project_object(name, description, issue_url, project_url, configuration_ids,license_id)
    response = create(project)
    if not response.ok:
        utils.print_error(__name__,response)
        return
    utils.print_by_key(response.json())

@arg("-id", "--id", help="ID for the project that will be updated.")
@arg("-n","--name", help="Name for the project that will be updated.")
@arg("-bc","--build-configurations", help="Comma separated list of build configuration IDs this project should be associated with.")
@arg("-desc","--description", help="Detailed description of the new project.")
@arg("-purl","--project_url", help="SCM Url for the project.")
@arg("-iurl","--issue_url", help="Issue tracker URL for the new project")
@arg("-l","--license_id", help="License ID for the new project")
def update_project(id=None, name=None, updated_name=None, description=None, issue_url=None, project_url=None, build_configurations=None,license_id=None):
    proj_id = get_project_id(id,name)
    if not proj_id:
        return

    updated_project = _create_project_object(updated_name, description, issue_url, project_url, build_configurations, license_id)
    response = update(proj_id, updated_project)

    if response.ok:
        print("Project {0} successfully updated.").format(proj_id)
    else:
        utils.print_error(__name__,response)

@arg("-id","--id",help="ID of the project to retrieve")
@arg("-n","--name", help="Name of the project to retrieve")
def get_project(id=None, name=None):
    proj_id = get_project_id(id,name)
    if not proj_id:
        return

    response = get_specific(proj_id)
    if not response.ok:
        utils.print_error(__name__, response)
        return
    utils.print_by_key(response.json())

def get_specific(id):
    return ProjectsApi(utils.get_api_client()).getSpecific(id=id)

@arg("-id","--id", help="ID of the project to delete")
@arg("-n","--name", help="Name of the project to delete")
def delete_project(id=None, name=None):
    if id:
        if not _project_exists(id):
            print("No project with id {0} exists.").format(id)
            return
        proj_id = id
    elif name:
        proj_id = _get_project_id_by_name(name)
        if not proj_id:
            print("There is no project with name {0}.").format(name)
            return
    else:
        print("Either a project name or id is required.")
        return
    response = delete(proj_id)

    if not response.ok:
        utils.print_error(__name__,response)
        return
    if name:
        format = name
    else:
        format = proj_id
    print("Project {0} successfully deleted.").format(format)

@arg("-a","--attributes", help="Comma separated list of attributes to print for each project")
def list_projects(attributes=None):
    response = get_all()
    if not response.ok:
        utils.print_error(__name__,response)
        return
    projects = response.json()
    if attributes is not None:
        utils.print_matching_attribute(projects, attributes, client.models.Project.Project().attributeMap)
    else:
        utils.print_by_key(projects)

def get_all():
    return ProjectsApi(utils.get_api_client()).getAll()

def create(new_project):
    return ProjectsApi(utils.get_api_client()).createNew(body=new_project)

def update(project_id, updated_project):
    return ProjectsApi(utils.get_api_client()).update(id=project_id,body=updated_project)

def delete(id):
    return ProjectsApi(utils.get_api_client()).deleteSpecific(id=id)

