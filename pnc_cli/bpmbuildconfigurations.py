from argh import arg

import ast
import logging
import pnc_cli.cli_types as types
from pnc_cli import swagger_client
from pnc_cli import utils
from pnc_cli.pnc_api import pnc_api

def create_build_conf_object(**kwargs):
    created_build_configuration = swagger_client.BuildConfigurationRest()
    for key, value in kwargs.items():
        setattr(created_build_configuration, str(key), value)
    return created_build_configuration

@arg("name", help="Name for the new BuildConfiguration.", type=types.unique_bc_name)
# allow specifying project by name?
@arg("project_id", help="ID of the Project to associate the BuildConfiguration with.", type=types.existing_project_id)
@arg("build_environment_id", help="ID of the Environment for the new BuildConfiguration.",
     type=types.existing_environment_id)
@arg("build_script", help="Script to execute for the BuildConfiguration.")
@arg("repository", help="Repository URL to the sources of the BuildConfiguration.")
@arg("revision", help="Revision of the repository sources for this BuildConfiguration.")
@arg("-d", "--description", help="Description of the new build configuration.")
@arg("-pvi", "--product-version-id", type=types.existing_product_version, help="Associated ProductVersion ID.")
@arg("-dids", "--dependency-ids", type=types.existing_bc_id, nargs="+",
     help="List of BuildConfiguration IDs that are dependencies of this BuildConfiguration.")
@arg("-bcsids", "--build-configuration-set-ids", type=types.existing_bc_set_id, nargs="+", help="List of BuildConfiguration set IDs this BuildConfiguration should be a member of.")
@arg("-gp", "--generic-parameters", help="Set of arbitrary additional key=value pairs.")
def create_build_configuration_process(repository, revision, **kwargs):
    """
    Create a new BuildConfiguration. BuildConfigurations represent the settings and configuration required to run a build of a specific version of the associated Project's source code.
    If a ProductVersion ID is provided, the BuildConfiguration will have access to artifacts which were produced for that version, but may not have been released yet.
    :return BPM Task ID of the new BuildConfiguration creation
    """

    if not kwargs.get("dependency_ids"):
        kwargs["dependency_ids"] = []

    if not kwargs.get("build_configuration_set_ids"):
        kwargs["build_configuration_set_ids"] = []

    if kwargs.get("generic_parameters"):
        kwargs["generic_parameters"] = ast.literal_eval(kwargs.get("generic_parameters"))


    if not kwargs.get("project"):
        kwargs["project"] = pnc_api.projects.get_specific(kwargs.get("project_id")).content
    if not kwargs.get("environment"):
        kwargs["environment"] = pnc_api.environments.get_specific(kwargs.get("build_environment_id")).content

    build_configuration = create_build_conf_object(scm_revision=revision, **kwargs)
    repo_creation = swagger_client.RepositoryCreationUrlAutoRest()
    repo_creation.scm_url = repository
    repo_creation.build_configuration_rest = build_configuration

    response = utils.checked_api_call(
        pnc_api.bpm, 'start_r_creation_task_with_single_url', body=repo_creation)
    if response:
        return response

def get_bpm_task_by_id(bpm_task_id):
    return utils.checked_api_call(pnc_api.bpm, "get_bpm_task_by_id", task_id=bpm_task_id)

