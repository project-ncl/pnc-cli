import pytest
from pnc_cli import environments
from pnc_cli.swagger_client.apis.environments_api import EnvironmentsApi
from pnc_cli import utils
from test import testutils


@pytest.fixture(scope='function', autouse=True)
def get_envs_api():
    global envs_api
    envs_api = EnvironmentsApi(utils.get_api_client())


def test_get_all_invalid_param():
    testutils.assert_raises_typeerror(envs_api, 'get_all')


def test_get_all():
    envs = envs_api.get_all(page_index=0, page_size=1000000, sort='', q='').content
    assert envs is not None


def test_create_invalid_param():
    testutils.assert_raises_typeerror(envs_api, 'create_new')


def test_create_new(new_environment):
    env_ids = [env.id for env in envs_api.get_all(page_size=1000000).content]
    assert new_environment.id in env_ids


def test_get_specific_no_id():
    testutils.assert_raises_valueerror(envs_api, 'get_specific', id=None)


def test_get_specific_invalid_param():
    testutils.assert_raises_typeerror(envs_api, 'get_specific', id=1)


def test_get_specific(new_environment):
    assert envs_api.get_specific(id=new_environment.id).content is not None


def test_update_no_id():
    testutils.assert_raises_valueerror(envs_api, 'update', id=None)


def test_update_invalid_param():
    testutils.assert_raises_typeerror(envs_api, 'update', id=1)


def test_update(new_environment):
    randname = testutils.gen_random_name()
    updated_env = environments.create_environment_object(name=randname, system_image_type='VIRTUAL_MACHINE_RAW', description='DOCKER',
                                                         system_image_id=randname)
    envs_api.update(id=new_environment.id, body=updated_env)
    retrieved_env = envs_api.get_specific(new_environment.id).content
    assert (retrieved_env.description == 'DOCKER')
    assert (retrieved_env.name == randname)
    # the following fields are immutable, and should remain unchanged
    assert (retrieved_env.system_image_id == retrieved_env.system_image_id)
    assert (retrieved_env.system_image_type == 'DOCKER_IMAGE')


def test_delete_no_id():
    testutils.assert_raises_valueerror(envs_api, 'delete', id=None)


def test_delete_invalid_param():
    testutils.assert_raises_typeerror(envs_api, 'delete', id=1)


def test_delete(new_environment):
    envs_api.delete(new_environment.id)
    env_ids = [env.id for env in envs_api.get_all(page_size=1000000).content]
    assert new_environment.id not in env_ids
