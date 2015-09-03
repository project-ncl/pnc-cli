import random
import string
import pytest


__author__ = 'thauser'

from pnc import buildconfigurationsets
from test.integration import test_buildconfigurations_api
from pnc import buildconfigurations

def create_set():
    randname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    return buildconfigurationsets.create(buildconfigurationsets._create_build_config_set_object(name=randname, productVersionId=1)).json()

def test_get_all():
    sets = buildconfigurationsets.get_all().json()
    assert sets is not None

def test_create():
    new_set = create_set()
    sets = buildconfigurationsets.get_all().json()
    set_names = [set['name'] for set in sets]
    assert new_set['name'] in set_names

def test_get_specific():
    new_set = create_set()
    set = buildconfigurationsets.get_specific(new_set['id'])
    assert set is not None

def test_update():
    new_set = create_set()
    updated_set = buildconfigurationsets._create_build_config_set_object(name="updated set name")
    buildconfigurationsets.update(new_set['id'], updated_set)
    retrieved_set = buildconfigurationsets.get_specific(new_set['id']).json()
    assert retrieved_set['name'] == 'updated set name'

@pytest.mark.xfail(reason='delete is only possible for sets which do not have any buildrecords')
def test_delete():
    pass

@pytest.mark.xfail(reason="doesn't reliably return valid json.")
def test_trigger():
    new_set = create_set()
    running_set = buildconfigurationsets.trigger(new_set['id'])
    assert running_set.ok

def test_get_configurations():
    new_config = buildconfigurations.create_build_conf_object(name="new build config")
    new_set = create_set()
    buildconfigurationsets.add_configuration(new_set['id'],new_config)
    set_configs = buildconfigurationsets.get_configurations(new_set['id']).json()
    assert set_configs is not None

def test_add_configuration():
    new_set = create_set()
    new_config = test_buildconfigurations_api.create_config()
    config_object = buildconfigurations.create_build_conf_object(**new_config)
    buildconfigurationsets.add_configuration(new_set['id'], config_object)
    set_configs = buildconfigurationsets.get_configurations(new_set['id']).json()
    assert new_config in set_configs

def test_get_build_records():
    pass








