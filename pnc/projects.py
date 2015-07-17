from argh import arg
import client
from client.ProjectsApi import ProjectsApi
import utils

__author__ = 'thauser'
def _create_project_object(name, description, issue_url, project_url, configuration_ids, license_id):
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
    """Create a new project"""
    project = _create_project_object(name, description, issue_url, project_url, configuration_ids,license_id)
    response = utils.pretty_format_response(ProjectsApi(utils.get_api_client()).createNew(body=project).json())
    print(response)

@arg("project-id", help="ID for the project that will be updated")
@arg("-n","--name", help="Name for the project")
@arg("-cids","--configuration-ids", help="List of configuration IDs this project should be associated with")
@arg("-desc","--description", help="Detailed description of the new project")
@arg("-purl","--project_url", help="SCM Url for the project")
@arg("-iurl","--issue_url", help="Issue tracker URL for the new project")
@arg("-l","--license_id", help="License ID for the new project")
def update_project(project_id, name=None, description=None, issue_url=None, project_url=None, configuration_ids=None,license_id=None):
    project = _create_project_object(name, description, issue_url, project_url, configuration_ids, license_id)
    if _project_exists(project_id):
        response = ProjectsApi(utils.get_api_client()).update(id=project_id,body=project)
        if response.ok:
            print("Project {0} successfully updated.").format(project_id)
        else:
            print("Updating project with id {0} failed").format(project_id)
    else:
        print("No project with id {0} exists.").format(project_id)

@arg("-id","--id",help="ID of the project to retrieve")
@arg("-n","--name", help="Name of the project to retrieve")
def get_project(id=None, name=None):
    if id:
        response = ProjectsApi(utils.get_api_client()).getSpecific(id=id)
        if response.ok:
            print(utils.pretty_format_response(response.json()))
        else:
            print("No project with id {0} exists.").format(id)
    elif name:
        response = ProjectsApi(utils.get_api_client()).getSpecific(id=_get_project_id_by_name(name))
        if response.ok:
            print(utils.pretty_format_response(response.json()))
        else:
            print("No project with name {0} exists.").format(name)
    else:
        print("Either a project name or id is required")

@arg("-id","--id", help="ID of the project to delete")
@arg("-n","--name", help="Name of the project to delete")
def delete_project(id=None, name=None):
    if id:
        if not _project_exists(id):
            print("No project with id {0} exists.").format(id)
            return
        id = id
    elif name:
        id = _get_project_id_by_name(name)
        if not id:
            print("There is no project with name {0}.").format(name)
            return
    else:
        print("Either a project name or id is required.")
        return

    response = ProjectsApi(utils.get_api_client()).deleteSpecific(id=id)
    if response.ok:
        print("Project {0} successfully deleted.").format(id)
    else:
        print("Failed to delete Project {0}").format(id)

def list_projects():
    """Get a JSON object containing existing projects"""
    response = ProjectsApi(utils.get_api_client()).getAll()
    print(utils.pretty_format_response(response.json()))