from argh import arg
from six import iteritems

__author__ = 'thauser'

from pnc_cli.swagger_client import UsersApi
from pnc_cli.swagger_client import UserRest
from pnc_cli import utils

users_api = UsersApi(utils.get_api_client())


def user_exists(user_id):
    existing = utils.checked_api_call(users_api, 'get_specific', id=user_id)
    if existing:
        return True
    return False


def get_user_id_by_name(name):
    users = users_api.get_all(q='username==' + name).content
    if users:
        user = users[0]
        return user.id
    return None


def get_user_id(id, name):
    if id:
        found_id = id
        if not user_exists(id):
            print("No User with ID {} exists.".format(id))
            return
    elif name:
        found_id = get_user_id_by_name(name)
        if not found_id:
            print("No User with username {} exists.".format(name))
            return
    else:
        print("Either a User's name or ID is required.")
        return
    return found_id


def create_user_object(**kwargs):
    created = UserRest()
    for key, value in iteritems(kwargs):
        setattr(created, key, value)
    return created


def list_users():
    """
    List all Users
    """
    response = utils.checked_api_call(users_api, 'get_all')
    if response:
        return response.content


@arg('-i', '--id', help='ID for the User to retrieve.')
@arg('-n', '--name', help='Username of the User to retrieve.')
def get_user(id=None, name=None):
    """
    Get a specific User
    """
    found_id = get_user_id(id, name)
    if not found_id:
        return
    response = utils.checked_api_call(users_api, 'get_specific', id=found_id)
    if response:
        return response.content


@arg('username', help='Username for the new User.')
@arg('-e', '--email', help='Email address for the new User.')
@arg('-fn', '--first-name', help="User's first name.")
@arg('-ln', '--last-name', help="User's last name.")
def create_user(username, **kwargs):
    """
    Create a new User
    """
    user = create_user_object(username=username, **kwargs)
    response = utils.checked_api_call(users_api, 'create_new', body=user)
    if response:
        return response.content


@arg('-i', '--id', help='ID of the User to update.')
@arg('-n', '--name', help='Username for the User to update.')
@arg('-u', '--username', help='New username for the User.')
@arg('-fn', '--first-name', help='New first name.')
@arg('-ln', '--last-name', help='New last name.')
@arg('-e', '--email', help='New email.')
def update_user(id=None, name=None, **kwargs):
    found_id = get_user_id(id, name)
    if not found_id:
        return

    to_update = users_api.get_specific(id=found_id).content

    for key, value in iteritems(kwargs):
        if value is not None:
            setattr(to_update, key, value)

    response = utils.checked_api_call(users_api, 'update', id=found_id, body=to_update)
    if response:
        return response.content
