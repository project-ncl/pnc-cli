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
    mock.assert_called_once_with()
    assert result == 1


@patch('pnc_cli.buildconfigurationsets.sets_api.get_all',
       return_value=testutils.create_mock_list_with_name_attribute())
def test_get_build_config_set_id_by_name_notexist(mock):
    result = buildconfigurationsets.get_build_config_set_id_by_name('notexist')
    mock.assert_called_once_with()
    assert not result


@patch('pnc_cli.buildconfigurationsets.sets_api.get_all', return_value=MagicMock(content=[1, 2, 3]))
def test_list_build_configuration_sets(mock):
    result = buildconfigurationsets.list_build_configuration_sets()
    mock.assert_called_once_with(page_size=200, q="", sort="")
    assert result == [1, 2, 3]


@patch('pnc_cli.buildconfigurationsets.get_build_config_set_id_by_name', return_value=None)
@patch('pnc_cli.productversions.version_exists', return_vale=True)
@patch('pnc_cli.buildconfigurations.config_id_exists', return_value=True)
@patch('pnc_cli.buildconfigurationsets._create_build_config_set_object', return_value='test-config-set')
@patch('pnc_cli.buildconfigurationsets.sets_api.create_new', return_value=MagicMock(content='SUCCESS'))
def test_create_build_configuration_set(mock_create_new, mock_create_object, mock_config_id_exists, mock_version_exists,
                                        mock_get_set_by_name):
    result = buildconfigurationsets.create_build_configuration_set(name='newname', product_version_id=1,
                                                                   build_configuration_ids=[1, 2, 3])
    mock_get_set_by_name.assert_called_once_with('newname')
    mock_version_exists.assert_called_once_with(1)
    mock_config_id_exists.assert_has_calls([call(1), call(2), call(3)])
    mock_create_object.assert_called_once_with(name='newname', product_version_id=1, build_configuration_ids=[1, 2, 3])
    mock_create_new.assert_called_once_with(body='test-config-set')
    assert result == 'SUCCESS'


@patch('pnc_cli.buildconfigurationsets.get_build_config_set_id_by_name', return_value='existing')
@patch('pnc_cli.productversions.version_exists', return_vale=True)
@patch('pnc_cli.buildconfigurations.config_id_exists', return_value=True)
@patch('pnc_cli.buildconfigurationsets._create_build_config_set_object', return_value='test-config-set')
@patch('pnc_cli.buildconfigurationsets.sets_api.create_new', return_value=MagicMock(content='SUCCESS'))
def test_create_build_configuration_set_setexists(mock_create_new, mock_create_object, mock_config_id_exists,
                                                  mock_version_exists, mock_get_set_by_name):
    result = buildconfigurationsets.create_build_configuration_set(name='newname', product_version_id=1,
                                                                   build_configuration_ids=[1, 2, 3])
    mock_get_set_by_name.assert_called_once_with('newname')
    assert not mock_version_exists.called
    assert not mock_config_id_exists.called
    assert not mock_create_object.called
    assert not mock_create_new.called
    assert not result


@patch('pnc_cli.buildconfigurationsets.get_build_config_set_id_by_name', return_value=None)
@patch('pnc_cli.productversions.version_exists', return_value=False)
@patch('pnc_cli.buildconfigurations.config_id_exists')
@patch('pnc_cli.buildconfigurationsets._create_build_config_set_object')
@patch('pnc_cli.buildconfigurationsets.sets_api.create_new')
def test_create_build_configuration_set_versionnotexists(mock_create_new, mock_create_object, mock_config_id_exists,
                                                         mock_version_exists, mock_get_set_by_name):
    result = buildconfigurationsets.create_build_configuration_set(name='newname', product_version_id=1,
                                                                   build_configuration_ids=[1, 2, 3])
    mock_get_set_by_name.assert_called_once_with('newname')
    mock_version_exists.assert_called_once_with(1)
    assert not mock_config_id_exists.called
    assert not mock_create_object.called
    assert not mock_create_new.called
    assert not result

@patch('pnc_cli.buildconfigurationsets.get_build_config_set_id_by_name', return_value=None)
@patch('pnc_cli.productversions.version_exists', return_vale=True)
@patch('pnc_cli.buildconfigurations.config_id_exists', return_value=False)
@patch('pnc_cli.buildconfigurationsets._create_build_config_set_object')
@patch('pnc_cli.buildconfigurationsets.sets_api.create_new')
def test_create_build_configuration_set_confignotexists(mock_create_new, mock_create_object, mock_config_id_exists,
                                                         mock_version_exists, mock_get_set_by_name):
    result = buildconfigurationsets.create_build_configuration_set(name='newname', product_version_id=1,
                                                                   build_configuration_ids=[1, 2, 3])
    mock_get_set_by_name.assert_called_once_with('newname')
    mock_version_exists.assert_called_once_with(1)
    mock_config_id_exists.assert_has_calls([call(1), call(2), call(3)])
    assert not mock_create_object.called
    assert not mock_create_new.called
    assert not result


@patch('pnc_cli.buildconfigurationsets.get_set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.get_specific', return_value=MagicMock(content='SUCCESS'))
def test_get_build_configuration_set_id(mock_get_specific, mock_get_set_id):
    result = buildconfigurationsets.get_build_configuration_set(id=1)
    mock_get_set_id.assert_called_once_with(1, None)
    mock_get_specific.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.buildconfigurationsets.get_set_id', return_value=None)
@patch('pnc_cli.buildconfigurationsets.sets_api.get_specific')
def test_get_build_configuration_set_id_notexist(mock_get_specific, mock_get_set_id):
    result = buildconfigurationsets.get_build_configuration_set(id=1)
    mock_get_set_id.assert_called_once_with(1, None)
    assert not mock_get_specific.called
    assert not result


@patch('pnc_cli.buildconfigurationsets.get_set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.get_specific', return_value=MagicMock(content='SUCCESS'))
def test_get_build_configuration_set_name(mock_get_specific, mock_get_set_id):
    result = buildconfigurationsets.get_build_configuration_set(name='testerino')
    mock_get_set_id.assert_called_once_with(None, 'testerino')
    mock_get_specific.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.buildconfigurationsets.get_set_id', return_value=None)
@patch('pnc_cli.buildconfigurationsets.sets_api.get_specific')
def test_get_build_configuration_set_name_notexist(mock_get_specific, mock_get_set_id):
    result = buildconfigurationsets.get_build_configuration_set(name='testerino')
    mock_get_set_id.assert_called_once_with(None, 'testerino')
    assert not mock_get_specific.called
    assert not result


@patch('pnc_cli.buildconfigurationsets.sets_api.get_specific')
@patch('pnc_cli.productversions.get_product_version', return_value=True)
@patch('pnc_cli.buildconfigurationsets.get_set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.update', return_value=MagicMock(content='SUCCESS'))
def test_update_build_configuration_set(mock_update, mock_get_set_id, mock_get_product_version, mock_get_specific):
    mock = MagicMock()
    mockcontent = MagicMock(content=mock)
    mock_get_specific.return_value=mockcontent
    result = buildconfigurationsets.update_build_configuration_set(1, product_version_id='updated')
    mock_get_specific.assert_called_once_with(id=1)
    mock_get_product_version.assert_called_once_with(id='updated')
    mock_get_set_id.assert_called_once_with(1, None)
    mock_update.assert_called_once_with(id=1, body=mock)
    assert result == 'SUCCESS'


@patch('pnc_cli.buildconfigurationsets.get_set_id', return_value=None)
@patch('pnc_cli.buildconfigurationsets.sets_api.update')
def test_update_build_configuration_set_notexist(mock_update, mock_get_set_id):
    result = buildconfigurationsets.update_build_configuration_set(1, product_version_id='herpaderpa')
    mock_get_set_id.assert_called_once_with(1, None)
    assert not mock_update.called
    assert not result


@patch('pnc_cli.buildconfigurationsets.get_set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.get_specific')
@patch('pnc_cli.buildconfigurationsets.productversions.get_product_version', return_value=None)
@patch('pnc_cli.buildconfigurationsets.sets_api.update')
def test_update_build_configuration_set_invalid_project_version_id(mock_update, mock_get_product_version, mock_get_specific, mock_get_set_id):
    mock = MagicMock()
    mockcontent = MagicMock(content=mock)
    mock_get_specific.return_value=mockcontent
    result = buildconfigurationsets.update_build_configuration_set(1, product_version_id='notexist')
    mock_get_set_id.assert_called_once_with(1, None)
    mock_get_specific.assert_called_once_with(id=1)
    mock_get_product_version.assert_called_once_with(id='notexist')
    assert not mock_update.called
    assert not result


@patch('pnc_cli.buildconfigurationsets.get_set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.get_specific')
@patch('pnc_cli.buildconfigurationsets.buildconfigurations.get_build_configuration', return_value=None)
@patch('pnc_cli.buildconfigurationsets.sets_api.update')
def test_update_build_configuration_set_invalid_build_configuration_id(mock_update,mock_get_build_configuration, mock_get_specific, mock_get_set_id):
    mock = MagicMock()
    mockcontent = MagicMock(content=mock)
    mock_get_specific.return_value=mockcontent
    result = buildconfigurationsets.update_build_configuration_set(1, build_configuration_ids=[1,2,3])
    mock_get_set_id.assert_called_once_with(1, None)
    mock_get_specific.assert_called_once_with(id=1)
    mock_get_build_configuration.assert_has_calls([call(id=1), call(id=2), call(id=3)])
    assert not mock_update.called
    assert not result


@patch('pnc_cli.buildconfigurationsets.get_set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.delete_specific', return_value=MagicMock(content='SUCCESS'))
def test_delete_build_config_set(mock_delete, mock_get_set_id):
    result = buildconfigurationsets.delete_build_configuration_set(id=1)
    mock_get_set_id.assert_called_once_with(1, None)
    mock_delete.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.buildconfigurationsets.get_set_id', return_value=None)
@patch('pnc_cli.buildconfigurationsets.sets_api.delete_specific')
def test_delete_build_config_set_id_notexist(mock_delete, mock_get_set_id):
    result = buildconfigurationsets.delete_build_configuration_set(id=1)
    mock_get_set_id.assert_called_once_with(1, None)
    assert not mock_delete.called
    assert not result


@patch('pnc_cli.buildconfigurationsets.get_set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.delete_specific', return_value=MagicMock(content='SUCCESS'))
def test_delete_build_config_set_name(mock_delete, mock_get_set_id):
    result = buildconfigurationsets.delete_build_configuration_set(name='testerino')
    mock_get_set_id.assert_called_once_with(None, 'testerino')
    mock_delete.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.buildconfigurationsets.get_set_id', return_value=None)
@patch('pnc_cli.buildconfigurationsets.sets_api.delete_specific')
def test_delete_build_config_set_name_notexist(mock_delete, mock_get_set_id):
    result = buildconfigurationsets.delete_build_configuration_set(name='testerino')
    mock_get_set_id.assert_called_once_with(None, 'testerino')
    assert not mock_delete.called
    assert not result


@patch('pnc_cli.buildconfigurationsets.sets_api.get_all', return_value=MagicMock(content=[MagicMock(id=1)]))
def test_set_exists(mock):
    result = buildconfigurationsets._set_exists(1)
    mock.assert_called_once_with()
    assert result


@patch('pnc_cli.buildconfigurationsets.sets_api.get_all', return_value=MagicMock(content=[MagicMock(id=1)]))
def test_set_exists_notexist(mock):
    result = buildconfigurationsets._set_exists(10)
    mock.assert_called_once_with()
    assert not result


@patch('pnc_cli.buildconfigurationsets._set_exists', return_value=True)
def test_get_set_id(mock):
    result = buildconfigurationsets.get_set_id(1, None)
    mock.assert_called_once_with(1)
    assert result == 1


@patch('pnc_cli.buildconfigurationsets._set_exists', return_value=False)
def test_get_set_id_notexist(mock):
    result = buildconfigurationsets.get_set_id(1, None)
    mock.assert_called_once_with(1)
    assert not result


@patch('pnc_cli.buildconfigurationsets.get_build_config_set_id_by_name', return_value=None)
def test_get_set_name(mock):
    result = buildconfigurationsets.get_set_id(None, 'testerino')
    mock.assert_called_once_with('testerino')
    assert not result


@patch('pnc_cli.buildconfigurationsets.get_build_config_set_id_by_name', return_value=None)
def test_get_set_name_notexist(mock):
    result = buildconfigurationsets.get_set_id(None, 'testerino')
    mock.assert_called_once_with('testerino')
    assert not result


def test_get_set_none():
    result = buildconfigurationsets.get_set_id(None, None)
    assert not result


@patch('pnc_cli.buildconfigurationsets.get_set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.build', return_value=MagicMock(content='SUCCESS'))
def test_build_set_id(mock_build, mock_get_set_id):
    result = buildconfigurationsets.build_set(id=1)
    mock_get_set_id.assert_called_once_with(1, None)
    mock_build.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.buildconfigurationsets.get_set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.build', return_value=MagicMock(content='SUCCESS'))
def test_build_set_name(mock_build, mock_get_set_id):
    result = buildconfigurationsets.build_set(name='testerino')
    mock_get_set_id.assert_called_once_with(None, 'testerino')
    mock_build.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.buildconfigurationsets.get_set_id', return_value=None)
@patch('pnc_cli.buildconfigurationsets.sets_api.build')
def test_build_set_notexist(mock_build, mock_get_set_id):
    result = buildconfigurationsets.build_set(id=1)
    mock_get_set_id.assert_called_once_with(1, None)
    assert not mock_build.called
    assert not result


@patch('pnc_cli.buildconfigurationsets.get_set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.get_configurations', return_value=MagicMock(content='SUCCESS'))
def test_list_build_configurations_for_set_id(mock_get_configurations, mock_get_set_id):
    result = buildconfigurationsets.list_build_configurations_for_set(id=1)
    mock_get_set_id.assert_called_once_with(1, None)
    mock_get_configurations.assert_called_once_with(id=1, page_size=200, q="", sort="")
    assert result == 'SUCCESS'


@patch('pnc_cli.buildconfigurationsets.get_set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.get_configurations', return_value=MagicMock(content='SUCCESS'))
def test_list_build_configurations_for_set_name(mock_get_configurations, mock_get_set_id):
    result = buildconfigurationsets.list_build_configurations_for_set(name='testerino')
    mock_get_set_id.assert_called_once_with(None, 'testerino')
    mock_get_configurations.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.buildconfigurationsets.get_set_id', return_value=None)
@patch('pnc_cli.buildconfigurationsets.sets_api.get_configurations')
def test_list_build_configurations_for_set_name(mock_get_configurations, mock_get_set_id):
    result = buildconfigurationsets.list_build_configurations_for_set(name='testerino')
    mock_get_set_id.assert_called_once_with(None, 'testerino')
    assert not mock_get_configurations.called
    assert not result


@patch('pnc_cli.buildconfigurationsets.get_set_id', return_value=1)
@patch('pnc_cli.buildconfigurations.get_config_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.configs_api.get_specific', return_value=MagicMock(content='BuildConfiguration'))
@patch('pnc_cli.buildconfigurationsets.sets_api.add_configuration', return_value=MagicMock(content='SUCCESS'))
def test_add_build_configuration_to_set_id(mock_add_config, mock_get_config, mock_get_config_id, mock_get_set_id):
    result = buildconfigurationsets.add_build_configuration_to_set(set_id=1, config_id=1)
    mock_get_set_id.assert_called_once_with(1, None)
    mock_get_config_id.assert_called_once_with(1, None)
    mock_get_config.assert_called_once_with(id=1)
    mock_add_config.assert_called_once_with(id=1, body='BuildConfiguration')
    assert result == 'SUCCESS'

@patch('pnc_cli.buildconfigurationsets.get_set_id', return_value=1)
@patch('pnc_cli.buildconfigurations.get_config_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.configs_api.get_specific', return_value=MagicMock(content='BuildConfiguration'))
@patch('pnc_cli.buildconfigurationsets.sets_api.add_configuration', return_value=MagicMock(content='SUCCESS'))
def test_add_build_configuration_to_set_name(mock_add_config, mock_get_config, mock_get_config_id, mock_get_set_id):
    result = buildconfigurationsets.add_build_configuration_to_set(set_name='testerino', config_id=1)
    mock_get_set_id.assert_called_once_with(None, 'testerino')
    mock_get_config_id.assert_called_once_with(1, None)
    mock_get_config.assert_called_once_with(id=1)
    mock_add_config.assert_called_once_with(id=1, body='BuildConfiguration')
    assert result == 'SUCCESS'


@patch('pnc_cli.buildconfigurationsets.get_set_id', return_value=None)
@patch('pnc_cli.buildconfigurations.get_config_id')
@patch('pnc_cli.buildconfigurationsets.configs_api.get_specific')
@patch('pnc_cli.buildconfigurationsets.sets_api.add_configuration')
def test_add_build_configuration_to_set_notexist(mock_add_config, mock_get_config, mock_get_config_id, mock_get_set_id):
    result = buildconfigurationsets.add_build_configuration_to_set(set_name='testerino', config_id=1)
    mock_get_set_id.assert_called_once_with(None, 'testerino')
    assert not mock_get_config_id.called
    assert not mock_get_config.called
    assert not mock_add_config.called
    assert not result


@patch('pnc_cli.buildconfigurationsets.get_set_id', return_value=1)
@patch('pnc_cli.buildconfigurations.get_config_id', return_value=None)
@patch('pnc_cli.buildconfigurationsets.configs_api.get_specific')
@patch('pnc_cli.buildconfigurationsets.sets_api.add_configuration')
def test_add_build_configuration_to_set_id_notexist(mock_add_config, mock_get_config, mock_get_config_id, mock_get_set_id):
    result = buildconfigurationsets.add_build_configuration_to_set(set_id=1, config_id=1)
    mock_get_set_id.assert_called_once_with(1, None)
    mock_get_config_id.assert_called_once_with(1, None)
    assert not mock_get_config.called
    assert not mock_add_config.called
    assert not result

@patch('pnc_cli.buildconfigurationsets.get_set_id', return_value=1)
@patch('pnc_cli.buildconfigurations.get_config_id', return_value=None)
@patch('pnc_cli.buildconfigurationsets.configs_api.get_specific')
@patch('pnc_cli.buildconfigurationsets.sets_api.add_configuration')
def test_add_build_configuration_to_set_name_notexist(mock_add_config, mock_get_config, mock_get_config_id, mock_get_set_id):
    result = buildconfigurationsets.add_build_configuration_to_set(set_id=1, config_name='testerino')
    mock_get_set_id.assert_called_once_with(1, None)
    mock_get_config_id.assert_called_once_with(None, 'testerino')
    assert not mock_get_config.called
    assert not mock_add_config.called
    assert not result

@patch('pnc_cli.buildconfigurationsets.get_set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.get_build_records', return_value=MagicMock(content='SUCCESS'))
def test_list_build_records_for_set_id(mock_get_records, mock_get_set_id):
    result = buildconfigurationsets.list_build_records_for_set(id=1)
    mock_get_set_id.assert_called_once_with(1, None)
    mock_get_records.assert_called_once_with(id=1, page_size=200, q="", sort="")
    assert result == 'SUCCESS'

@patch('pnc_cli.buildconfigurationsets.get_set_id', return_value=None)
@patch('pnc_cli.buildconfigurationsets.sets_api.get_build_records', return_value=MagicMock(content='SUCCESS'))
def test_list_build_records_for_set_id_notexist(mock_get_records, mock_get_set_id):
    result = buildconfigurationsets.list_build_records_for_set(id=1)
    mock_get_set_id.assert_called_once_with(1, None)
    assert not mock_get_records.called
    assert not result

@patch('pnc_cli.buildconfigurationsets.get_set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.get_build_records', return_value=MagicMock(content='SUCCESS'))
def test_list_build_records_for_set_name(mock_get_records, mock_get_set_id):
    result = buildconfigurationsets.list_build_records_for_set(name='testerino')
    mock_get_set_id.assert_called_once_with(None, 'testerino')
    mock_get_records.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.buildconfigurationsets.get_set_id', return_value=1)
@patch('pnc_cli.buildconfigurationsets.sets_api.get_build_records', return_value=MagicMock(content='SUCCESS'))
def test_list_build_records_for_set_name(mock_get_records, mock_get_set_id):
    result = buildconfigurationsets.list_build_records_for_set(name='testerino')
    mock_get_set_id.assert_called_once_with(None, 'testerino')
    mock_get_records.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.buildconfigurationsets.get_set_id', return_value=None)
@patch('pnc_cli.buildconfigurationsets.sets_api.get_build_records', return_value=MagicMock(content='SUCCESS'))
def test_list_build_records_for_set_name(mock_get_records, mock_get_set_id):
    result = buildconfigurationsets.list_build_records_for_set(name='testerino')
    mock_get_set_id.assert_called_once_with(None, 'testerino')
    assert not mock_get_records.called
    assert not result
