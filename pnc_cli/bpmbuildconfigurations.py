from argh import arg

import pnc_cli.cli_types as types
from pnc_cli import swagger_client
from pnc_cli import utils
from pnc_cli.swagger_client import BpmApi
from pnc_cli.swagger_client import EnvironmentsApi
from pnc_cli.swagger_client import ProjectsApi
import pnc_cli.user_config as uc

projects_api = ProjectsApi(uc.user.get_api_client())
configs_api = BpmApi(uc.user.get_api_client())
envs_api = EnvironmentsApi(uc.user.get_api_client())

def create_build_conf_object(**kwargs):
    created_build_configuration = swagger_client.BpmBuildConfigurationCreationRest()
    for key, value in kwargs.items():
        setattr(created_build_configuration, str(key), value)
    return created_build_configuration

@arg("name", help="Name for the new BuildConfiguration.", type=types.valid_bc_name)
# allow specifying project by name?
@arg("project_id", help="ID of the Project to associate the BuildConfiguration with.", type=types.existing_project_id)
@arg("environment_id", help="ID of the Environment for the new BuildConfiguration.",
     type=types.existing_environment_id)
@arg("scm_repo_url", help="URL to the sources of the BuildConfiguration.")
@arg("scm_revision", help="Revision of the sources in scm-url for this BuildConfiguration.")
@arg("scm_external_repo_url", help="URL to the external sources of the BuildConfiguration.")
@arg("scm_external_revision", help="Revision of the external sources in scm-url for this BuildConfiguration.")
@arg("build_script", help="Script to execute for the BuildConfiguration.")
@arg("-d", "--description", help="Description of the new build configuration.")
@arg("-pvi", "--product-version-id", help="Associated ProductVersion ID.")
@arg("-dids", "--dependency-ids", type=int, nargs="+",
     help="List of BuildConfiguration IDs that are dependencies of this BuildConfiguration.")
# @arg("-bcsid", "--")
def create_bpm_build_configuration(**kwargs):
    """
    Create a new BuildConfiguration. BuildConfigurations represent the settings and configuration required to run a build of a specific version of the associated Project's source code.
    If a ProductVersion ID is provided, the BuildConfiguration will have access to artifacts which were produced for that version, but may not have been released yet.
    """

    build_configuration = create_build_conf_object(**kwargs)
    response = utils.checked_api_call(
        configs_api, 'start_bc_creation_task', body=build_configuration)
    if response:
        return response

def get_bpm_task_by_id(bpm_task_id):
    return utils.checked_api_call(configs_api, "get_bpm_task_by_id", task_id=bpm_task_id )

