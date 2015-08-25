import random
import string
from pnc import builds

def _add_config():
    randname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    return builds.create_build_configuration(randname, 1, 1)

def test_create_build_configuration():
    new_config = _add_config()
    bcs = builds.list_build_configurations(attributes="name")
    bc_names = [bc['name'] for bc in bcs]
    assert new_config['name'] in bc_names
    # todo: remove the newly added config

def test_list_build_configurations():
    build_configurations = builds.list_build_configurations()
    assert build_configurations is not None

def test_list_build_configurations_attribute():
    build_configurations = builds.list_build_configurations(attributes="name")
    assert build_configurations is not None

def test_build_trigger():
    randname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    builds.create_build_configuration(randname, 1, 1)
    builds.build(name=randname)
    # todo: assertion check that the new build is amongst running builds

def test_build_configuration_exists():
    randname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    created_bc = builds.create_build_configuration(randname, 1, 1)
    assert builds._build_configuration_exists(created_bc['id']) is True
    # todo: remove newly added build config

def test_get_build_configuration_id_by_name():
    created_bc = _add_config()
    assert builds._get_build_configuration_id_by_name(name=created_bc['name']) == created_bc['id']
    # todo: remove newly added config