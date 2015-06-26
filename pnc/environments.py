from argh import arg
import client
from client.EnvironmentsApi import EnvironmentsApi
import utils

__author__ = 'thauser'
def _create_environment_object(build_type, operational_system):
    created_environment = client.models.Environment.Environment()
    if build_type: created_environment.buildType = build_type
    if operational_system: created_environment.operationalSystem = operational_system
    return created_environment


def _environment_exists(search_id):
    response = EnvironmentsApi(utils.get_api_client()).getSpecific(id=search_id)
    if response.ok:
        return True
    return False

@arg("build-type", help="Type of build for this build environment")
@arg("operating-system", help="Operating system for this build environment")
def create_environment(build_type, operating_system):
    environment = _create_environment_object(build_type, operating_system)
    response = EnvironmentsApi(utils.get_api_client()).createNew(body=environment)
    print(utils.pretty_format_response(response.json()))

@arg("id", help="ID of the environment to replace")
@arg("-bt","--build-type", help="Type of build for the new environment")
@arg("-os","--operating-system", help="Operating system for the new environment")
def update_environment(id, build_type=None, operating_system=None):
    environment = _create_environment_object(build_type, operating_system)
    if _environment_exists(id):
        response = EnvironmentsApi(utils.get_api_client()).update(id=id, body=environment)
        if (response.ok):
            print("Successfully updated environment {0}.").format(id)
        else:
            print("Updating environment {0} failed.").format(id)
    else:
        print("No environment with id {0} exists.").format(id)

@arg("id", help="ID of the environment to delete")
def delete_environment(id):
    if not _environment_exists(id):
        print("No environment with id {0} exists.").format(id)
        return

    response = EnvironmentsApi(utils.get_api_client()).delete(id=id)
    if (response.ok):
        print("Environment {0} succesfully deleted.")
    else:
        print("Failed to delete environment {0}").format(id)
        print(response)

@arg("id", help="ID of the environment to retrieve")
def get_environment(id):
    response = EnvironmentsApi(utils.get_api_client()).getSpecific(id=id)
    if (response.ok):
        print(utils.pretty_format_response(response.json()))
    else:
        print("No environment with id {0} exists.").format(id)

def list_environments():
    response = EnvironmentsApi(utils.get_api_client()).getAll()
    print(utils.pretty_format_response(response.json()))