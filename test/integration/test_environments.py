from pnc import environments

def _create_env():
    return environments.create_environment("java", "linux")

def test_list_environments():
    envs = environments.list_environments
    assert envs is not None

def test_list_environments_attribute():
    envs = environments.list_environments(attributes="name")
    assert envs is not None

def test_create_environment():
    new_env = _create_env()
    envs = environments.list_environments(attributes="name")
    env_ids = [env['id'] for env in envs]
    assert new_env['id'] in env_ids

def test_get_environment():
    newenv = _create_env()
    assert environments.get_environment(newenv['id']) is not None

def test_delete_environment():
    new_env = _create_env()
    environments.delete_environment(new_env['id'])
    envs = environments.list_environments(attributes='id')
    env_ids = [env['id'] for env in envs]
    assert new_env['id'] not in env_ids

def test_update_environment():
    new_env = _create_env()
    environments.update_environment(new_env['id'], "DOCKER", "WINDOWS")
    updated_env = environments.get_environment(new_env['id'])
    assert updated_env['buildType'] == 'DOCKER'
    assert updated_env['operationalSystem'] == 'WINDOWS'


