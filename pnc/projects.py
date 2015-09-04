from pprint import pprint
import swagger_client
from swagger_client.apis.projects_api import ProjectsApi
from argh import arg
import utils

projects_api = ProjectsApi(utils.get_api_client())

def _create_project_object(**kwargs):
    created_project = swagger_client.models.project.Project()
    for key, value in kwargs.iteritems():
        setattr(created_project, key, value)
    return created_project

def get_project_id(proj_id,name):
    """
    :param proj_id: id to check existence
    :param name: name to resolve to ID
    :return: a valid ID of a project
    """
    if proj_id:
        return proj_id
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
    for project in projects_api.get_all():
        if project.name == search_name:
            return project.id
    return None

def _project_exists(search_id):
    """
    Test if a project with the given id exists
    :param search_id: id to test for
    :return: True if a project with search_id exists
    """
    existing_ids = [x.id for x in projects_api.get_all()]
    return search_id in existing_ids

@arg("name", help="Name for the project")
@arg("-c","--configuration-ids", help="List of configuration IDs this project should be associated with")
@arg("-d","--description", help="Detailed description of the new project")
@arg("-p","--project_url", help="SCM Url for the project")
@arg("-i","--issue_url", help="Issue tracker URL for the new project")
@arg("-l","--license_id", help="License ID for the new project")
def create_project(name, **kwargs):
    """
    Create a new project
    :param name:
    :param kwargs:
    :return:
    """
    project = _create_project_object(name, **kwargs)
    projects_api.create(body=project,callback=callback_function)

@arg("-id", "--id", help="ID for the project that will be updated.")
@arg("-n","--name", help="New name for the project that will be updated.")
@arg("-bc","--build-configurations", help="Comma separated list of build configuration IDs this project should be associated with.")
@arg("-desc","--description", help="Detailed description of the new project.")
@arg("-purl","--project_url", help="SCM Url for the project.")
@arg("-iurl","--issue_url", help="Issue tracker URL for the new project")
@arg("-l","--license_id", help="License ID for the new project")
def update_project(id=None, **kwargs):
    """
    Update a project
    :param id:
    :param kwargs:
    :return:
    """
    to_udpate = projects_api.get_specific(id=id)
    for key, value in kwargs.iteritems():
        setattr(to_udpate, key, value)
    projects_api.update(id=id, body=to_udpate, callback=callback_function)

@arg("-id","--id",help="ID of the project to retrieve")
@arg("-n","--name", help="Name of the project to retrieve")
def get_project(id=None, name=None):
    """
    Get a specific project by ID or name
    :param id:
    :param name:
    :return:
    """
    proj_id = get_project_id(id,name)
    if not proj_id:
        return
    projects_api.get_specific(id=proj_id, callback=callback_function)


@arg("-id","--id", help="ID of the project to delete")
@arg("-n","--name", help="Name of the project to delete")
def delete_project(id=None, name=None):
    """
    Delete a project by ID or name.
    :param id: id of the project to delete
    :param name: name of the project to delete
    :return: errors upon failure
    """
    proj_id = get_project_id(id, name)
    if not proj_id:
        return
    projects_api.delete(proj_id, callback=callback_function)

def list_projects():
    """
    List all projects
    :return: list of all projects
    """
    projects_api.get_all(callback=callback_function)

def callback_function(response):
    if response:
        pprint(response)

