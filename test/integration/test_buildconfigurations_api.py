import random
import string
from pnc import buildconfigurations
from pnc.swagger_client.apis.buildconfigurations_api import BuildconfigurationsApi
from pnc import utils

builds_api = BuildconfigurationsApi(utils.get_api_client())

def create_config():
    randname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    return builds_api.create_new(body=buildconfigurations.create_build_conf_object(name=randname, project_id=1, environment_id=1))

def test_get_all():
    build_configurations = builds_api.get_all()
    assert build_configurations is not None

def test_create_build_configuration():
    new_config = create_config()
    bcs = builds_api.get_all()
    bc_names = [bc.name for bc in bcs]
    assert new_config.name in bc_names

def test_build_trigger():
    new_config = create_config()
    running_build = builds_api.trigger(id=new_config.id)
    assert running_build.ok

def test_get_build_configuration_id_by_name():
    created_bc = create_config()
    assert builds_api.get_specific(id=buildconfigurations.get_build_configuration_id_by_name(name=created_bc.name)).id \
           == builds_api.get_specific(id=created_bc.id)
