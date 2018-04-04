import argparse
import datetime
import re
import validators
from tzlocal import get_localzone
import pnc_cli.common as common
import pnc_cli.utils as utils
from pnc_cli.pnc_api import pnc_api
import requests


bc_name_regex = "^[a-zA-Z0-9_.][a-zA-Z0-9_.-]*(?!\.git)+$"


# BuildConfiguration Types
def valid_bc_name(name_input):
    pattern = re.compile(bc_name_regex)
    if not pattern.match(name_input):
        raise argparse.ArgumentTypeError("name contains invalid characters")
    return name_input


def unique_bc_name(name_input):
    valid_bc_name(name_input)
    if common.get_id_by_name(pnc_api.build_configs, name_input):
        raise argparse.ArgumentTypeError("BuildConfiguration name '{}' is already in use".format(name_input))
    return name_input


def valid_unique_bc_name(name_input):
    unique_bc_name(valid_bc_name(name_input))
    return name_input


def existing_bc_name(name_input):
    valid_bc_name(name_input)
    if not common.get_id_by_name(pnc_api.build_configs, name_input):
        raise argparse.ArgumentTypeError("no BuildConfiguration with the name {} exists".format(name_input))
    return name_input


def existing_bc_id(id_input):
    valid_id(id_input)
    if not common.id_exists(pnc_api.build_configs, id_input):
        raise argparse.ArgumentTypeError("no BuildConfiguration with ID {} exists".format(id_input))
    return id_input

# RepositoryConfiguration Types
def existing_rc_id(id_input):
    valid_id(id_input)
    if not common.id_exists(pnc_api.repositories, id_input):
        raise argparse.ArgumentTypeError("no RepositoryConfiguration with ID {} exists".format(id_input))

# Product Types
def existing_product_id(id_input):
    valid_id(id_input)
    if not common.id_exists(pnc_api.products, id_input):
        raise argparse.ArgumentTypeError("no Product with ID {} exists".format(id_input))
    return id_input


def existing_product_name(name_input):
    if not common.get_id_by_name(pnc_api.products, name_input):
        raise argparse.ArgumentTypeError("no Product with the name {} exists".format(name_input))
    return name_input


def unique_product_name(name_input):
    if common.get_id_by_name(pnc_api.products, name_input):
        raise argparse.ArgumentTypeError("a Product with the name {} already exists".format(name_input))
    return name_input


def valid_abbreviation(abbreviation_input):
    if len(abbreviation_input) < 0 or len(abbreviation_input) > 20:
        raise argparse.ArgumentTypeError("a Product abbreviation must be between 0 and 20 characters")
    return abbreviation_input


def unique_product_abbreviation(abbreviation_input):
    valid_abbreviation(abbreviation_input)
    if pnc_api.products.get_all(q='abbreviation==' + abbreviation_input).content:
        raise argparse.ArgumentTypeError("a Product with the abbreviation {} already exists".format(abbreviation_input))
    return abbreviation_input


# ProductVersion types
def existing_product_version(id_input):
    valid_id(id_input)
    if not common.id_exists(pnc_api.product_versions, id_input):
        raise argparse.ArgumentTypeError("no ProductVersion with ID {} exists".format(id_input))
    return id_input


def valid_version_two_digits(version):
    if not utils.is_valid_version(version, '^\d+\.\d+'):
        raise argparse.ArgumentTypeError("Version should consist of two numeric parts separated by a dot.")
    return version


# ProductMilestone types
def existing_product_milestone(id_input):
    valid_id(id_input)
    if not common.id_exists(pnc_api.product_milestones, id_input):
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
    if not common.id_exists(pnc_api.product_releases, id_input):
        raise argparse.ArgumentTypeError("no ProductRelease with ID {} exists.".format(id_input))
    return id_input


# BuildConfigurationSet types
def unique_bc_set_name(name_input):
    if common.get_id_by_name(pnc_api.build_group_configs, name_input):
        raise argparse.ArgumentTypeError("BuildConfigurationSet name '{}' is already in use".format(name_input))
    return name_input


def existing_bc_set_name(name_input):
    if not common.get_id_by_name(pnc_api.build_group_configs, name_input):
        raise argparse.ArgumentTypeError("no BuildConfigurationSet with the name {} exists".format(name_input))
    return name_input


def existing_bc_set_id(id_input):
    valid_id(id_input)
    if not common.id_exists(pnc_api.build_group_configs, id_input):
        raise argparse.ArgumentTypeError("no BuildConfigurationSet with ID {} exists".format(id_input))
    return id_input


# BuildEnvironmentTypes
def existing_environment_id(id_input):
    valid_id(id_input)
    if not common.id_exists(pnc_api.environments, id_input):
        raise argparse.ArgumentTypeError("no BuildEnvironment exists with id {}".format(id_input))
    return id_input


def existing_environment_name(name_input):
    if not common.get_id_by_name(pnc_api.environments, name_input):
        raise argparse.ArgumentTypeError("no BuildEnvironment exists with name {}".format(name_input))
    return name_input


def unique_environment_name(nameInput):
    if common.get_id_by_name(pnc_api.environments, nameInput):
        raise argparse.ArgumentTypeError("a BuildEnvironment with name {} already exists".format(nameInput))
    return nameInput


# Project Types
def existing_project_id(id_input):
    valid_id(id_input)
    if not common.id_exists(pnc_api.projects, id_input):
        raise argparse.ArgumentTypeError("no Project with ID {} exists".format(id_input))
    return id_input


def existing_project_name(name_input):
    if not common.get_id_by_name(pnc_api.projects, name_input):
        raise argparse.ArgumentTypeError("no Project with name {} exists".format(name_input))
    return name_input


def unique_project_name(name_input):
    if common.get_id_by_name(pnc_api.projects, name_input):
        raise argparse.ArgumentTypeError("a Project with name {} already exists".format(name_input))
    return name_input


# BuildConfigurationSetRecord types
def existing_bc_set_record(id_input):
    valid_id(id_input)
    if not common.id_exists(pnc_api.build_groups, id_input):
        raise argparse.ArgumentTypeError("no BuildConfigurationSetRecord with ID {} exists".format(id_input))
    return id_input


# BuildRecord types
def existing_build_record(id_input):
    valid_id(id_input)
    if not common.id_exists(pnc_api.builds, id_input):
        raise argparse.ArgumentTypeError("no BuildRecord with ID {} exists".format(id_input))
    return id_input


def existing_built_artifact(id_input):
    pass


# License types
def existing_license(id_input):
    valid_id(id_input)
    if not common.id_exists(pnc_api.licenses, id_input):
        raise argparse.ArgumentTypeError("no License with ID {} exists".format(id_input))
    return id_input


# Running build records types
def existing_running_build(id_input):
    valid_id(id_input)
    if not common.id_exists(pnc_api.running_builds, id_input):
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

