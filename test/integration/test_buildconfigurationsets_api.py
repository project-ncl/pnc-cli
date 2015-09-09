import random
import string
import pytest


__author__ = 'thauser'

from pnc import buildconfigurationsets
from test.integration import test_buildconfigurations_api
from pnc import buildconfigurations
from pnc import utils
from pnc.swagger_client.apis.buildconfigurationsets_api import BuildconfigurationsetsApi
from pnc.swagger_client.apis.buildconfigurations_api import BuildconfigurationsApi

sets_api = BuildconfigurationsetsApi(utils.get_api_client())
configs_api = BuildconfigurationsApi(utils.get_api_client())

def create_set():
    randname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    return sets_api.create_new(body=buildconfigurationsets._create_build_config_set_object(name=randname, productVersionId=1)).content

def test_get_all():
    sets = sets_api.get_all().content
    assert sets is not None

def test_create():
    new_set = create_set()
    set_names = [set.name for set in sets_api.get_all().content]
    assert new_set.name in set_names

def test_get_specific():
    new_set = create_set()
    set = sets_api.get_specific(id=new_set.id)
    assert set is not None

def test_update():
    new_set = create_set()
    newname = "newname" +''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    updated_set = buildconfigurationsets._create_build_config_set_object(name=newname)
    sets_api.update(id=new_set.id, body=updated_set)
    retrieved_set = sets_api.get_specific(id=new_set.id).content
    assert retrieved_set.name == newname

@pytest.mark.xfail(reason='delete is only possible for sets which do not have any buildrecords')
def test_delete():
    pass

@pytest.mark.xfail(reason="doesn't reliably return valid json.")
def test_trigger():
    new_set = create_set()
    running_set = sets_api.trigger(id=new_set.id)
    assert running_set.ok

def test_get_configurations():
    new_config_obj = buildconfigurations.create_build_conf_object(name=utils.gen_random_name(), project_id="1", environment_id="1", build_status="SUCCESS")
    new_config = configs_api.create_new(body=new_config_obj).content
    new_set = create_set()

    sets_api.add_configuration(id=new_set.id,body=new_config)
    set_configs = sets_api.get_configurations(id=new_set.id)
    assert set_configs is not None

def test_add_configuration():
    new_set = create_set()
    new_config = test_buildconfigurations_api.create_config()
    sets_api.add_configuration(id=new_set.id, body=new_config)
    set_config_ids = [x.id for x in sets_api.get_configurations(id=new_set.id).content]
    assert new_config.id in set_config_ids

def test_get_build_records():
    pass








