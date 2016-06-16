import argparse
import re

import pnc_cli.utils as utils
import pnc_cli.common as common
from pnc_cli.swagger_client import BuildconfigsetrecordsApi
from pnc_cli.swagger_client import BuildconfigurationsApi
from pnc_cli.swagger_client import BuildconfigurationsetsApi
from pnc_cli.swagger_client import BuildrecordsApi
from pnc_cli.swagger_client import EnvironmentsApi
from pnc_cli.swagger_client import ProductsApi
from pnc_cli.swagger_client import ProductversionsApi
from pnc_cli.swagger_client import ProjectsApi
from pnc_cli.swagger_client import LicensesApi

api_client = utils.get_api_client()
configs_api = BuildconfigurationsApi(api_client)
products_api = ProductsApi(api_client)
sets_api = BuildconfigurationsetsApi(api_client)
envs_api = EnvironmentsApi(api_client)
projects_api = ProjectsApi(api_client)
versions_api = ProductversionsApi(api_client)
bcsr_api = BuildconfigsetrecordsApi(api_client)
records_api = BuildrecordsApi(api_client)
license_api = LicensesApi(api_client)

bc_name_regex = "^[a-zA-Z0-9_.][a-zA-Z0-9_.-]*(?!\.git)+$"


# Type declarations.
def valid_bc_name(name_input):
    pattern = re.compile(bc_name_regex)
    if not pattern.match(name_input):
        raise argparse.ArgumentTypeError("name contains invalid characters")
    return name_input


def unique_bc_name(name_input):
    if common.get_id_by_name(configs_api, name_input):
        raise argparse.ArgumentTypeError("BuildConfiguration name '{}' is already in use".format(name_input))
    return name_input


def valid_unique_bc_name(name_input):
    unique_bc_name(valid_bc_name(name_input))
    return name_input


def existing_bc_name(name_input):
    valid_bc_name(name_input)
    if not common.get_id_by_name(configs_api, name_input):
        raise argparse.ArgumentTypeError("no BuildConfiguration with the name {} exists".format(name_input))
    return name_input


def existing_bc_id(id_input):
    utils.valid_id(id_input)
    if not common.id_exists(configs_api, id_input):
        raise argparse.ArgumentTypeError("no BuildConfiguration with ID {} exists".format(id_input))
    return id_input


def existing_product_id(id_input):
    utils.valid_id(id_input)
    if not common.id_exists(products_api, id_input):
        raise argparse.ArgumentTypeError("no Product with ID {} exists".format(id_input))
    return id_input


def existing_product_name(name_input):
    if not common.get_id_by_name(products_api, name_input):
        raise argparse.ArgumentTypeError("no Product with the name {} exists".format(name_input))
    return name_input


def unique_product_name(name_input):
    if common.get_id_by_name(products_api, name_input):
        raise argparse.ArgumentTypeError("a Product with the name {} already exists".format(name_input))
    return name_input


def unique_bc_set_name(name_input):
    if common.get_id_by_name(sets_api, name_input):
        raise argparse.ArgumentTypeError("BuildConfigurationSet name '{}' is already in use".format(name_input))
    return name_input


def existing_bc_set_name(name_input):
    if not common.get_id_by_name(sets_api, name_input):
        raise argparse.ArgumentTypeError("no BuildConfigurationSet with the name {} exists".format(name_input))
    return name_input


def existing_set_id(id_input):
    utils.valid_id(id_input)
    if not common.id_exists(sets_api, id_input):
        raise argparse.ArgumentTypeError("no BuildConfigurationSet with ID {} exists".format(id_input))
    return id_input


def existing_environment_id(id_input):
    utils.valid_id(id_input)
    if not common.id_exists(envs_api, id_input):
        raise argparse.ArgumentTypeError("no BuildEnvironment exists with id {}".format(id_input))
    return id_input


def existing_environment_name(name_input):
    if not common.get_id_by_name(envs_api, name_input):
        raise argparse.ArgumentTypeError("no BuildEnvironment exists with name {}".format(name_input))
    return name_input


def unique_environment_name(nameInput):
    if common.get_id_by_name(envs_api, nameInput):
        raise argparse.ArgumentTypeError("a BuildEnvironment with name {} already exists".format(nameInput))
    return nameInput


def existing_project_id(id_input):
    utils.valid_id(id_input)
    if not common.id_exists(projects_api, id_input):
        raise argparse.ArgumentTypeError("no Project with ID {} exists".format(id_input))
    return id_input


def existing_product_version(id_input):
    utils.valid_id(id_input)
    if not common.id_exists(versions_api, id_input):
        raise argparse.ArgumentTypeError("no ProductVersion with ID {} exists.".format(id_input))
    return id_input


def existing_bc_set_record(id_input):
    utils.valid_id(id_input)
    if not common.id_exists(bcsr_api, id_input):
        raise argparse.ArgumentTypeError("no BuildConfigurationSetRecord with ID {} exists".format(id_input))
    return id_input


def existing_build_record(id_input):
    utils.valid_id(id_input)
    if not common.id_exists(records_api, id_input):
        raise argparse.ArgumentTypeError("no BuildRecord with ID {} exists".format(id_input))
    return id_input


def existing_license_id(license_id):
    utils.valid_id(license_id)
    if not common.id_exists(license_api, license_id):
        raise argparse.ArgumentTypeError("No license with id {} exists".format(license_id))
    return license_id


def existing_license_name(name):
    utils.valid_id(name)
    if not common.id_exists(license_api, name):
        raise argparse.ArgumentTypeError("No license with name {} exists".format(name))
    return name