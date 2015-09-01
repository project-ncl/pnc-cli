import random
import string
from pnc import buildconfigurations

def _add_config():
    randname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    return buildconfigurations.create(buildconfigurations.create_build_conf_object(name=randname, projectId=1, environmentId=1)).json()

def test_get_all():
    build_configurations = buildconfigurations.get_all()
    assert build_configurations is not None

def test_create_build_configuration():
    new_config = _add_config()
    bcs = buildconfigurations.get_all().json()
    bc_names = [bc['name'] for bc in bcs]
    assert new_config['name'] in bc_names

def test_build_trigger():
    new_config = _add_config()
    running_build = buildconfigurations.trigger(new_config['id'])
    assert running_build.ok

def test_build_configuration_exists():
    created_bc = _add_config()
    assert buildconfigurations.build_configuration_exists(created_bc['id']) is True

def test_get_build_configuration_id_by_name():
    created_bc = _add_config()
    assert buildconfigurations.get_build_configuration_id_by_name(name=created_bc['name']) == created_bc['id']
