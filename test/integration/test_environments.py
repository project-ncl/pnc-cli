from pnc import environments

def _create_env(bt="java", os="linux"):
    return environments.create(environments._create_environment_object(buildType=bt.upper(),operationalSystem=os.upper())).json()

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
    updated_env = environments._create_environment_object(buildType="DOCKER",operationalSystem="WINDOWS")
    environments.update(new_env['id'], updated_env)
    updated_env = environments.get_specific(new_env['id']).json()
    assert (updated_env['buildType'] == 'DOCKER') and (updated_env['operationalSystem'] == 'WINDOWS')


