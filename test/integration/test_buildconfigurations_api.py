from pnc_cli import buildconfigurations
from pnc_cli.swagger_client.apis.buildconfigurations_api import BuildconfigurationsApi
from pnc_cli import utils
from test import testutils
from test.integration import test_productversions_api

configs_api = BuildconfigurationsApi(utils.get_api_client())


def create_config():
    return configs_api.create_new(
        body=buildconfigurations.create_build_conf_object(name=testutils.gen_random_name(), project_id=1, environment_id=1,
                                                          build_status="UNKNOWN")).content


def test_get_all():
    build_configurations = configs_api.get_all().content
    assert build_configurations is not None


def test_create_build_configuration():
    new_config = create_config()
    bc_names = [bc.name for bc in configs_api.get_all().content]
    assert new_config.name in bc_names


def test_build():
    new_config = create_config()
    configs_api.trigger(id=new_config.id)
    running_build = configs_api.get_specific(id=new_config.id).content
    assert running_build.build_status == "BUILDING"


def test_get_build_configuration_id_by_name():
    created_bc = create_config()
    find_by_name = buildconfigurations.get_build_configuration_id_by_name(name=created_bc.name)
    assert configs_api.get_specific(id=find_by_name).content.id == configs_api.get_specific(id=created_bc.id).content.id

def test_get_all_by_product_id():
    #need to add bcs to some product
    response = configs_api.get_all_by_product_id(product_id=1).content
    assert response is not None

def test_get_all_by_product_version_id():
    #need to add bcs to some product version
    response = configs_api.get_all_by_product_version_id(product_id=1, version_id=1).content
    assert response is not None

def test_get_all_by_project_id():
    response = configs_api.get_all_by_project_id(project_id=1).content
    assert response is not None

def test_update():
    created_bc = create_config()
    created_bc.description = "This is a new description for testing update functionality"
    created_bc.name = "pnc-cli-test-updated-"+created_bc.name
    configs_api.update(id=created_bc.id, body=created_bc)
    updated = configs_api.get_specific(id=created_bc.id).content
    assert updated.to_dict() == created_bc.to_dict()

def test_delete_specific():
    created_bc = create_config()
    existing_ids = [bc.id for bc in configs_api.get_all().content]
    assert created_bc.id in existing_ids
    configs_api.delete_specific(id=created_bc.id)
    existing_ids = [bc.id for bc in configs_api.get_all().content]
    assert created_bc not in existing_ids

def test_get_build_records():
    response = configs_api.get_build_records(id=1).content
    assert response is not None

def test_get_latest_build_record():
    response = configs_api.get_latest_build_record(id=1).content
    assert response is not None

def test_clone():
    created_bc = create_config()
    cloned_bc = configs_api.clone(id=created_bc.id).content
    assert created_bc.to_dict() == cloned_bc.to_dict()

# add_dependency
# get_dependencies
# remove_dependency
def test_dependency_operations():
    created_bc = create_config()
    created_dep = create_config()
    configs_api.add_dependency(id=created_dep.id, body=created_bc)
    dependency_ids = [dep.id for dep in configs_api.get_dependencies(id=created_bc).content]
    assert created_dep.id in dependency_ids
    configs_api.remove_dependency(id=created_bc.id, dependency_id=created_dep.id)
    dependency_ids = [dep.id for dep in configs_api.get_dependencies(id=created_bc).content]
    assert created_dep.id not in dependency_ids

def test_get_product_versions():
    response = configs_api.get_product_versions(id=1)
    assert response is not None

# add_product_version
# get_product_versions
# remove_product_version
#TODO: cannot test due to test_productversions_api incomplete
def test_product_version_operations():
    created_bc = create_config()
    test_productversions_api.create_product_version()










