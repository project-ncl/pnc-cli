import argh.exceptions

import pnc_cli.utils as utils

"""
Utility module that contains generalized API calls for use in other modules.
"""


def id_exists(api, search_id):
    """
    Test if an ID exists within any arbitrary API
    :param api: api to search for search_id
    :param search_id: id to test for
    :return: True if an entity with ID search_id exists, false otherwise
    """
    response = utils.checked_api_call(api, 'get_specific', id=search_id)
    return response is not None


def get_id_by_name(api, search_name):
    """
    calls 'get_all' on the given API with a search name and returns the ID of the entity retrieved, if any, None otherwise
    :param api: api to search
    :param search_name: name to test for
    :return ID of entity matching search_name, None otherwise
    """
    entities = api.get_all(q='name==' + "'" + search_name + "'").content
    if entities:
        return entities[0].id
    return


def set_id(api, id, name):
    if id:
        return id
    elif name:
        return get_id_by_name(api, name)
    else:
        raise argh.exceptions.CommandError("One of ID or Name is required.")


def get_entity(api, entity_id):
    """
    Generic "getSpecific" call that calls get_specific with the given id
    :param api: api to call get_specific on
    :param id: id of the entity to retrieve
    :return: REST entity
    """
    response = utils.checked_api_call(api, 'get_specific', id=entity_id)
    if response:
        return response.content
    return
