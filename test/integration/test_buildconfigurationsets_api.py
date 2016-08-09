import pytest

from test.integration.conftest import new_config

__author__ = 'thauser'

from pnc_cli import buildconfigurationsets
from pnc_cli import utils
from test import testutils
from pnc_cli.swagger_client.apis.buildconfigurationsets_api import BuildconfigurationsetsApi


@pytest.fixture(scope='function', autouse=True)
def get_sets_api():
    global sets_api
    sets_api = BuildconfigurationsetsApi(utils.get_api_client())


def test_get_all_invalid_param():
    testutils.assert_raises_typeerror(sets_api, 'get_all')


def test_get_all():
    sets = sets_api.get_all().content
    assert sets is not None


def test_create_new_invalid_param():
    testutils.assert_raises_typeerror(sets_api, 'create_new')


def test_create_new(new_set):
    assert sets_api.get_specific(id=new_set.id).content is not None


def test_get_specific_no_id():
    testutils.assert_raises_valueerror(sets_api, 'get_specific', id=None)


def test_get_specific_invalid_param():
    testutils.assert_raises_typeerror(sets_api, 'get_specific', id=1)


def test_get_specific(new_set):
    set = sets_api.get_specific(id=new_set.id)
    assert set is not None


def test_update_no_id():
    testutils.assert_raises_valueerror(sets_api, 'update', id=None)


def test_update_invalid_param():
    testutils.assert_raises_typeerror(sets_api, 'update', id=1)


def test_update(new_set):
    newname = "newname" + testutils.gen_random_name()
    updated_set = buildconfigurationsets._create_build_config_set_object(name=newname)
    sets_api.update(id=new_set.id, body=updated_set)
    retrieved_set = sets_api.get_specific(id=new_set.id).content
    assert retrieved_set.name == newname


def test_delete_no_id():
    testutils.assert_raises_valueerror(sets_api, 'delete_specific', id=None)


def test_delete_invalid_param():
    testutils.assert_raises_typeerror(sets_api, 'delete_specific', id=1)


def test_delete(new_set):
    sets_api.delete_specific(id=new_set.id)
    response = utils.checked_api_call(sets_api, 'get_specific', id=new_set.id)
    assert response is None


def test_get_configurations_no_id():
    testutils.assert_raises_valueerror(sets_api, 'get_configurations', id=None)


def test_get_configurations_invalid_param():
    testutils.assert_raises_typeerror(sets_api, 'get_configurations', id=1)


def test_get_configurations(new_config, new_set):
    sets_api.add_configuration(id=new_set.id, body=new_config)
    set_configs = sets_api.get_configurations(id=new_set.id)
    assert set_configs is not None


def test_add_configuration_no_set_id(new_config, new_set):
    testutils.assert_raises_valueerror(sets_api, 'remove_configuration', id=None, config_id=1)


def test_add_configuration_no_config_id(new_config, new_set):
    testutils.assert_raises_valueerror(sets_api, 'remove_configuration', id=1, config_id=None)


def test_add_configuration_invalid_param():
    testutils.assert_raises_typeerror(sets_api, 'remove_configuration', id=1, config_id=1)


def test_add_configuration(new_config, new_set):
    sets_api.add_configuration(id=new_set.id, body=new_config)
    set_config_ids = [x.id for x in sets_api.get_configurations(id=new_set.id).content]
    assert new_config.id in set_config_ids


def test_remove_configuration_no_set_id():
    testutils.assert_raises_valueerror(sets_api, 'remove_configuration', id=None, config_id=1)


def test_remove_configuration_no_config_id():
    testutils.assert_raises_valueerror(sets_api, 'remove_configuration', id=1, config_id=None)


def test_remove_configuration_invalid_param():
    testutils.assert_raises_typeerror(sets_api, 'remove_configuration', id=1, config_id=1)


def test_remove_configuration(new_config, new_set):
    sets_api.add_configuration(id=new_set.id, body=new_config)
    set_config_ids = [x.id for x in sets_api.get_configurations(id=new_set.id).content]
    # config is added successfully
    assert new_config.id in set_config_ids
    # remove config
    sets_api.remove_configuration(id=new_set.id, config_id=new_config.id)
    # removed successfully
    assert sets_api.get_configurations(id=new_set.id).content is None


def test_get_build_records_no_id():
    testutils.assert_raises_valueerror(sets_api, 'get_build_records', id=None)


def test_get_build_records_invalid_param():
    testutils.assert_raises_typeerror(sets_api, 'get_build_records', id=1)


def test_get_build_records(new_set):
    response = sets_api.get_build_records(id=new_set.id)
    assert response


def test_build_no_id():
    testutils.assert_raises_valueerror(sets_api, 'build', id=None)


def test_build_invalid_param():
    testutils.assert_raises_typeerror(sets_api, 'build', id=1)


def test_build(request, new_set, new_project, new_environment):
    config_one = new_config(request, new_project, new_environment)
    config_two = new_config(request, new_project, new_environment)
    config_three = new_config(request, new_project, new_environment)
    sets_api.add_configuration(id=new_set.id, body=config_one)
    sets_api.add_configuration(id=new_set.id, body=config_two)
    sets_api.add_configuration(id=new_set.id, body=config_three)
    build_records = sets_api.build(id=new_set.id, rebuild_all=False)
    assert build_records is not None


def test_get_all_build_config_set_records_no_id():
    testutils.assert_raises_valueerror(sets_api, 'get_all_build_config_set_records', id=None)


def test_get_all_build_config_set_records_invalid_param():
    testutils.assert_raises_typeerror(sets_api, 'get_all_build_config_set_records', id=1)


def test_get_all_build_config_set_records(new_set):
    response = sets_api.get_all_build_config_set_records(id=new_set.id)
    assert response is not None
