from argh import arg

import logging
import pnc_cli.cli_types as types
from pnc_cli import swagger_client
from pnc_cli import utils
from pnc_cli.swagger_client import BpmApi
from pnc_cli.swagger_client import EnvironmentsApi
from pnc_cli.swagger_client import ProjectsApi
import pnc_cli.user_config as uc

projects_api = ProjectsApi(uc.user.get_api_client())
bpm_api = BpmApi(uc.user.get_api_client())
envs_api = EnvironmentsApi(uc.user.get_api_client())

def create_build_conf_object(**kwargs):
    created_build_configuration = swagger_client.BpmBuildConfigurationCreationRest()
    for key, value in kwargs.items():
        setattr(created_build_configuration, str(key), value)
    return created_build_configuration

@arg("name", help="Name for the new BuildConfiguration.", type=types.unique_bc_name)
# allow specifying project by name?
@arg("project_id", help="ID of the Project to associate the BuildConfiguration with.", type=types.existing_project_id)
@arg("build_environment_id", help="ID of the Environment for the new BuildConfiguration.",
     type=types.existing_environment_id)
@arg("build_script", help="Script to execute for the BuildConfiguration.")
@arg("-iurl", "--scm_repo_url", type=types.valid_internal_url, help="Internal repository URL to the sources of the BuildConfiguration.")
@arg("-irev", "--scm_revision", help="Revision of the internal repository sources for this BuildConfiguration.")
@arg("-exturl", "--scm_external_repo_url", type=types.valid_url, help="URL to the external sources of the BuildConfiguration.")
@arg("-extrev", "--scm_external_revision", help="Revision of the external sources in scm-url for this BuildConfiguration.")
@arg("-d", "--description", help="Description of the new build configuration.")
@arg("-pvi", "--product-version-id", type=types.existing_product_version, help="Associated ProductVersion ID.")
@arg("-dids", "--dependency-ids", type=types.existing_bc_id, nargs="+",
     help="List of BuildConfiguration IDs that are dependencies of this BuildConfiguration.")
@arg("-bcsids", "--build-configuration-set-ids", type=types.existing_bc_set_id, nargs="+", help="List of BuildConfiguration set IDs this BuildConfiguration should be a member of.")
@arg("-gp", "--generic-parameters", help="Set of arbitrary additional key=value pairs.")
def create_build_configuration(**kwargs):
    """
    Create a new BuildConfiguration. BuildConfigurations represent the settings and configuration required to run a build of a specific version of the associated Project's source code.
    If a ProductVersion ID is provided, the BuildConfiguration will have access to artifacts which were produced for that version, but may not have been released yet.
    :return BPM Task ID of the new BuildConfiguration creation
    """
    scm_repo_url = kwargs.get("scm_repo_url")
    external_url = kwargs.get("scm_external_repo_url")


    if scm_repo_url is None and external_url is None:
        logging.error("At least one scm-url must be specified.")
        return

    if scm_repo_url and kwargs.get("scm_revision") is None:
        logging.error("The repository revision must be provided for the internal repository.")
        return

    if external_url and kwargs.get('scm_external_revision') is None:
        logging.error("The external repository revision must be provided for the external repository.")
        return

    if not kwargs.get("dependency_ids"):
        kwargs["dependency_ids"] = []

    if not kwargs.get("build_configuration_set_ids"):
        kwargs["build_configuration_set_ids"] = []

    if not kwargs.get("generic_parameters"):
        kwargs["generic_parameters"] = {}

    build_configuration = create_build_conf_object(**kwargs)
    response = utils.checked_api_call(
        bpm_api, 'start_bc_creation_task', body=build_configuration)
    if response:
        return response

def get_bpm_task_by_id(bpm_task_id):
    return utils.checked_api_call(bpm_api, "get_bpm_task_by_id", task_id=bpm_task_id)

