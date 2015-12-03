import pytest
from pnc_cli import environments
from pnc_cli.swagger_client.apis.environments_api import EnvironmentsApi
from pnc_cli import utils
from test import testutils

envs_api = EnvironmentsApi(utils.get_api_client())


@pytest.fixture(scope='function')
def new_env(request):
    env = envs_api.create_new(
        body=environments._create_environment_object(name=testutils.gen_random_name())).content

    def teardown():
        if env.id in [x.id for x in envs_api.get_all(page_size=1000000).content]:
            envs_api.delete(id=env.id)

    request.addfinalizer(teardown)
    return env


def test_get_all_invalid_param():
    testutils.assert_raises_typeerror(envs_api, 'get_all')


def test_get_all():
    envs = envs_api.get_all(page_index=0, page_size=1000000, sort='', q='').content
    assert envs is not None


def test_create_invalid_param():
    testutils.assert_raises_typeerror(envs_api, 'create_new')


def test_create_new(new_env):
    env_ids = [env.id for env in envs_api.get_all(page_size=1000000).content]
    assert new_env.id in env_ids


def test_get_specific_no_id():
    testutils.assert_raises_valueerror(envs_api, 'get_specific', id=None)


def test_get_specific_invalid_param():
    testutils.assert_raises_typeerror(envs_api, 'get_specific', id=1)


def test_get_specific(new_env):
    assert envs_api.get_specific(id=new_env.id).content is not None


def test_update_no_id():
    testutils.assert_raises_valueerror(envs_api, 'update', id=None)


def test_update_invalid_param():
    testutils.assert_raises_typeerror(envs_api, 'update', id=1)


def test_update(new_env):
    randname = testutils.gen_random_name()
    updated_env = environments._create_environment_object(description="DOCKER", name=randname)
    envs_api.update(id=new_env.id, body=updated_env)
    retrieved_env = envs_api.get_specific(new_env.id).content
    assert (retrieved_env.description == 'DOCKER') and (retrieved_env.name == randname)


def test_delete_no_id():
    testutils.assert_raises_valueerror(envs_api, 'delete', id=None)


def test_delete_invalid_param():
    testutils.assert_raises_typeerror(envs_api, 'delete', id=1)


def test_delete(new_env):
    envs_api.delete(new_env.id)
    env_ids = [env.id for env in envs_api.get_all(page_size=1000000).content]
    assert new_env.id not in env_ids



