from pnc_cli import environments
from pnc_cli.swagger_client.apis.environments_api import EnvironmentsApi
from pnc_cli import utils

envs_api = EnvironmentsApi(utils.get_api_client())

def _create_env(bt="java"):
    return envs_api.create_new(body=environments._create_environment_object(build_type=bt.upper(),name=utils.gen_random_name())).content

def test_get_all():
    envs = envs_api.get_all().content
    assert envs is not None

def test_create():
    new_env = _create_env()
    env_ids = [env.id for env in envs_api.get_all().content]
    assert new_env.id in env_ids

def test_get_specific():
    newenv = _create_env()
    assert envs_api.get_specific(id=newenv.id).content is not None

def test_delete():
    new_env = _create_env()
    envs_api.delete(new_env.id)
    env_ids = [env.id for env in envs_api.get_all().content]
    assert new_env.id not in env_ids

def test_update():
    new_env = _create_env()
    updated_env = environments._create_environment_object(build_type="DOCKER",name="test-BuildEnvironmentName")
    envs_api.update(id=new_env.id, body=updated_env)
    retrieved_env = envs_api.get_specific(new_env.id).content
    assert (retrieved_env.build_type == 'DOCKER') and (retrieved_env.name == 'test-BuildEnvironmentName')


