import test.utils

__author__ = 'thauser'
from mock import MagicMock, patch, call
from pnc_cli import buildconfigurations

@patch('pnc_cli.buildconfigurations.config_id_exists', return_value=True)
def test_get_config_id_id(mock):
    result = buildconfigurations.get_config_id(1,None)
    mock.assert_called_once_with(1)
    assert result == 1

@patch('pnc_cli.buildconfigurations.config_id_exists', return_value=False)
def test_get_config_id_no_id(mock):
    result = buildconfigurations.get_config_id(1,None)
    mock.assert_called_once_with(1)
    assert not result

@patch('pnc_cli.buildconfigurations.get_build_configuration_id_by_name', return_value=1)
def test_get_config_id_name(mock):
    result = buildconfigurations.get_config_id(None, 'testerino')
    mock.assert_called_once_with('testerino')
    assert result == 1

@patch('pnc_cli.buildconfigurations.get_build_configuration_id_by_name', return_value=None)
def test_get_config_id_no_name(mock):
    result = buildconfigurations.get_config_id(None, 'testerino')
    mock.assert_called_once_with('testerino')
    assert not result

def test_get_config_id_none():
    result = buildconfigurations.get_config_id(None,None)
    assert not result

@patch('pnc_cli.buildconfigurations.configs_api.get_all', return_value=MagicMock(content=[MagicMock(id=1), MagicMock(id=2)]))
def test_config_id_exists(mock):
    result = buildconfigurations.config_id_exists(1)
    mock.assert_called_once_with()
    assert result

@patch('pnc_cli.buildconfigurations.configs_api.get_all', return_value=MagicMock(content=[MagicMock(id=1), MagicMock(id=2)]))
def test_config_id_exists_false(mock):
    result = buildconfigurations.config_id_exists(5)
    mock.assert_called_once_with()
    assert not result

@patch('pnc_cli.buildconfigurations.configs_api.get_all')
def test_get_build_configuration_id_by_name(mock):
    mock.return_value = test.utils.create_mock_content_list()
    result = buildconfigurations.get_build_configuration_id_by_name('testerino')
    mock.assert_called_once_with()
    assert result == 1

@patch('pnc_cli.buildconfigurations.configs_api.get_all', return_value=MagicMock(content=[MagicMock(name='testerino', id=1), MagicMock(name='another', id=2)]))
def test_get_build_configuration_id_by_name_notexist(mock):
    result = buildconfigurations.get_build_configuration_id_by_name('doesntexist')
    mock.assert_called_once_with()
    assert not result


@patch('pnc_cli.buildconfigurations.get_config_id', return_value=1)
@patch('pnc_cli.buildconfigurations.configs_api.trigger', return_value=MagicMock(content='buildstarted'))
def test_build_id(mock_trigger, mock_get_config_id):
    result = buildconfigurations.build(id=1)
    mock_get_config_id.assert_called_once_with(1, None)
    mock_trigger.assert_called_once_with(id=1)
    assert result == 'buildstarted'


@patch('pnc_cli.buildconfigurations.get_config_id', return_value=1)
@patch('pnc_cli.buildconfigurations.configs_api.trigger', return_value=MagicMock(content='buildstarted'))
def test_build_name(mock_trigger, mock_get_config_id):
    result = buildconfigurations.build(name='testerino')
    mock_get_config_id.assert_called_once_with(None, 'testerino')
    mock_trigger.assert_called_once_with(id=1)
    assert result == 'buildstarted'


@patch('pnc_cli.buildconfigurations.get_config_id', return_value=None)
@patch('pnc_cli.buildconfigurations.configs_api.trigger')
def test_build_notexist(mock_trigger, mock_get_config_id):
    result = buildconfigurations.build(id=1)
    mock_get_config_id.assert_called_once_with(1, None)
    assert not mock_trigger.called
    assert not result


@patch('pnc_cli.buildconfigurations.get_config_id', return_value=1)
@patch('pnc_cli.buildconfigurations.configs_api.get_specific', return_value=MagicMock(content='buildconfiguration'))
def test_get_build_configuration_id(mock_get_specific, mock_get_config_id):
    result = buildconfigurations.get_build_configuration(id=1)
    mock_get_config_id.assert_called_once_with(1, None)
    mock_get_specific.assert_called_once_with(id=1)
    assert result == 'buildconfiguration'


@patch('pnc_cli.buildconfigurations.get_config_id', return_value=1)
@patch('pnc_cli.buildconfigurations.configs_api.get_specific', return_value=MagicMock(content='buildconfiguration'))
def test_get_build_configuration_id(mock_get_specific, mock_get_config_id):
    result = buildconfigurations.get_build_configuration(name='testerino')
    mock_get_config_id.assert_called_once_with(None, 'testerino')
    mock_get_specific.assert_called_once_with(id=1)
    assert result == 'buildconfiguration'


@patch('pnc_cli.buildconfigurations.get_config_id', return_value=None)
@patch('pnc_cli.buildconfigurations.configs_api.get_specific')
def test_get_build_configuration_notexist(mock_get_specific, mock_get_config_id):
    result = buildconfigurations.get_build_configuration(id=1)
    mock_get_config_id.assert_called_once_with(1, None)
    assert not mock_get_specific.called
    assert not result


@patch('pnc_cli.buildconfigurations.get_config_id', return_value=1)
@patch('pnc_cli.buildconfigurations.configs_api.get_specific',
       return_value=MagicMock(content=buildconfigurations.create_build_conf_object(build_script='testerino')))
@patch('pnc_cli.buildconfigurations.configs_api.update', return_value=MagicMock(content='updated-configuration'))
def test_update_build_configuration_id(mock_update, mock_get_specific, mock_get_config_id):
    result = buildconfigurations.update_build_configuration(id=1, build_script='mvn install')
    mock_get_config_id.assert_called_once_with(1, None)
    mock_get_specific.assert_called_once_with(id=1)
    kwargs = mock_update.call_args
    bc = buildconfigurations.create_build_conf_object(build_script='mvn install', id=1)
    assert mock_update.call_count == 1
    assert cmp(kwargs, bc)
    assert result == 'updated-configuration'


@patch('pnc_cli.buildconfigurations.get_config_id', return_value=1)
@patch('pnc_cli.buildconfigurations.configs_api.get_specific',
       return_value=MagicMock(content=buildconfigurations.create_build_conf_object(build_script='testerino')))
@patch('pnc_cli.buildconfigurations.configs_api.update', return_value=MagicMock(content='updated-configuration'))
def test_update_build_configuration_name(mock_update, mock_get_specific, mock_get_config_id):
    result = buildconfigurations.update_build_configuration(name='testerino', build_script='mvn install')
    mock_get_config_id.assert_called_once_with(None, 'testerino')
    assert mock_update.called
    kwargs = mock_update.call_args
    bc = buildconfigurations.create_build_conf_object(build_script='mvn install', id=1)
    assert mock_update.call_count == 1
    assert cmp(kwargs, bc)
    assert result == 'updated-configuration'


@patch('pnc_cli.buildconfigurations.get_config_id', return_value=None)
@patch('pnc_cli.buildconfigurations.configs_api.get_specific')
@patch('pnc_cli.buildconfigurations.configs_api.update')
def test_update_build_configuration_notexist(mock_update, mock_get_specific, mock_get_config_id):
    result = buildconfigurations.update_build_configuration(name='testerino', build_script='mvn install')
    mock_get_config_id.assert_called_once_with(None, 'testerino')
    assert not mock_get_specific.called
    assert not mock_update.called
    assert not result


@patch('pnc_cli.buildconfigurations.create_build_conf_object', return_value='test-build-config-object')
@patch('pnc_cli.buildconfigurations.configs_api.create_new', return_value=MagicMock(content='test-build-config-object'))
def test_create_build_configuration(mock_create_new, mock_create_build_conf_object):
    result = buildconfigurations.create_build_configuration(name='testerino', description='test description')
    mock_create_build_conf_object.assert_called_once_with(name='testerino', description='test description')
    mock_create_new.assert_called_once_with(body='test-build-config-object')
    assert result == 'test-build-config-object'


@patch('pnc_cli.buildconfigurations.get_config_id', return_value=1)
@patch('pnc_cli.buildconfigurations.configs_api.delete_specific', return_value=MagicMock(content=True))
def test_delete_build_configuration_id(mock_delete_specific, mock_get_config_id):
    result = buildconfigurations.delete_build_configuration(id=1)
    mock_get_config_id.assert_called_once_with(1, None)
    mock_delete_specific.assert_called_once_with(id=1)
    assert result


@patch('pnc_cli.buildconfigurations.get_config_id', return_value=1)
@patch('pnc_cli.buildconfigurations.configs_api.delete_specific', return_value=MagicMock(content=True))
def test_delete_build_configuration_name(mock_delete_specific, mock_get_config_id):
    result = buildconfigurations.delete_build_configuration(name='testerino')
    mock_get_config_id.assert_called_once_with(None, 'testerino')
    mock_delete_specific.assert_called_once_with(id=1)
    assert result


@patch('pnc_cli.buildconfigurations.get_config_id', return_value=None)
@patch('pnc_cli.buildconfigurations.configs_api.delete_specific')
def test_delete_build_configuration_notexist(mock_delete_specific, mock_get_config_id):
    result = buildconfigurations.delete_build_configuration(name='testerino')
    mock_get_config_id.assert_called_once_with(None, 'testerino')
    assert not mock_delete_specific.called
    assert not result


@patch('pnc_cli.products.get_product_id', return_value=1)
@patch('pnc_cli.buildconfigurations.configs_api.get_all_by_product_id', return_value=MagicMock(content=[1,2,3]))
def test_list_build_configurations_for_product_id(mock_get_all_by_product_id, mock_get_product_id):
    result = buildconfigurations.list_build_configurations_for_product(id=1)
    mock_get_product_id.called_once_with(1, None)
    mock_get_all_by_product_id.called_once_with(product_id=1)
    assert result == [1,2,3]

@patch('pnc_cli.products.get_product_id', return_value=1)
@patch('pnc_cli.buildconfigurations.configs_api.get_all_by_product_id', return_value=MagicMock(content=[1,2,3]))
def test_list_build_configurations_for_product_name(mock_get_all_by_product_id, mock_get_product_id):
    result = buildconfigurations.list_build_configurations_for_product(name='testerino')
    mock_get_product_id.called_once_with(None, 'testerino')
    mock_get_all_by_product_id.called_once_with(product_id=1)
    assert result == [1,2,3]

@patch('pnc_cli.products.get_product_id', return_value=None)
@patch('pnc_cli.buildconfigurations.configs_api.get_all_by_product_id')
def test_list_build_configurations_for_product_notexist(mock_get_all_by_product_id, mock_get_product_id):
    result = buildconfigurations.list_build_configurations_for_product(name='testerino')
    mock_get_product_id.called_once_with(None, 'testerino')
    assert not mock_get_all_by_product_id.called
    assert not result


@patch('pnc_cli.products.get_product_id', return_value=1)
@patch('pnc_cli.productversions.version_exists', return_value=True)
@patch('pnc_cli.buildconfigurations.configs_api.get_all_by_product_id_1', return_value=MagicMock(content=[1,2,3]))
def test_list_build_configurations_for_product_version(mock_get_all_by_product_id_1, mock_version_exists, mock_get_product_id):
    result = buildconfigurations.list_build_configurations_for_product_version(product_id=1,version_id=2)
    mock_get_product_id.assert_called_once_with(1)
    mock_version_exists.assert_called_once_with(2)
    mock_get_all_by_product_id_1.assert_called_once_with(product_id=1, version_id=2)
    assert result == [1,2,3]

@patch('pnc_cli.products.get_product_id', return_value=None)
@patch('pnc_cli.productversions.version_exists')
@patch('pnc_cli.buildconfigurations.configs_api.get_all_by_product_id_1')
def test_list_build_configurations_for_product_version_no_product(mock_get_all_by_product_id_1, mock_version_exists, mock_get_product_id):
    result = buildconfigurations.list_build_configurations_for_product_version(product_id=1,version_id=2)
    mock_get_product_id.assert_called_once_with(1)
    assert not mock_version_exists.called
    assert not mock_get_all_by_product_id_1.called
    assert not result

@patch('pnc_cli.products.get_product_id', return_value=1)
@patch('pnc_cli.productversions.version_exists', return_value=False)
@patch('pnc_cli.buildconfigurations.configs_api.get_all_by_product_id_1')
def test_list_build_configurations_for_product_version_no_version(mock_get_all_by_product_id_1, mock_version_exists, mock_get_product_id):
    result = buildconfigurations.list_build_configurations_for_product_version(product_id=1,version_id=2)
    mock_get_product_id.assert_called_once_with(1)
    mock_version_exists.assert_called_once_with(2)
    assert not mock_get_all_by_product_id_1.called
    assert not result


@patch('pnc_cli.buildconfigurations.get_config_id', return_value=1)
@patch('pnc_cli.buildconfigurations.configs_api.get_dependencies', return_value=MagicMock(content=['dep1','dep2']))
def test_list_dependencies_id(mock_get_dependencies, mock_get_config_id):
    result = buildconfigurations.list_dependencies(id=1)
    mock_get_config_id.assert_called_once_with(1, None)
    mock_get_dependencies.assert_called_once_with(id=1)
    assert result == ['dep1','dep2']

@patch('pnc_cli.buildconfigurations.get_config_id', return_value=1)
@patch('pnc_cli.buildconfigurations.configs_api.get_dependencies', return_value=MagicMock(content=['dep1','dep2']))
def test_list_dependencies_name(mock_get_dependencies, mock_get_config_id):
    result = buildconfigurations.list_dependencies(name='testerino')
    mock_get_config_id.assert_called_once_with(None, 'testerino')
    mock_get_dependencies.assert_called_once_with(id=1)
    assert result == ['dep1','dep2']

@patch('pnc_cli.buildconfigurations.get_config_id', return_value=None)
@patch('pnc_cli.buildconfigurations.configs_api.get_dependencies')
def test_list_dependencies_notexist(mock_get_dependencies, mock_get_config_id):
    result = buildconfigurations.list_dependencies(name='testerino')
    mock_get_config_id.assert_called_once_with(None, 'testerino')
    assert not mock_get_dependencies.called
    assert not result


@patch('pnc_cli.buildconfigurations.get_config_id', side_effect=[1,2])
@patch('pnc_cli.buildconfigurations.configs_api.get_specific', return_value=MagicMock(content='added-dep'))
@patch('pnc_cli.buildconfigurations.configs_api.add_dependency', return_value=MagicMock(content='SUCCESS'))
def test_add_dependency_ids(mock_add_dependency, mock_get_specific, mock_get_config_id):
    result = buildconfigurations.add_dependency(id=1,dependency_id=2)
    calls = [call(1,None), call(2,None)]
    mock_get_config_id.assert_has_calls(calls)
    mock_get_specific.assert_called_once_with(id=2)
    mock_add_dependency.assert_called_once_with(id=1, body='added-dep')
    assert result == 'SUCCESS'

@patch('pnc_cli.buildconfigurations.get_config_id', side_effect=[1,2])
@patch('pnc_cli.buildconfigurations.configs_api.get_specific', return_value=MagicMock(content='added-dep'))
@patch('pnc_cli.buildconfigurations.configs_api.add_dependency', return_value=MagicMock(content='SUCCESS'))
def test_add_dependency_id_name(mock_add_dependency, mock_get_specific, mock_get_config_id):
    result = buildconfigurations.add_dependency(id=1,dependency_name='testerino')
    calls = [call(1,None), call(None,'testerino')]
    mock_get_config_id.assert_has_calls(calls)
    mock_get_specific.assert_called_once_with(id=2)
    mock_add_dependency.assert_called_once_with(id=1, body='added-dep')
    assert result == 'SUCCESS'

@patch('pnc_cli.buildconfigurations.get_config_id', side_effect=[1,2])
@patch('pnc_cli.buildconfigurations.configs_api.get_specific', return_value=MagicMock(content='added-dep'))
@patch('pnc_cli.buildconfigurations.configs_api.add_dependency', return_value=MagicMock(content='SUCCESS'))
def test_add_dependency_name_id(mock_add_dependency, mock_get_specific, mock_get_config_id):
    result = buildconfigurations.add_dependency(name='testerino',dependency_id=2)
    calls = [call(None,'testerino'), call(2,None)]
    mock_get_config_id.assert_has_calls(calls)
    mock_get_specific.assert_called_once_with(id=2)
    mock_add_dependency.assert_called_once_with(id=1, body='added-dep')
    assert result == 'SUCCESS'

@patch('pnc_cli.buildconfigurations.get_config_id', side_effect=[1,2])
@patch('pnc_cli.buildconfigurations.configs_api.get_specific', return_value=MagicMock(content='added-dep'))
@patch('pnc_cli.buildconfigurations.configs_api.add_dependency', return_value=MagicMock(content='SUCCESS'))
def test_add_dependency_names(mock_add_dependency, mock_get_specific, mock_get_config_id):
    result = buildconfigurations.add_dependency(name='testerino',dependency_name='testerino2')
    calls = [call(None,'testerino'), call(None,'testerino2')]
    mock_get_config_id.assert_has_calls(calls)
    mock_get_specific.assert_called_once_with(id=2)
    mock_add_dependency.assert_called_once_with(id=1, body='added-dep')
    assert result == 'SUCCESS'

@patch('pnc_cli.buildconfigurations.get_config_id', side_effect=[None,2])
@patch('pnc_cli.buildconfigurations.configs_api.get_specific')
@patch('pnc_cli.buildconfigurations.configs_api.add_dependency')
def test_add_dependency_no_conf(mock_add_dependency, mock_get_specific, mock_get_config_id):
    result = buildconfigurations.add_dependency(name='testerino',dependency_name='testerino2')
    mock_get_config_id.assert_called_once_with(None, 'testerino')
    assert not mock_get_specific.called
    assert not mock_add_dependency.called
    assert not result

@patch('pnc_cli.buildconfigurations.get_config_id', side_effect=[1,None])
@patch('pnc_cli.buildconfigurations.configs_api.get_specific')
@patch('pnc_cli.buildconfigurations.configs_api.add_dependency')
def test_add_dependency_no_dep(mock_add_dependency, mock_get_specific, mock_get_config_id):
    result = buildconfigurations.add_dependency(name='testerino',dependency_name='testerino2')
    calls = [call(None,'testerino'), call(None,'testerino2')]
    mock_get_config_id.assert_has_calls(calls)
    assert not mock_get_specific.called
    assert not mock_add_dependency.called
    assert not result


@patch('pnc_cli.buildconfigurations.get_config_id', side_effect=[1,2])
@patch('pnc_cli.buildconfigurations.configs_api.remove_dependency', return_value=MagicMock(content='SUCCESS'))
def test_remove_dependency_ids(mock_remove_dependency, mock_get_config_id):
    result = buildconfigurations.remove_dependency(id=1,dependency_id=2)
    calls = [call(1, None),call(2, None)]
    mock_get_config_id.assert_has_calls(calls)
    mock_remove_dependency.assert_called_once_with(id=1, dependency_id=2)
    assert result == 'SUCCESS'

@patch('pnc_cli.buildconfigurations.get_config_id', side_effect=[1,2])
@patch('pnc_cli.buildconfigurations.configs_api.remove_dependency', return_value=MagicMock(content='SUCCESS'))
def test_remove_dependency_id_name(mock_remove_dependency, mock_get_config_id):
    result = buildconfigurations.remove_dependency(id=1,dependency_name='testerino')
    calls = [call(1, None),call(None, 'testerino')]
    mock_get_config_id.assert_has_calls(calls)
    mock_remove_dependency.assert_called_once_with(id=1, dependency_id=2)
    assert result == 'SUCCESS'

@patch('pnc_cli.buildconfigurations.get_config_id', side_effect=[1,2])
@patch('pnc_cli.buildconfigurations.configs_api.remove_dependency', return_value=MagicMock(content='SUCCESS'))
def test_remove_dependency_name_id(mock_remove_dependency, mock_get_config_id):
    result = buildconfigurations.remove_dependency(name='testerino',dependency_id=2)
    calls = [call(None, 'testerino'), call(2, None)]
    mock_get_config_id.assert_has_calls(calls)
    mock_remove_dependency.assert_called_once_with(id=1, dependency_id=2)
    assert result == 'SUCCESS'

@patch('pnc_cli.buildconfigurations.get_config_id', side_effect=[1,2])
@patch('pnc_cli.buildconfigurations.configs_api.remove_dependency', return_value=MagicMock(content='SUCCESS'))
def test_remove_dependency_names(mock_remove_dependency, mock_get_config_id):
    result = buildconfigurations.remove_dependency(name='testerino', dependency_name='testerino')
    calls = [call(None,'testerino'), call(None, 'testerino')]
    mock_get_config_id.assert_has_calls(calls)
    mock_remove_dependency.assert_called_once_with(id=1, dependency_id=2)
    assert result == 'SUCCESS'

@patch('pnc_cli.buildconfigurations.get_config_id', side_effect=[None,2])
@patch('pnc_cli.buildconfigurations.configs_api.remove_dependency')
def test_remove_dependency_no_conf(mock_remove_dependency, mock_get_config_id):
    result = buildconfigurations.remove_dependency(id=1,dependency_id=2)
    mock_get_config_id.assert_called_once_with(1,None)
    assert not mock_remove_dependency.called
    assert not result

@patch('pnc_cli.buildconfigurations.get_config_id', side_effect=[1,None])
@patch('pnc_cli.buildconfigurations.configs_api.remove_dependency')
def test_remove_dependency_no_dep(mock_remove_dependency, mock_get_config_id):
    result = buildconfigurations.remove_dependency(id=1,dependency_id=2)
    calls = [call(1, None),call(2, None)]
    mock_get_config_id.assert_has_calls(calls)
    assert not mock_remove_dependency.called
    assert not result

@patch('pnc_cli.buildconfigurations.get_config_id', return_value=1)
@patch('pnc_cli.buildconfigurations.configs_api.get_product_versions', return_value=MagicMock(content=[1,2,3]))
def test_list_product_versions_for_build_configuration_id(mock_get_product_versions, mock_get_config_id):
    result = buildconfigurations.list_product_versions_for_build_configuration(id=1)
    mock_get_config_id.assert_called_once_with(1,None)
    mock_get_product_versions.assert_called_once_with(id=1)
    assert result == [1,2,3]

@patch('pnc_cli.buildconfigurations.get_config_id', return_value=1)
@patch('pnc_cli.buildconfigurations.configs_api.get_product_versions', return_value=MagicMock(content=[1,2,3]))
def test_list_product_versions_for_build_configuration_name(mock_get_product_versions, mock_get_config_id):
    result = buildconfigurations.list_product_versions_for_build_configuration(name='testerino')
    mock_get_config_id.assert_called_once_with(None, 'testerino')
    mock_get_product_versions.assert_called_once_with(id=1)
    assert result == [1,2,3]

@patch('pnc_cli.buildconfigurations.get_config_id', return_value=None)
@patch('pnc_cli.buildconfigurations.configs_api.get_product_versions')
def test_list_product_versions_for_build_configuration_notexist(mock_get_product_versions, mock_get_config_id):
    result = buildconfigurations.list_product_versions_for_build_configuration(id=1)
    mock_get_config_id.assert_called_once_with(1,None)
    assert not mock_get_product_versions.called
    assert not result

@patch('pnc_cli.buildconfigurations.get_config_id', return_value=1)
@patch('pnc_cli.productversions.version_exists', return_value=True)
@patch('pnc_cli.productversions.get_product_version', return_value=MagicMock(content='productversion'))
@patch('pnc_cli.buildconfigurations.configs_api.add_product_version', return_value=MagicMock(content='testresponse'))
def test_add_product_version_to_build_configuration_id(mock_add_product_version,
                                                    mock_get_product_version,
                                                    mock_version_exists,
                                                    mock_get_config_id):
    result = buildconfigurations.add_product_version_to_build_configuration(id=1, product_version_id=2)
    mock_get_config_id.assert_called_once_with(1, None)
    mock_version_exists.assert_called_once_with(2)
    mock_get_product_version.assert_called_once_with(id=2)
    mock_add_product_version.assert_called_once_with(id=1,body='productversion')
    assert result == 'testresponse'

@patch('pnc_cli.buildconfigurations.get_config_id', return_value=1)
@patch('pnc_cli.productversions.version_exists', return_value=True)
@patch('pnc_cli.productversions.get_product_version', return_value=MagicMock(content='productversion'))
@patch('pnc_cli.buildconfigurations.configs_api.add_product_version', return_value=MagicMock(content='testresponse'))
def test_add_product_version_to_build_configuration_name(mock_add_product_version,
                                                    mock_get_product_version,
                                                    mock_version_exists,
                                                    mock_get_config_id):
    result = buildconfigurations.add_product_version_to_build_configuration(name='testerino', product_version_id=2)
    mock_get_config_id.assert_called_once_with(None, 'testerino')
    mock_version_exists.assert_called_once_with(2)
    mock_get_product_version.assert_called_once_with(id=2)
    mock_add_product_version.assert_called_once_with(id=1,body='productversion')
    assert result == 'testresponse'

@patch('pnc_cli.buildconfigurations.get_config_id', return_value=None)
@patch('pnc_cli.productversions.version_exists')
@patch('pnc_cli.productversions.get_product_version')
@patch('pnc_cli.buildconfigurations.configs_api.add_product_version')
def test_add_product_version_to_build_configuration_notexist(mock_add_product_version,
                                                    mock_get_product_version,
                                                    mock_version_exists,
                                                    mock_get_config_id):
    result = buildconfigurations.add_product_version_to_build_configuration(id=1, product_version_id=2)
    mock_get_config_id.assert_called_once_with(1, None)
    assert not mock_version_exists.called
    assert not mock_get_product_version.called
    assert not mock_add_product_version.called
    assert not result

@patch('pnc_cli.buildconfigurations.get_config_id', return_value=1)
@patch('pnc_cli.productversions.version_exists', return_value=False)
@patch('pnc_cli.productversions.get_product_version', return_value=MagicMock(content='productversion'))
@patch('pnc_cli.buildconfigurations.configs_api.add_product_version', return_value=MagicMock(content='testresponse'))
def test_add_product_version_to_build_configuration_noversion(mock_add_product_version,
                                                    mock_get_product_version,
                                                    mock_version_exists,
                                                    mock_get_config_id):
    result = buildconfigurations.add_product_version_to_build_configuration(id=1, product_version_id=2)
    mock_get_config_id.assert_called_once_with(1, None)
    mock_version_exists.assert_called_once_with(2)
    assert not mock_get_product_version.called
    assert not mock_add_product_version.called
    assert not result


@patch('pnc_cli.buildconfigurations.get_config_id', return_value=1)
@patch('pnc_cli.buildconfigurations.configs_api.get_product_versions',
       return_value=MagicMock(content=[MagicMock(id=1), MagicMock(id=2)]))
@patch('pnc_cli.buildconfigurations.configs_api.remove_product_version', return_value=MagicMock(content='SUCCESS'))
def test_remove_product_version_from_build_configuration_id(mock_remove_product_version,
                                                            mock_get_product_versions,
                                                            mock_get_config_id):
    result = buildconfigurations.remove_product_version_from_build_configuration(id=1, product_version_id=1)
    mock_get_config_id.assert_called_once_with(1, None)
    mock_get_product_versions.assert_called_once_with(id=1)
    mock_remove_product_version.assert_called_once_with(id=1, product_version_id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.buildconfigurations.get_config_id', return_value=1)
@patch('pnc_cli.buildconfigurations.configs_api.get_product_versions',
       return_value=MagicMock(content=[MagicMock(id=1), MagicMock(id=2)]))
@patch('pnc_cli.buildconfigurations.configs_api.remove_product_version', return_value=MagicMock(content='SUCCESS'))
def test_remove_product_version_from_build_configuration_name(mock_remove_product_version,
                                                              mock_get_product_versions,
                                                              mock_get_config_id):
    result = buildconfigurations.remove_product_version_from_build_configuration(name='testerino', product_version_id=1)
    mock_get_config_id.assert_called_once_with(None, 'testerino')
    mock_get_product_versions.assert_called_once_with(id=1)
    mock_remove_product_version.assert_called_once_with(id=1, product_version_id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.buildconfigurations.get_config_id', return_value=None)
@patch('pnc_cli.buildconfigurations.configs_api.get_product_versions',
       return_value=MagicMock(content=[MagicMock(id=1), MagicMock(id=2)]))
@patch('pnc_cli.buildconfigurations.configs_api.remove_product_version', return_value=MagicMock(content='SUCCESS'))
def test_remove_product_version_from_build_configuration_notexist(mock_remove_product_version,
                                                                  mock_get_product_versions, mock_get_config_id):
    result = buildconfigurations.remove_product_version_from_build_configuration(id=1, product_version_id=1)
    mock_get_config_id.assert_called_once_with(1, None)
    assert not mock_get_product_versions.called
    assert not mock_remove_product_version.called
    assert not result


@patch('pnc_cli.buildconfigurations.get_config_id', return_value=1)
@patch('pnc_cli.buildconfigurations.configs_api.get_product_versions', return_value=MagicMock(content=[]))
@patch('pnc_cli.buildconfigurations.configs_api.remove_product_version', return_value=MagicMock(content='SUCCESS'))
def test_remove_product_version_from_build_configuration_no_version(mock_remove_product_version,
                                                                    mock_get_product_versions, mock_get_config_id):
    result = buildconfigurations.remove_product_version_from_build_configuration(id=1, product_version_id=1)
    mock_get_config_id.assert_called_once_with(1, None)
    mock_get_product_versions.called_once_with(id=1)
    assert not mock_remove_product_version.called
    assert not result


@patch('pnc_cli.buildconfigurations.get_config_id', return_value=1)
@patch('pnc_cli.buildconfigurations.configs_api.get_revisions', return_value=MagicMock(content=['rev1', 'rev2']))
def test_list_revisions_of_build_configuration_id(mock_get_revisions, mock_get_config_id):
    result = buildconfigurations.list_revisions_of_build_configuration(id=1)
    mock_get_config_id.assert_called_once_with(1, None)
    mock_get_revisions.assert_called_once_with(id=1)
    assert result == ['rev1', 'rev2']


@patch('pnc_cli.buildconfigurations.get_config_id', return_value=1)
@patch('pnc_cli.buildconfigurations.configs_api.get_revisions', return_value=MagicMock(content=['rev1', 'rev2']))
def test_list_revisions_of_build_configuration(mock_get_revisions, mock_get_config_id):
    result = buildconfigurations.list_revisions_of_build_configuration(name='testerino')
    mock_get_config_id.assert_called_once_with(None, 'testerino')
    mock_get_revisions.assert_called_once_with(id=1)
    assert result == ['rev1', 'rev2']


@patch('pnc_cli.buildconfigurations.get_config_id', return_value=None)
@patch('pnc_cli.buildconfigurations.configs_api.get_revisions')
def test_list_revisions_of_build_configuration(mock_get_revisions, mock_get_config_id):
    result = buildconfigurations.list_revisions_of_build_configuration(name='testerino')
    mock_get_config_id.assert_called_once_with(None, 'testerino')
    assert not mock_get_revisions.called
    assert not result


@patch('pnc_cli.buildconfigurations.get_config_id', return_value=1)
@patch('pnc_cli.buildconfigurations.configs_api.get_revision', return_value=MagicMock(content='test-revision'))
def test_get_revision_of_build_configuration_id(mock_get_revision, mock_get_config_id):
    result = buildconfigurations.get_revision_of_build_configuration(id=1, revision_id=1)
    mock_get_config_id.assert_called_once_with(1, None)
    mock_get_revision.assert_called_once_with(id=1, rev=1)
    assert result == 'test-revision'


@patch('pnc_cli.buildconfigurations.get_config_id', return_value=1)
@patch('pnc_cli.buildconfigurations.configs_api.get_revision', return_value=MagicMock(content='test-revision'))
def test_get_revision_of_build_configuration_name(mock_get_revision, mock_get_config_id):
    result = buildconfigurations.get_revision_of_build_configuration(name="testerino", revision_id=1)
    mock_get_config_id.assert_called_once_with(None, 'testerino')
    mock_get_revision.assert_called_once_with(id=1, rev=1)
    assert result == 'test-revision'


@patch('pnc_cli.buildconfigurations.get_config_id', return_value=None)
@patch('pnc_cli.buildconfigurations.configs_api.get_revision')
def test_get_revision_of_build_configuration_notexist(mock_get_revision, mock_get_config_id):
    result = buildconfigurations.get_revision_of_build_configuration(name="testerino", revision_id=1)
    mock_get_config_id.assert_called_once_with(None, 'testerino')
    assert not mock_get_revision.called
    assert not result


@patch('pnc_cli.projects.get_project_id', return_value=1)
@patch('pnc_cli.buildconfigurations.configs_api.get_all_by_project_id', return_value=MagicMock(content=[1, 2, 3]))
def test_list_build_configurations_for_project_id(mock_get_all_by_project_id, mock_get_project_id):
    result = buildconfigurations.list_build_configurations_for_project(id=1)
    mock_get_project_id.assert_called_once_with(1, None)
    mock_get_all_by_project_id.assert_called_once_with(project_id=1)
    assert result == [1, 2, 3]


@patch('pnc_cli.projects.get_project_id', return_value=1)
@patch('pnc_cli.buildconfigurations.configs_api.get_all_by_project_id', return_value=MagicMock(content=[1, 2, 3]))
def test_list_build_configurations_for_project_name(mock_get_all_by_project_id, mock_get_project_id):
    result = buildconfigurations.list_build_configurations_for_project(name='testerino-project')
    mock_get_project_id.assert_called_once_with(None, 'testerino-project')
    mock_get_all_by_project_id.assert_called_once_with(project_id=1)
    assert result == [1, 2, 3]


@patch('pnc_cli.projects.get_project_id', return_value=None)
@patch('pnc_cli.buildconfigurations.configs_api.get_all_by_project_id')
def test_list_build_configurations_for_project_notexist(mock_get_all_by_project_id, mock_get_project_id):
    result = buildconfigurations.list_build_configurations_for_project(name='testerino-project')
    mock_get_project_id.assert_called_once_with(None, 'testerino-project')
    assert not mock_get_all_by_project_id.called
    assert not result


@patch('pnc_cli.buildconfigurations.configs_api.get_all', return_value=MagicMock(content=[1, 2, 3]))
def test_list_build_configurations(mock):
    result = buildconfigurations.list_build_configurations()
    mock.assert_called_once_with()
    assert result == [1, 2, 3]