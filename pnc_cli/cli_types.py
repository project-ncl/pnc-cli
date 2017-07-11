import argparse
import datetime
import re
import validators
from tzlocal import get_localzone
import pnc_cli.common as common
import pnc_cli.utils as utils
from pnc_cli.swagger_client import BuildconfigsetrecordsApi
from pnc_cli.swagger_client import BuildconfigurationsApi
from pnc_cli.swagger_client import BuildconfigurationsetsApi
from pnc_cli.swagger_client import BuildrecordsApi
from pnc_cli.swagger_client import EnvironmentsApi
from pnc_cli.swagger_client import LicensesApi
from pnc_cli.swagger_client import ProductmilestonesApi
from pnc_cli.swagger_client import ProductreleasesApi
from pnc_cli.swagger_client import ProductsApi
from pnc_cli.swagger_client import ProductversionsApi
from pnc_cli.swagger_client import ProjectsApi
from pnc_cli.swagger_client import RepositoryconfigurationsApi
from pnc_cli.swagger_client import RunningbuildrecordsApi
import pnc_cli.user_config as uc
import requests

api_client = uc.user.get_api_client()

# BuildConfigurations
configs_api = BuildconfigurationsApi(api_client)
repos_api = RepositoryconfigurationsApi(api_client)
sets_api = BuildconfigurationsetsApi(api_client)

envs_api = EnvironmentsApi(api_client)

projects_api = ProjectsApi(api_client)

# Product related APIs
products_api = ProductsApi(api_client)
versions_api = ProductversionsApi(api_client)
milestones_api = ProductmilestonesApi(api_client)
releases_api = ProductreleasesApi(api_client)

# Build Configuration Set Records
bcsr_api = BuildconfigsetrecordsApi(api_client)

# Build Records
records_api = BuildrecordsApi(api_client)
license_api = LicensesApi(api_client)

# Licenses API
licenses_api = LicensesApi(api_client)

# Running build records Api
running_api = RunningbuildrecordsApi(api_client)

bc_name_regex = "^[a-zA-Z0-9_.][a-zA-Z0-9_.-]*(?!\.git)+$"


# BuildConfiguration Types
def valid_bc_name(name_input):
    pattern = re.compile(bc_name_regex)
    if not pattern.match(name_input):
        raise argparse.ArgumentTypeError("name contains invalid characters")
    return name_input


def unique_bc_name(name_input):
    valid_bc_name(name_input)
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
    valid_id(id_input)
    if not common.id_exists(configs_api, id_input):
        raise argparse.ArgumentTypeError("no BuildConfiguration with ID {} exists".format(id_input))
    return id_input

# RepositoryConfiguration Types
def existing_rc_id(id_input):
    valid_id(id_input)
    if not common.id_exists(repos_api, id_input):
        raise argparse.ArgumentTypeError("no RepositoryConfiguration with ID {} exists".format(id_input))

# Product Types
def existing_product_id(id_input):
    valid_id(id_input)
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


def valid_abbreviation(abbreviation_input):
    if len(abbreviation_input) < 0 or len(abbreviation_input) > 20:
        raise argparse.ArgumentTypeError("a Product abbreviation must be between 0 and 20 characters")
    return abbreviation_input


def unique_product_abbreviation(abbreviation_input):
    valid_abbreviation(abbreviation_input)
    if products_api.get_all(q='abbreviation==' + abbreviation_input).content:
        raise argparse.ArgumentTypeError("a Product with the abbreviation {} already exists".format(abbreviation_input))
    return abbreviation_input


# ProductVersion types
def existing_product_version(id_input):
    valid_id(id_input)
    if not common.id_exists(versions_api, id_input):
        raise argparse.ArgumentTypeError("no ProductVersion with ID {} exists".format(id_input))
    return id_input


def valid_version_two_digits(version):
    if not utils.is_valid_version(version, '^\d+\.\d+'):
        raise argparse.ArgumentTypeError("Version should consist of two numeric parts separated by a dot.")
    return version


# ProductMilestone types
def existing_product_milestone(id_input):
    valid_id(id_input)
    if not common.id_exists(milestones_api, id_input):
        raise argparse.ArgumentTypeError("no ProductMilestone with ID {} exist".format(id_input))
    return id_input


def valid_version_create(version):
    if not utils.is_valid_version(version, '^\d+\.\w+$'):
        raise argparse.ArgumentTypeError(
            "Version must start with a number, followed by a dot and then a qualifier (e.g ER1).")
    return version


def valid_version_update(version):
    if not utils.is_valid_version(version, '^\d+\.\d+\.\d+\.\w+$'):
        raise argparse.ArgumentTypeError(
            "The version should consist of three numeric parts and one alphanumeric qualifier each separated by a dot.")
    return version


# ProductRelease types
def existing_product_release(id_input):
    valid_id(id_input)
    if not common.id_exists(releases_api, id_input):
        raise argparse.ArgumentTypeError("no ProductRelease with ID {} exists.".format(id_input))
    return id_input


# BuildConfigurationSet types
def unique_bc_set_name(name_input):
    if common.get_id_by_name(sets_api, name_input):
        raise argparse.ArgumentTypeError("BuildConfigurationSet name '{}' is already in use".format(name_input))
    return name_input


def existing_bc_set_name(name_input):
    if not common.get_id_by_name(sets_api, name_input):
        raise argparse.ArgumentTypeError("no BuildConfigurationSet with the name {} exists".format(name_input))
    return name_input


def existing_bc_set_id(id_input):
    valid_id(id_input)
    if not common.id_exists(sets_api, id_input):
        raise argparse.ArgumentTypeError("no BuildConfigurationSet with ID {} exists".format(id_input))
    return id_input


# BuildEnvironmentTypes
def existing_environment_id(id_input):
    valid_id(id_input)
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


# Project Types
def existing_project_id(id_input):
    valid_id(id_input)
    if not common.id_exists(projects_api, id_input):
        raise argparse.ArgumentTypeError("no Project with ID {} exists".format(id_input))
    return id_input


def existing_project_name(name_input):
    if not common.get_id_by_name(projects_api, name_input):
        raise argparse.ArgumentTypeError("no Project with name {} exists".format(name_input))
    return name_input


def unique_project_name(name_input):
    if common.get_id_by_name(projects_api, name_input):
        raise argparse.ArgumentTypeError("a Project with name {} already exists".format(name_input))
    return name_input


# BuildConfigurationSetRecord types
def existing_bc_set_record(id_input):
    valid_id(id_input)
    if not common.id_exists(bcsr_api, id_input):
        raise argparse.ArgumentTypeError("no BuildConfigurationSetRecord with ID {} exists".format(id_input))
    return id_input


# BuildRecord types
def existing_build_record(id_input):
    valid_id(id_input)
    if not common.id_exists(records_api, id_input):
        raise argparse.ArgumentTypeError("no BuildRecord with ID {} exists".format(id_input))
    return id_input


def existing_built_artifact(id_input):
    pass


# License types
def existing_license(id_input):
    valid_id(id_input)
    if not common.id_exists(licenses_api, id_input):
        raise argparse.ArgumentTypeError("no License with ID {} exists".format(id_input))
    return id_input


# Running build records types
def existing_running_build(id_input):
    valid_id(id_input)
    if not common.id_exists(running_api, id_input):
        raise argparse.ArgumentTypeError("no RunningBuild with ID {} exists".format(id_input))
    return id_input


# Misc types
def valid_date(dateInput):
    try:
        dateInput = get_localzone().localize(datetime.datetime.strptime(dateInput, '%Y-%m-%d'))
    except ValueError:
        raise argparse.ArgumentTypeError("Date format: yyyy-mm-dd")
    return dateInput


def valid_id(id_input):
    if not id_input.isdigit():
        raise argparse.ArgumentTypeError("An ID must be a positive integer")
    return id_input


def valid_url(urlInput):
    if not validators.url(urlInput):
        raise argparse.ArgumentTypeError("Invalid url")
    return urlInput

def t_or_f(arg):
    ua = str(arg).upper()
    if 'TRUE'.startswith(ua):
       return True
    elif 'FALSE'.startswith(ua):
       return False
    else:
       raise argparse.ArgumentTypeError("Only true or false is possible.")

# validation is different depnding on the PNC url.
def valid_internal_url(urlInput):
    repo_start = utils.get_internal_repo_start(uc.user.pnc_config.url)
    if not urlInput.startswith(repo_start):
        raise argparse.ArgumentTypeError("An internal SCM repository URL must start with: " + repo_start)
    if urlInput == repo_start:
        raise argparse.ArgumentTypeError("No specific internal repository specified.")
    valid_url(urlInput)
    return urlInput
