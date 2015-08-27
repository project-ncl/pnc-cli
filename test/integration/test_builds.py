import random
import string
from pnc import builds

def _add_config():
    randname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    return builds.create(builds._create_build_conf_object(randname, 1, 1)).json()

def test_create_build_configuration():
    new_config = _add_config()
    bcs = builds.get_all().json()
    bc_names = [bc['name'] for bc in bcs]
    assert new_config['name'] in bc_names

def test_get_all():
    build_configurations = builds.get_all()
    assert build_configurations is not None

def test_build_trigger():
    randname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    builds.create_build_configuration(randname, 1, 1)
    builds.build(name=randname)

def test_build_configuration_exists():
    randname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    created_bc = builds.create_build_configuration(randname, 1, 1)
    assert builds._build_configuration_exists(created_bc['id']) is True

def test_get_build_configuration_id_by_name():
    created_bc = _add_config()
    assert builds._get_build_configuration_id_by_name(name=created_bc['name']) == created_bc['id']
