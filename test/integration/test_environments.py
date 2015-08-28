from pnc import environments

def _create_env_object(os, bt):
    return environments._create_environment_object(os,bt)

def _create_env(env=None):
    if env is None:
        return environments.create(_create_env_object("java","linux")).json()
    else:
        return environments.create(env).json()

def test_get_all():
    envs = environments.get_all().json()
    assert envs is not None

def test_create():
    new_env = _create_env()
    envs = environments.get_all().json()
    env_ids = [env['id'] for env in envs]
    assert new_env['id'] in env_ids

def test_get_specific():
    newenv = _create_env()
    assert environments.get_specific(newenv['id']) is not None

def test_delete():
    new_env = _create_env()
    environments.delete(new_env['id'])
    envs = environments.get_all().json()
    env_ids = [env['id'] for env in envs]
    assert new_env['id'] not in env_ids

def test_update():
    new_env = _create_env()
    updated_env = _create_env_object("DOCKER","WINDOWS")
    environments.update(new_env['id'], updated_env)
    updated_env = environments.get_specific(new_env['id']).json()
    assert (updated_env['buildType'] == 'DOCKER') and (updated_env['operationalSystem'] == 'WINDOWS')


