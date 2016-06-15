import argparse
import re

import pnc_cli.utils as utils
from pnc_cli.swagger_client import BuildconfigurationsApi
from pnc_cli.swagger_client import BuildconfigurationsetsApi
from pnc_cli.swagger_client import ProductsApi

api_client = utils.get_api_client()
configs_api = BuildconfigurationsApi(api_client)
products_api = ProductsApi(api_client)
sets_api = BuildconfigurationsetsApi(api_client)

bc_name_regex = "^[a-zA-Z0-9_.][a-zA-Z0-9_.-]*(?!\.git)+$"


# Type declarations.
def valid_bc_name(name_input):
    pattern = re.compile(bc_name_regex)
    if not pattern.match(name_input):
        raise argparse.ArgumentTypeError("name contains invalid characters")
    return name_input


def unique_bc_name(name_input):
    if get_id_by_name(configs_api, name_input):
        raise argparse.ArgumentTypeError("BuildConfiguration name '{}' is already in use".format(name_input))
    return name_input


def valid_unique_bc_name(name_input):
    unique_bc_name(valid_bc_name(name_input))
    return name_input


def existing_bc_name(name_input):
    valid_bc_name(name_input)
    if not get_id_by_name(configs_api, name_input):
        raise argparse.ArgumentTypeError("no BuildConfiguration with the name {} exists".format(name_input))
    return name_input


def existing_bc_id(id_input):
    utils.valid_id(id_input)
    if not id_exists(configs_api, id_input):
        raise argparse.ArgumentTypeError("no BuildConfiguration with ID {} exists".format(id_input))
    return id_input


def existing_product_id(id_input):
    utils.valid_id(id_input)
    if not id_exists(products_api, id_input):
        raise argparse.ArgumentTypeError("no Product with ID {} exists".format(id_input))
    return id_input


def existing_product_name(name_input):
    if not get_id_by_name(products_api, name_input):
        raise argparse.ArgumentTypeError("no Product with the name {} exists".format(name_input))
    return name_input


def unique_product_name(name_input):
    if get_id_by_name(products_api, name_input):
        raise argparse.ArgumentTypeError("a Product with the name {} already exists".format(name_input))
    return name_input


def unique_build_configuration_set_name(name_input):
    if get_id_by_name(sets_api, name_input):
        raise argparse.ArgumentTypeError("BuildConfigurationSet name '{}' is already in use".format(name_input))
    return name_input


def existing_set_name(name_input):
    if not get_id_by_name(sets_api, name_input):
        raise argparse.ArgumentTypeError("no BuildConfigurationSet with the name {} exists".format(name_input))
    return name_input


def existing_set_id(id_input):
    utils.valid_id(id_input)
    if not id_exists(sets_api, id_input):
        raise argparse.ArgumentTypeError("no BuildConfigurationSet with ID {} exists".format(id_input))
    return id_input


# Utility functions. Possibly should go in "common.py"
def id_exists(api, search_id):
    """
    Test if an ID exists within any arbitrary API
    :param search_id: id to test for
    :return: True if an entity with ID search_id exists, false otherwise
    """
    response = utils.checked_api_call(api, 'get_specific', id=search_id)
    if not response:
        return False
    return True


def get_id_by_name(api, search_name):
    """
    calls 'get_all' on the given API with a search name and returns the ID of the entity retrieved, if any, None otherwise
    """
    entities = api.get_all(q='name==' + search_name).content
    if entities:
        return entities[0].id
    return
