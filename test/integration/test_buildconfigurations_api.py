from pnc import buildconfigurations
from pnc.swagger_client.apis.buildconfigurations_api import BuildconfigurationsApi
from pnc import utils

configs_api = BuildconfigurationsApi(utils.get_api_client())

def create_config():
    return configs_api.create_new(body=buildconfigurations.create_build_conf_object(name=utils.gen_random_name(), project_id=1, environment_id=1, build_status="UNKNOWN")).content

def test_get_all():
    build_configurations = configs_api.get_all().content
    assert build_configurations is not None

def test_create_build_configuration():
    new_config = create_config()
    bc_names = [bc.name for bc in configs_api.get_all().content]
    assert new_config.name in bc_names

def test_build_trigger():
    new_config = create_config()
    running_build = configs_api.trigger(id=new_config.id).content
    assert running_build.status == "BUILDING"

def test_get_build_configuration_id_by_name():
    created_bc = create_config()
    find_by_name = buildconfigurations.get_build_configuration_id_by_name(name=created_bc.name)
    assert configs_api.get_specific(id=find_by_name).content.id == configs_api.get_specific(id=created_bc.id).content.id
