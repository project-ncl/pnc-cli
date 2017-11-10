import argparse

import pytest

__author__ = 'Tom'
from test import testutils
from mock import MagicMock, patch, call
from pnc_cli import buildconfigurationsets
from pnc_cli.swagger_client import BuildconfigurationsetsApi
from pnc_cli.swagger_client import BuildConfigurationSetRest
from pnc_cli.swagger_client import BuildconfigurationsApi


def test_create_build_config_set_object(**kwargs):
    compare = BuildConfigurationSetRest()
    compare.name = 'testerino'
    compare.product_version_id = 1
    result = buildconfigurationsets._create_build_config_set_object(name='testerino', product_version_id=1)
    assert result.to_dict() == compare.to_dict()


@patch('pnc_cli.buildconfigurationsets.sets_api.get_all', return_value=MagicMock(content=[1, 2, 3]))
def test_list_build_configuration_sets(mock):
    result = buildconfigurationsets.list_build_configuration_sets_raw()
    mock.assert_called_once_with(page_size=200, q="", sort="")
    assert result == [1, 2, 3]


@patch('pnc_cli.buildconfigurationsets._create_build_config_set_object', return_value='test-config-set')
@patch('pnc_cli.buildconfigurationsets.sets_api.create_new', return_value=MagicMock(content='SUCCESS'))
def test_create_build_configuration_set(mock_create_new, mock_create_object):
    result = buildconfigurationsets.create_build_configuration_set_raw(name='newname', product_version_id=1,
                                                                   build_configuration_ids=[1, 2, 3])
    mock_create_object.assert_called_once_with(name='newname', product_version_id=1, build_configuration_ids=[1, 2, 3])
    mock_create_new.assert_called_once_with(body='test-config-set')
    assert result == 'SUCCESS'



@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.get_specific', return_value=MagicMock(content='SUCCESS'))
@patch('pnc_cli.buildconfigurationsets.sets_api', autospec=BuildconfigurationsetsApi)
def test_get_build_configuration_set_id(mock_sets_api, mock_get_specific, mock_set_id):
    result = buildconfigurationsets.get_build_configuration_set_raw(id=1)
    mock_set_id.assert_called_once_with(mock_sets_api, 1, None)
    mock_get_specific.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.get_specific', return_value=MagicMock(content='SUCCESS'))
@patch('pnc_cli.buildconfigurationsets.sets_api', autospec=BuildconfigurationsetsApi)
def test_get_build_configuration_set_name(mock_sets_api, mock_get_specific, mock_set_id):
    result = buildconfigurationsets.get_build_configuration_set_raw(name='testerino')
    mock_set_id.assert_called_once_with(mock_sets_api, None, 'testerino')
    mock_get_specific.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.buildconfigurationsets.sets_api.get_specific')
@patch('pnc_cli.buildconfigurationsets.sets_api.update', return_value=MagicMock(content='SUCCESS'))
def test_update_build_configuration_set(mock_update, mock_get_specific):
    mock = MagicMock()
    mockcontent = MagicMock(content=mock)
    mock_get_specific.return_value = mockcontent
    result = buildconfigurationsets.update_build_configuration_set_raw(1, product_version_id='updated')
    mock_get_specific.assert_called_once_with(id=1)
    mock_update.assert_called_once_with(id=1, body=mock)
    assert result == 'SUCCESS'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.delete_specific', return_value=MagicMock(content='SUCCESS'))
@patch('pnc_cli.buildconfigurationsets.sets_api', autospec=BuildconfigurationsetsApi)
def test_delete_build_config_set(mock_sets_api, mock_delete, mock_set_id):
    result = buildconfigurationsets.delete_build_configuration_set_raw(id=1)
    mock_set_id.assert_called_once_with(mock_sets_api, 1, None)
    mock_delete.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.delete_specific', return_value=MagicMock(content='SUCCESS'))
@patch('pnc_cli.buildconfigurationsets.sets_api', autospec=BuildconfigurationsetsApi)
def test_delete_build_config_set_name(mock_sets_api, mock_delete, mock_set_id):
    result = buildconfigurationsets.delete_build_configuration_set_raw(name='testerino')
    mock_set_id.assert_called_once_with(mock_sets_api, None, 'testerino')
    mock_delete.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.build', return_value=MagicMock(content='SUCCESS'))
@patch('pnc_cli.buildconfigurationsets.sets_api', autospec=BuildconfigurationsetsApi)
def test_build_set_id(mock_sets_api, mock_build, mock_set_id):
    result = buildconfigurationsets.build_set_raw(id=1)
    mock_set_id.assert_called_once_with(mock_sets_api, 1, None)
    mock_build.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.build', return_value=MagicMock(content='SUCCESS'))
@patch('pnc_cli.buildconfigurationsets.sets_api', autospec=BuildconfigurationsetsApi)
def test_build_set_name(mock_sets_api, mock_build, mock_set_id):
    result = buildconfigurationsets.build_set_raw(name='testerino')
    mock_set_id.assert_called_once_with(mock_sets_api, None, 'testerino')
    mock_build.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.get_configurations', return_value=MagicMock(content='SUCCESS'))
@patch('pnc_cli.buildconfigurationsets.sets_api', autospec=BuildconfigurationsetsApi)
def test_list_build_configurations_for_set_id(mock_sets_api, mock_get_configurations, mock_set_id):
    result = buildconfigurationsets.list_build_configurations_for_set_raw(id=1)
    mock_set_id.assert_called_once_with(mock_sets_api, 1, None)
    mock_get_configurations.assert_called_once_with(id=1, page_size=200, q="", sort="")
    assert result == 'SUCCESS'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.get_configurations', return_value=MagicMock(content='SUCCESS'))
@patch('pnc_cli.buildconfigurationsets.sets_api', autospec=BuildconfigurationsetsApi)
def test_list_build_configurations_for_set_name(mock_sets_api, mock_get_configurations, mock_set_id):
    result = buildconfigurationsets.list_build_configurations_for_set_raw(name='testerino')
    mock_set_id.assert_called_once_with(mock_sets_api, None, 'testerino')
    mock_get_configurations.assert_called_once_with(id=1, page_size=200, q='', sort='')
    assert result == 'SUCCESS'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.common.get_entity', return_value='BuildConfiguration')
@patch('pnc_cli.buildconfigurationsets.sets_api.add_configuration', return_value=MagicMock(content='SUCCESS'))
@patch('pnc_cli.buildconfigurationsets.sets_api', autospec=BuildconfigurationsetsApi)
@patch('pnc_cli.buildconfigurationsets.configs_api', autospec=BuildconfigurationsApi)
def test_add_build_configuration_to_set_id(mock_configs_api, mock_sets_api, mock_add_config, mock_get_entity, mock_set_id):
    result = buildconfigurationsets.add_build_configuration_to_set_raw(set_id=1, config_id=1)
    set_id_calls = [call(mock_sets_api, 1, None), call(mock_configs_api, 1, None)]
    mock_set_id.assert_has_calls(set_id_calls)
    mock_get_entity.assert_called_once_with(mock_configs_api,  1)
    mock_add_config.assert_called_once_with(id=1, body='BuildConfiguration')
    assert result == 'SUCCESS'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.common.get_entity', return_value='BuildConfiguration')
@patch('pnc_cli.buildconfigurationsets.sets_api.add_configuration', return_value=MagicMock(content='SUCCESS'))
@patch('pnc_cli.buildconfigurationsets.sets_api', autospec=BuildconfigurationsetsApi)
@patch('pnc_cli.buildconfigurationsets.configs_api', autospec=BuildconfigurationsApi)
def test_add_build_configuration_to_set_name(mock_configs_api, mock_sets_api, mock_add_config, mock_get_entity, mock_set_id):
    result = buildconfigurationsets.add_build_configuration_to_set_raw(set_name='testerino', config_id=1)
    set_id_calls = [call(mock_sets_api, None, 'testerino'), call(mock_configs_api, 1, None)]
    mock_set_id.assert_has_calls(set_id_calls)
    mock_get_entity.assert_called_once_with(mock_configs_api, 1)
    mock_add_config.assert_called_once_with(id=1, body='BuildConfiguration')
    assert result == 'SUCCESS'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.remove_configuration', return_value=MagicMock(content="removed"))
@patch('pnc_cli.buildconfigurationsets.sets_api', autospec=BuildconfigurationsetsApi)
@patch('pnc_cli.buildconfigurationsets.configs_api', autospec=BuildconfigurationsApi)
def test_remove_build_configuration_from_set_id(mock_configs_api, mock_sets_api, mock_remove_configuration, mock_set_id):
    response = buildconfigurationsets.remove_build_configuration_from_set_raw(set_id=1, config_id=100)
    set_id_calls = [call(mock_sets_api, 1, None), call(mock_configs_api, 100, None)]
    mock_set_id.assert_has_calls(set_id_calls)
    mock_remove_configuration.assert_called_once_with(id=1, config_id=1)
    assert response == "removed"


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.remove_configuration', return_value=MagicMock(content="removed"))
@patch('pnc_cli.buildconfigurationsets.sets_api', autospec=BuildconfigurationsetsApi)
@patch('pnc_cli.buildconfigurationsets.configs_api', autospec=BuildconfigurationsApi)
def test_remove_build_configuration_from_set_name(mock_configs_api, mock_sets_api, mock_remove_configuration, mock_set_id):
    response = buildconfigurationsets.remove_build_configuration_from_set_raw(set_name='test', config_name='test_conf')
    set_id_calls = [call(mock_sets_api, None, 'test'), call(mock_configs_api, None, 'test_conf')]
    mock_set_id.assert_has_calls(set_id_calls)
    mock_remove_configuration.assert_called_once_with(id=1, config_id=1)
    assert response == "removed"


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.get_build_records', return_value=MagicMock(content='SUCCESS'))
@patch('pnc_cli.buildconfigurationsets.sets_api', autospec=BuildconfigurationsetsApi)
def test_list_build_records_for_set_id(mock_sets_api, mock_get_records, mock_set_id):
    result = buildconfigurationsets.list_build_records_for_set_raw(id=1)
    mock_set_id.assert_called_once_with(mock_sets_api, 1, None)
    mock_get_records.assert_called_once_with(id=1, page_size=200, q="", sort="")
    assert result == 'SUCCESS'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.get_build_records', return_value=MagicMock(content='SUCCESS'))
@patch('pnc_cli.buildconfigurationsets.sets_api', autospec=BuildconfigurationsetsApi)
def test_list_build_records_for_set_name(mock_sets_api, mock_get_records, mock_set_id):
    result = buildconfigurationsets.list_build_records_for_set_raw(name='testerino')
    mock_set_id.assert_called_once_with(mock_sets_api, None, 'testerino')
    mock_get_records.assert_called_once_with(id=1, page_size=200, q='', sort='')
    assert result == 'SUCCESS'
