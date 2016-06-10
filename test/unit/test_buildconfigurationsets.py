import argparse

import pytest

__author__ = 'Tom'
from test import testutils
from mock import MagicMock, patch, call
from pnc_cli import buildconfigurationsets
from pnc_cli.swagger_client import BuildConfigurationSetRest


def test_create_build_config_set_object(**kwargs):
    compare = BuildConfigurationSetRest()
    compare.name = 'testerino'
    compare.product_version_id = 1
    result = buildconfigurationsets._create_build_config_set_object(name='testerino', product_version_id=1)
    assert result.to_dict() == compare.to_dict()


@patch('pnc_cli.buildconfigurationsets.sets_api.get_all',
       return_value=testutils.create_mock_list_with_name_attribute())
def test_get_build_config_set_id_by_name(mock):
    result = buildconfigurationsets.get_build_config_set_id_by_name('testerino')
    mock.assert_called_once_with(q='name==testerino')
    assert result == 1


@patch('pnc_cli.buildconfigurationsets.sets_api.get_all',
       return_value=MagicMock(content=[]))
def test_get_build_config_set_id_by_name_notexist(mock):
    result = buildconfigurationsets.get_build_config_set_id_by_name('notexist')
    mock.assert_called_once_with(q='name==notexist')
    assert not result


@patch('pnc_cli.buildconfigurationsets.sets_api.get_all', return_value=MagicMock(content=[1, 2, 3]))
def test_list_build_configuration_sets(mock):
    result = buildconfigurationsets.list_build_configuration_sets()
    mock.assert_called_once_with(page_size=200, q="", sort="")
    assert result == [1, 2, 3]



@patch('pnc_cli.buildconfigurationsets._create_build_config_set_object', return_value='test-config-set')
@patch('pnc_cli.buildconfigurationsets.sets_api.create_new', return_value=MagicMock(content='SUCCESS'))
def test_create_build_configuration_set(mock_create_new, mock_create_object):
    result = buildconfigurationsets.create_build_configuration_set(name='newname', product_version_id=1,
                                                                   build_configuration_ids=[1, 2, 3])
    mock_create_object.assert_called_once_with(name='newname', product_version_id=1, build_configuration_ids=[1, 2, 3])
    mock_create_new.assert_called_once_with(body='test-config-set')
    assert result == 'SUCCESS'



@patch('pnc_cli.buildconfigurationsets.set_set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.get_specific', return_value=MagicMock(content='SUCCESS'))
def test_get_build_configuration_set_id(mock_get_specific, mock_set_set_id):
    result = buildconfigurationsets.get_build_configuration_set(id=1)
    mock_set_set_id.assert_called_once_with(1, None)
    mock_get_specific.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.buildconfigurationsets.set_set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.get_specific', return_value=MagicMock(content='SUCCESS'))
def test_get_build_configuration_set_name(mock_get_specific, mock_set_set_id):
    result = buildconfigurationsets.get_build_configuration_set(name='testerino')
    mock_set_set_id.assert_called_once_with(None, 'testerino')
    mock_get_specific.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.buildconfigurationsets.sets_api.get_specific')
@patch('pnc_cli.buildconfigurationsets.sets_api.update', return_value=MagicMock(content='SUCCESS'))
def test_update_build_configuration_set(mock_update, mock_get_specific):
    mock = MagicMock()
    mockcontent = MagicMock(content=mock)
    mock_get_specific.return_value = mockcontent
    result = buildconfigurationsets.update_build_configuration_set(1, product_version_id='updated')
    mock_get_specific.assert_called_once_with(id=1)
    mock_update.assert_called_once_with(id=1, body=mock)
    assert result == 'SUCCESS'


@patch('pnc_cli.buildconfigurationsets.set_set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.delete_specific', return_value=MagicMock(content='SUCCESS'))
def test_delete_build_config_set(mock_delete, mock_set_set_id):
    result = buildconfigurationsets.delete_build_configuration_set(id=1)
    mock_set_set_id.assert_called_once_with(1, None)
    mock_delete.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.buildconfigurationsets.set_set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.delete_specific', return_value=MagicMock(content='SUCCESS'))
def test_delete_build_config_set_name(mock_delete, mock_set_set_id):
    result = buildconfigurationsets.delete_build_configuration_set(name='testerino')
    mock_set_set_id.assert_called_once_with(None, 'testerino')
    mock_delete.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.buildconfigurationsets.sets_api.get_specific', return_value=MagicMock(content=[MagicMock(id=1)]))
def test_set_exists(mock_get_specific):
    result = buildconfigurationsets._set_exists(1)
    mock_get_specific.assert_called_once_with(id=1)
    assert result


def test_set_set_id():
    result = buildconfigurationsets.set_set_id(1, None)
    assert result == 1


@patch('pnc_cli.buildconfigurationsets.get_build_config_set_id_by_name', return_value=None)
def test_get_set_name(mock):
    result = buildconfigurationsets.set_set_id(None, 'testerino')
    mock.assert_called_once_with('testerino')
    assert not result


def test_set_set_none():
    with (pytest.raises(argparse.ArgumentTypeError)):
        result = buildconfigurationsets.set_set_id(None, None)


@patch('pnc_cli.buildconfigurationsets.set_set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.build', return_value=MagicMock(content='SUCCESS'))
def test_build_set_id(mock_build, mock_set_set_id):
    result = buildconfigurationsets.build_set(id=1)
    mock_set_set_id.assert_called_once_with(1, None)
    mock_build.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.buildconfigurationsets.set_set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.build', return_value=MagicMock(content='SUCCESS'))
def test_build_set_name(mock_build, mock_set_set_id):
    result = buildconfigurationsets.build_set(name='testerino')
    mock_set_set_id.assert_called_once_with(None, 'testerino')
    mock_build.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.buildconfigurationsets.set_set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.get_configurations', return_value=MagicMock(content='SUCCESS'))
def test_list_build_configurations_for_set_id(mock_get_configurations, mock_set_set_id):
    result = buildconfigurationsets.list_build_configurations_for_set(id=1)
    mock_set_set_id.assert_called_once_with(1, None)
    mock_get_configurations.assert_called_once_with(id=1, page_size=200, q="", sort="")
    assert result == 'SUCCESS'


@patch('pnc_cli.buildconfigurationsets.set_set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.get_configurations', return_value=MagicMock(content='SUCCESS'))
def test_list_build_configurations_for_set_name(mock_get_configurations, mock_set_set_id):
    result = buildconfigurationsets.list_build_configurations_for_set(name='testerino')
    mock_set_set_id.assert_called_once_with(None, 'testerino')
    mock_get_configurations.assert_called_once_with(id=1, page_size=200, q='', sort='')
    assert result == 'SUCCESS'


@patch('pnc_cli.buildconfigurationsets.set_set_id', return_value=1)
@patch('pnc_cli.buildconfigurations.get_build_configuration', return_value='BuildConfiguration')
@patch('pnc_cli.buildconfigurationsets.sets_api.add_configuration', return_value=MagicMock(content='SUCCESS'))
def test_add_build_configuration_to_set_id(mock_add_config, mock_get_build_configuration, mock_set_set_id):
    result = buildconfigurationsets.add_build_configuration_to_set(set_id=1, config_id=1)
    mock_set_set_id.assert_called_once_with(1, None)
    mock_get_build_configuration.assert_called_once_with(id=1, name=None)
    mock_add_config.assert_called_once_with(id=1, body='BuildConfiguration')
    assert result == 'SUCCESS'


@patch('pnc_cli.buildconfigurationsets.set_set_id', return_value=1)
@patch('pnc_cli.buildconfigurations.get_build_configuration', return_value='BuildConfiguration')
@patch('pnc_cli.buildconfigurationsets.sets_api.add_configuration', return_value=MagicMock(content='SUCCESS'))
def test_add_build_configuration_to_set_name(mock_add_config, mock_get_build_configuration, mock_set_set_id):
    result = buildconfigurationsets.add_build_configuration_to_set(set_name='testerino', config_id=1)
    mock_set_set_id.assert_called_once_with(None, 'testerino')
    mock_get_build_configuration.assert_called_once_with(id=1, name=None)
    mock_add_config.assert_called_once_with(id=1, body='BuildConfiguration')
    assert result == 'SUCCESS'


@patch('pnc_cli.buildconfigurationsets.set_set_id', return_value=1)
@patch('pnc_cli.buildconfigurations.set_bc_id', return_value=100)
@patch('pnc_cli.buildconfigurationsets.sets_api.remove_configuration', return_value=MagicMock(content="removed"))
def test_remove_build_configuration_from_set_id(mock_remove_configuration, mock_set_bc_id, mock_set_set_id):
    response = buildconfigurationsets.remove_build_configuration_from_set(set_id=1, config_id=100)
    mock_set_set_id.assert_called_once_with(1, None)
    mock_set_bc_id.assert_called_once_with(100, None)
    mock_remove_configuration.assert_called_once_with(id=1, config_id=100)
    assert response == "removed"


@patch('pnc_cli.buildconfigurationsets.set_set_id', return_value=1)
@patch('pnc_cli.buildconfigurations.set_bc_id', return_value=100)
@patch('pnc_cli.buildconfigurationsets.sets_api.remove_configuration', return_value=MagicMock(content="removed"))
def test_remove_build_configuration_from_set_name(mock_remove_configuration, mock_set_bc_id, mock_set_set_id):
    response = buildconfigurationsets.remove_build_configuration_from_set(set_name='test', config_name='test_conf')
    mock_set_set_id.assert_called_once_with(None, 'test')
    mock_set_bc_id.assert_called_once_with(None, 'test_conf')
    mock_remove_configuration.assert_called_once_with(id=1, config_id=100)
    assert response == "removed"


@patch('pnc_cli.buildconfigurationsets.set_set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.get_build_records', return_value=MagicMock(content='SUCCESS'))
def test_list_build_records_for_set_id(mock_get_records, mock_set_set_id):
    result = buildconfigurationsets.list_build_records_for_set(id=1)
    mock_set_set_id.assert_called_once_with(1, None)
    mock_get_records.assert_called_once_with(id=1, page_size=200, q="", sort="")
    assert result == 'SUCCESS'


@patch('pnc_cli.buildconfigurationsets.set_set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.get_build_records', return_value=MagicMock(content='SUCCESS'))
def test_list_build_records_for_set_name(mock_get_records, mock_set_set_id):
    result = buildconfigurationsets.list_build_records_for_set(name='testerino')
    mock_set_set_id.assert_called_once_with(None, 'testerino')
    mock_get_records.assert_called_once_with(id=1, page_size=200, q='', sort='')
    assert result == 'SUCCESS'