import pytest
from argh import CommandError

import test.testutils

__author__ = 'thauser'
from mock import MagicMock, patch, call
from pnc_cli import buildconfigurations
from pnc_cli import common
from pnc_cli.swagger_client import BuildConfigurationRest
from pnc_cli.swagger_client import ProductsApi


def test_create_build_conf_object():
    compare = BuildConfigurationRest()
    compare.name = 'test'
    result = buildconfigurations.create_build_conf_object(name='test')
    assert compare.to_dict() == result.to_dict()


@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.get_specific',
       return_value=MagicMock(content=MagicMock(id=1)))
def test_config_id_exists(mock):
    result = buildconfigurations.config_id_exists(1)
    mock.assert_called_once_with(id=1)
    assert result


@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.get_specific',
       return_value=None)
def test_config_id_exists_false(mock):
    result = buildconfigurations.config_id_exists(5)
    mock.assert_called_once_with(id=5)
    assert not result


@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.get_all')
def test_get_build_configuration_id_by_name(mock):
    mock.return_value = test.testutils.create_mock_list_with_name_attribute()
    result = buildconfigurations.get_build_configuration_id_by_name('testerino')
    mock.assert_called_once_with(q='name==testerino')
    assert result == 1


@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.get_all',
       return_value=MagicMock(content=[]))
def test_get_build_configuration_id_by_name_notexist(mock):
    result = buildconfigurations.get_build_configuration_id_by_name('doesntexist')
    mock.assert_called_once_with(q='name==doesntexist')
    assert not result


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.trigger', return_value=MagicMock(content='buildstarted'))
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs', autospec=True)
def test_build_id(mock_configs_api, mock_trigger, mock_set_id):
    result = buildconfigurations.build_raw(id=1)
    mock_set_id.assert_called_once_with(mock_configs_api, 1, None)
    mock_trigger.assert_called_once_with(id=1, build_dependencies=True, force_rebuild=False, keep_pod_on_failure=False, temporary_build=False, timestamp_alignment=False, rebuild_mode=common.REBUILD_MODES_DEFAULT)
    assert result == 'buildstarted'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.trigger', return_value=MagicMock(content='buildstarted'))
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs', autospec=True)
def test_build_name(mock_configs_api, mock_trigger, mock_set_id):
    result = buildconfigurations.build_raw(name='testerino')
    mock_set_id.assert_called_once_with(mock_configs_api, None, 'testerino')
    mock_trigger.assert_called_once_with(id=1, build_dependencies=True, force_rebuild=False, keep_pod_on_failure=False, temporary_build=False, timestamp_alignment=False, rebuild_mode=common.REBUILD_MODES_DEFAULT)
    assert result == 'buildstarted'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.get_specific', return_value=MagicMock(content='buildconfiguration'))
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs', autospec=True)
def test_get_build_configuration_id(mock_configs_api, mock_get_specific, mock_set_id):
    result = buildconfigurations.get_build_configuration_raw(id=1)
    mock_set_id.assert_called_once_with(mock_configs_api, 1, None)
    mock_get_specific.assert_called_once_with(id=1)
    assert result == 'buildconfiguration'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.get_specific', return_value=MagicMock(content='buildconfiguration'))
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs', autospec=True)
def test_get_build_configuration_id(mock_configs_api, mock_get_specific, mock_set_id):
    result = buildconfigurations.get_build_configuration_raw(name='testerino')
    mock_set_id.assert_called_once_with(mock_configs_api, None, 'testerino')
    mock_get_specific.assert_called_once_with(id=1)
    assert result == 'buildconfiguration'


@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.get_specific')
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.update', return_value=MagicMock(content='SUCCESS'))
@patch('pnc_cli.common.get_entity', return_value='mock-entity')
@patch('pnc_cli.buildconfigurations.pnc_api.projects', autospec=True)
@patch('pnc_cli.buildconfigurations.pnc_api.environments', autospec=True)
def test_update_build_configuration(mock_envs_api, mock_projects_api, mock_entity, mock_update, mock_get_specific):
    mock = MagicMock()
    mockcontent = MagicMock(content=mock)
    mock_get_specific.return_value = mockcontent
    result = buildconfigurations.update_build_configuration_raw(id=1, build_script='mvn install', project=1, environment=1)
    mock_entity.assert_has_calls([call(mock_projects_api, 1), call(mock_envs_api, 1)])
    mock_get_specific.assert_called_once_with(id=1)
    # object returned by get_specific is appropriately modified
    assert getattr(mock, 'build_script') == 'mvn install'
    mock_update.assert_called_once_with(id=1, body=mock)
    assert result == 'SUCCESS'


@patch('pnc_cli.buildconfigurations.create_build_conf_object', return_value='test-build-config-object')
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.create_new', return_value=MagicMock(content='test-build-config-object'))
@patch('pnc_cli.common.get_entity', return_value='mock-entity')
@patch('pnc_cli.buildconfigurations.pnc_api.projects', autospec=True)
@patch('pnc_cli.buildconfigurations.pnc_api.environments', autospec=True)
@patch('pnc_cli.buildconfigurations.pnc_api.repositories', autospec=True)
def test_create_build_configuration(mock_repos_api, mock_projects_api, mock_envs_api, mock_entity, mock_create_new,
                                    mock_create_build_conf_object):
    result = buildconfigurations.create_build_configuration_raw(name='testerino', description='test description', project=1,
                                                            environment=1, repository_configuration=1)
    mock_create_build_conf_object.assert_called_once_with(name='testerino', description='test description',
                                                          project='mock-entity', environment='mock-entity',
                                                          repository_configuration="mock-entity")
    mock_entity.assert_has_calls([call(mock_envs_api, 1), call(mock_repos_api, 1), call(mock_projects_api, 1)])
    mock_create_new.assert_called_once_with(body='test-build-config-object')
    assert result == 'test-build-config-object'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurations.list_build_configurations_raw', return_value=[])
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.delete_specific', return_value=MagicMock(content=True))
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs', autospec=True)
def test_delete_build_configuration_id(mock_configs_api, mock_delete_specific, mock_list_configs, mock_set_id):
    result = buildconfigurations.delete_build_configuration_raw(id=1)
    mock_set_id.assert_called_once_with(mock_configs_api, 1, None)
    mock_list_configs.assert_called_once_with(page_size=1000000000)
    mock_delete_specific.assert_called_once_with(id=1)
    assert result


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurations.list_build_configurations_raw', return_value=[])
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.delete_specific', return_value=MagicMock(content=True))
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs', autospec=True)
def test_delete_build_configuration_name(mock_configs_api, mock_delete_specific, mock_list_configs, mock_set_id):
    result = buildconfigurations.delete_build_configuration_raw(name='testerino')
    mock_set_id.assert_called_once_with(mock_configs_api, None, 'testerino')
    mock_list_configs.assert_called_once_with(page_size=1000000000)
    mock_delete_specific.assert_called_once_with(id=1)
    assert result


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurations.list_build_configurations_raw', return_value=[MagicMock(dependency_ids=[1])])
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.delete_specific', return_value=MagicMock(content=True))
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs', autospec=True)
def test_delete_build_configuration_hasdep(mock_configs_api, mock_delete_specific, mock_list_configs, mock_set_id):
    with pytest.raises(CommandError):
        result = buildconfigurations.delete_build_configuration_raw(id='1')
    mock_set_id.assert_called_once_with(mock_configs_api, '1', None)
    mock_list_configs.assert_called_once_with(page_size=1000000000)
    mock_delete_specific.assert_not_called



@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.get_all_by_product_id', return_value=MagicMock(content=[1, 2, 3]))
@patch('pnc_cli.buildconfigurations.pnc_api.products', autospec=True)
def test_list_build_configurations_for_product_id(mock_products_api, mock_get_all_by_product_id, mock_set_id):
    result = buildconfigurations.list_build_configurations_for_product_raw(id=1)
    mock_set_id.called_once_with(mock_products_api, 1, None)
    mock_get_all_by_product_id.called_once_with(product_id=1, page_index=0, page_size=200, sort="", q="")
    assert result == [1, 2, 3]


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.get_all_by_product_id', return_value=MagicMock(content=[1, 2, 3]))
@patch('pnc_cli.buildconfigurations.pnc_api.products', autospec=True)
def test_list_build_configurations_for_product_name(mock_products_api, mock_get_all_by_product_id, mock_set_id):
    result = buildconfigurations.list_build_configurations_for_product_raw(name='testerino')
    mock_set_id.called_once_with(mock_products_api, None, 'testerino')
    mock_get_all_by_product_id.called_once_with(product_id=1)
    assert result == [1, 2, 3]


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.get_all_by_product_version_id',
       return_value=MagicMock(content=[1, 2, 3]))
@patch('pnc_cli.buildconfigurations.pnc_api.products', autospec=ProductsApi)
def test_list_build_configurations_for_product_version(mock_products_api, mock_get_all_by_product_version_id,
                                                       mock_set_id):
    result = buildconfigurations.list_build_configurations_for_product_version_raw(product_id=1, version_id=2)
    mock_set_id.assert_called_once_with(mock_products_api, 1, None)
    mock_get_all_by_product_version_id.assert_called_once_with(product_id=1, version_id=2, page_index=0, page_size=200, sort="", q="")
    assert result == [1, 2, 3]


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.get_dependencies', return_value=MagicMock(content=['dep1', 'dep2']))
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs', autospec=True)
def test_list_dependencies_id(mock_configs_api, mock_get_dependencies, mock_set_id):
    result = buildconfigurations.list_dependencies_raw(id=1)
    mock_set_id.assert_called_once_with(mock_configs_api, 1, None)
    mock_get_dependencies.assert_called_once_with(id=1, page_index=0, page_size=200, sort="", q="")
    assert result == ['dep1', 'dep2']


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.get_dependencies', return_value=MagicMock(content=['dep1', 'dep2']))
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs', autospec=True)
def test_list_dependencies_name(mock_configs_api, mock_get_dependencies, mock_set_id):
    result = buildconfigurations.list_dependencies_raw(name='testerino')
    mock_set_id.assert_called_once_with(mock_configs_api, None, 'testerino')
    mock_get_dependencies.assert_called_once_with(id=1, page_index=0, page_size=200, sort="", q="")
    assert result == ['dep1', 'dep2']


@patch('pnc_cli.common.set_id', side_effect=[1, 2])
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.get_specific', return_value=MagicMock(content='added-dep'))
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.add_dependency', return_value=MagicMock(content='SUCCESS'))
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs', autospec=True)
def test_add_dependency_ids(mock_configs_api, mock_add_dependency, mock_get_specific, mock_set_id):
    result = buildconfigurations.add_dependency_raw(id=1, dependency_id=2)
    calls = [call(mock_configs_api, 1, None), call(mock_configs_api, 2, None)]
    mock_set_id.assert_has_calls(calls)
    mock_get_specific.assert_called_once_with(id=2)
    mock_add_dependency.assert_called_once_with(id=1, body='added-dep')
    assert result == 'SUCCESS'


@patch('pnc_cli.common.set_id', side_effect=[1, 2])
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.get_specific', return_value=MagicMock(content='added-dep'))
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.add_dependency', return_value=MagicMock(content='SUCCESS'))
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs', autospec=True)
def test_add_dependency_id_name(mock_configs_api, mock_add_dependency, mock_get_specific, mock_set_id):
    result = buildconfigurations.add_dependency_raw(id=1, dependency_name='testerino')
    calls = [call(mock_configs_api, 1, None), call(mock_configs_api, None, 'testerino')]
    mock_set_id.assert_has_calls(calls)
    mock_get_specific.assert_called_once_with(id=2)
    mock_add_dependency.assert_called_once_with(id=1, body='added-dep')
    assert result == 'SUCCESS'


@patch('pnc_cli.common.set_id', side_effect=[1, 2])
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.get_specific', return_value=MagicMock(content='added-dep'))
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.add_dependency', return_value=MagicMock(content='SUCCESS'))
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs', autospec=True)
def test_add_dependency_name_id(mock_configs_api, mock_add_dependency, mock_get_specific, mock_set_id):
    result = buildconfigurations.add_dependency_raw(name='testerino', dependency_id=2)
    calls = [call(mock_configs_api, None, 'testerino'), call(mock_configs_api, 2, None)]
    mock_set_id.assert_has_calls(calls)
    mock_get_specific.assert_called_once_with(id=2)
    mock_add_dependency.assert_called_once_with(id=1, body='added-dep')
    assert result == 'SUCCESS'


@patch('pnc_cli.common.set_id', side_effect=[1, 2])
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.get_specific', return_value=MagicMock(content='added-dep'))
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.add_dependency', return_value=MagicMock(content='SUCCESS'))
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs', autospec=True)
def test_add_dependency_names(mock_configs_api, mock_add_dependency, mock_get_specific, mock_set_id):
    result = buildconfigurations.add_dependency_raw(name='testerino', dependency_name='testerino2')
    calls = [call(mock_configs_api, None, 'testerino'), call(mock_configs_api, None, 'testerino2')]
    mock_set_id.assert_has_calls(calls)
    mock_get_specific.assert_called_once_with(id=2)
    mock_add_dependency.assert_called_once_with(id=1, body='added-dep')
    assert result == 'SUCCESS'


@patch('pnc_cli.common.set_id', side_effect=[1, 2])
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.remove_dependency', return_value=MagicMock(content='SUCCESS'))
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs', autospec=True)
def test_remove_dependency_ids(mock_configs_api, mock_remove_dependency, mock_set_id):
    result = buildconfigurations.remove_dependency_raw(id=1, dependency_id=2)
    calls = [call(mock_configs_api, 1, None), call(mock_configs_api, 2, None)]
    mock_set_id.assert_has_calls(calls)
    mock_remove_dependency.assert_called_once_with(id=1, dependency_id=2)
    assert result == 'SUCCESS'


@patch('pnc_cli.common.set_id', side_effect=[1, 2])
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.remove_dependency', return_value=MagicMock(content='SUCCESS'))
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs', autospec=True)
def test_remove_dependency_id_name(mock_configs_api, mock_remove_dependency, mock_set_id):
    result = buildconfigurations.remove_dependency_raw(id=1, dependency_name='testerino')
    calls = [call(mock_configs_api, 1, None), call(mock_configs_api, None, 'testerino')]
    mock_set_id.assert_has_calls(calls)
    mock_remove_dependency.assert_called_once_with(id=1, dependency_id=2)
    assert result == 'SUCCESS'


@patch('pnc_cli.common.set_id', side_effect=[1, 2])
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.remove_dependency', return_value=MagicMock(content='SUCCESS'))
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs', autospec=True)
def test_remove_dependency_name_id(mock_configs_api, mock_remove_dependency, mock_set_id):
    result = buildconfigurations.remove_dependency_raw(name='testerino', dependency_id=2)
    calls = [call(mock_configs_api, None, 'testerino'), call(mock_configs_api, 2, None)]
    mock_set_id.assert_has_calls(calls)
    mock_remove_dependency.assert_called_once_with(id=1, dependency_id=2)
    assert result == 'SUCCESS'


@patch('pnc_cli.common.set_id', side_effect=[1, 2])
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.remove_dependency', return_value=MagicMock(content='SUCCESS'))
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs', autospec=True)
def test_remove_dependency_names(mock_configs_api, mock_remove_dependency, mock_set_id):
    result = buildconfigurations.remove_dependency_raw(name='testerino', dependency_name='testerino')
    calls = [call(mock_configs_api, None, 'testerino'), call(mock_configs_api, None, 'testerino')]
    mock_set_id.assert_has_calls(calls)
    mock_remove_dependency.assert_called_once_with(id=1, dependency_id=2)
    assert result == 'SUCCESS'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.get_product_versions', return_value=MagicMock(content=[1, 2, 3]))
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs', autospec=True)
def test_list_product_versions_for_build_configuration_id(mock_configs_api, mock_get_product_versions, mock_set_id):
    result = buildconfigurations.list_product_versions_for_build_configuration_raw(id=1)
    mock_set_id.assert_called_once_with(mock_configs_api, 1, None)
    mock_get_product_versions.assert_called_once_with(id=1, page_index=0, page_size=200, sort="", q="")
    assert result == [1, 2, 3]


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.get_product_versions', return_value=MagicMock(content=[1, 2, 3]))
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs', autospec=True)
def test_list_product_versions_for_build_configuration_name(mock_configs_api, mock_get_product_versions, mock_set_id):
    result = buildconfigurations.list_product_versions_for_build_configuration_raw(name='testerino')
    mock_set_id.assert_called_once_with(mock_configs_api, None, 'testerino')
    mock_get_product_versions.assert_called_once_with(id=1, page_index=0, page_size=200, sort="", q="")
    assert result == [1, 2, 3]


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.common.get_entity', return_value='productversion')
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.add_product_version', return_value=MagicMock(content='testresponse'))
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs', autospec=True)
@patch('pnc_cli.buildconfigurations.pnc_api.product_versions', autospec=True)
def test_add_product_version_to_build_configuration_id(mock_versions_api,
                                                       mock_configs_api,
                                                       mock_add_product_version,
                                                       mock_get_entity,
                                                       mock_set_id):
    result = buildconfigurations.add_product_version_to_build_configuration_raw(id=1, product_version_id=2)
    mock_set_id.assert_called_once_with(mock_configs_api, 1, None)
    mock_get_entity.assert_called_once_with(mock_versions_api, 2)
    mock_add_product_version.assert_called_once_with(id=1, body='productversion')
    assert result == 'testresponse'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.common.get_entity', return_value='productversion')
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.add_product_version', return_value=MagicMock(content='testresponse'))
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs', autospec=True)
@patch('pnc_cli.buildconfigurations.pnc_api.product_versions', autospec=True)
def test_add_product_version_to_build_configuration_name(mock_versions_api,
                                                         mock_configs_api,
                                                         mock_add_product_version,
                                                         mock_get_entity,
                                                         mock_set_id):
    result = buildconfigurations.add_product_version_to_build_configuration_raw(name='testerino', product_version_id=2)
    mock_set_id.assert_called_once_with(mock_configs_api, None, 'testerino')
    mock_get_entity.assert_called_once_with(mock_versions_api, 2)
    mock_add_product_version.assert_called_once_with(id=1, body='productversion')
    assert result == 'testresponse'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.remove_product_version', return_value=MagicMock(content='SUCCESS'))
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs', autospec=True)
def test_remove_product_version_from_build_configuration_id(mock_configs_api,
                                                            mock_remove_product_version,
                                                            mock_set_id):
    result = buildconfigurations.remove_product_version_from_build_configuration_raw(id=1, product_version_id=1)
    mock_set_id.assert_called_once_with(mock_configs_api, 1, None)
    mock_remove_product_version.assert_called_once_with(id=1, product_version_id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.remove_product_version', return_value=MagicMock(content='SUCCESS'))
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs', autospec=True)
def test_remove_product_version_from_build_configuration_name(mock_configs_api,
                                                              mock_remove_product_version,
                                                              mock_set_id):
    result = buildconfigurations.remove_product_version_from_build_configuration_raw(name='testerino', product_version_id=1)
    mock_set_id.assert_called_once_with(mock_configs_api, None, 'testerino')
    mock_remove_product_version.assert_called_once_with(id=1, product_version_id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.get_revisions', return_value=MagicMock(content=['rev1', 'rev2']))
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs', autospec=True)
def test_list_revisions_of_build_configuration_id(mock_configs_api, mock_get_revisions, mock_set_id):
    result = buildconfigurations.list_revisions_of_build_configuration_raw(id=1)
    mock_set_id.assert_called_once_with(mock_configs_api, 1, None)
    mock_get_revisions.assert_called_once_with(id=1, page_index=0, page_size=200, sort="")
    assert result == ['rev1', 'rev2']


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.get_revisions', return_value=MagicMock(content=['rev1', 'rev2']))
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs', autospec=True)
def test_list_revisions_of_build_configuration(mock_configs_api, mock_get_revisions, mock_set_id):
    result = buildconfigurations.list_revisions_of_build_configuration_raw(name='testerino')
    mock_set_id.assert_called_once_with(mock_configs_api, None, 'testerino')
    mock_get_revisions.assert_called_once_with(id=1, page_index=0, page_size=200, sort="")
    assert result == ['rev1', 'rev2']


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.get_revision', return_value=MagicMock(content='test-revision'))
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs', autospec=True)
def test_get_revision_of_build_configuration_id(mock_configs_api, mock_get_revision, mock_set_id):
    result = buildconfigurations.get_revision_of_build_configuration_raw(id=1, revision_id=1)
    mock_set_id.assert_called_once_with(mock_configs_api, 1, None)
    mock_get_revision.assert_called_once_with(id=1, rev=1)
    assert result == 'test-revision'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.get_revision', return_value=MagicMock(content='test-revision'))
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs', autospec=True)
def test_get_revision_of_build_configuration_name(mock_configs_api, mock_get_revision, mock_set_id):
    result = buildconfigurations.get_revision_of_build_configuration_raw(name="testerino", revision_id=1)
    mock_set_id.assert_called_once_with(mock_configs_api, None, 'testerino')
    mock_get_revision.assert_called_once_with(id=1, rev=1)
    assert result == 'test-revision'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.get_all_by_project_id', return_value=MagicMock(content=[1, 2, 3]))
@patch('pnc_cli.buildconfigurations.pnc_api.projects', autospec=True)
def test_list_build_configurations_for_project_id(mock_projects_api, mock_get_all_by_project_id, mock_set_id):
    result = buildconfigurations.list_build_configurations_for_project_raw(id=1)
    mock_set_id.assert_called_once_with(mock_projects_api, 1, None)
    mock_get_all_by_project_id.assert_called_once_with(project_id=1, page_index=0, page_size=200, sort="", q="")
    assert result == [1, 2, 3]


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.get_all_by_project_id', return_value=MagicMock(content=[1, 2, 3]))
@patch('pnc_cli.buildconfigurations.pnc_api.projects', autospec=True)
def test_list_build_configurations_for_project_name(mock_projects_api, mock_get_all_by_project_id, mock_set_id):
    result = buildconfigurations.list_build_configurations_for_project_raw(name='testerino-project')
    mock_set_id.assert_called_once_with(mock_projects_api, None, 'testerino-project')
    mock_get_all_by_project_id.assert_called_once_with(project_id=1, page_index=0, page_size=200, sort="", q="")
    assert result == [1, 2, 3]


@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.get_all', return_value=MagicMock(content=[1, 2, 3]))
def test_list_build_configurations(mock):
    result = buildconfigurations.list_build_configurations_raw()
    mock.assert_called_once_with(page_index=0, page_size=200, sort="", q="")
    assert result == [1, 2, 3]


@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.trigger_audited', return_value=MagicMock(content='SUCCESS'))
def test_build_a_revision(mock_trigger_audited):
    result = buildconfigurations.build_raw(1, revision=2, temporary_build=True, force_rebuild=True)
    mock_trigger_audited.assert_called_once_with(id=1, rev=2, temporary_build=True, force_rebuild=True,
                                                 timestamp_alignment=False, build_dependencies=True,
                                                 keep_pod_on_failure=False, rebuild_mode=common.REBUILD_MODES_DEFAULT)
    assert result == 'SUCCESS'


@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.get_specific')
@patch('pnc_cli.buildconfigurations.pnc_api.build_configs.update_and_get_audited', return_value=MagicMock(content='SUCCESS'))
@patch('pnc_cli.common.get_entity', return_value='mock-entity')
@patch('pnc_cli.buildconfigurations.pnc_api.projects', autospec=True)
@patch('pnc_cli.buildconfigurations.pnc_api.environments', autospec=True)
def test_update_and_get_audited(mock_envs_api, mock_projects_api, mock_entity, mock_update, mock_get_specific):
    mock = MagicMock()
    mockcontent = MagicMock(content=mock)
    mock_get_specific.return_value = mockcontent
    result = buildconfigurations.update_build_configuration_raw(id=1, build_script='mvn install', project=1, environment=1, get_revision=True)
    mock_entity.assert_has_calls([call(mock_projects_api, 1), call(mock_envs_api, 1)])
    mock_get_specific.assert_called_once_with(id=1)
    # object returned by get_specific is appropriately modified
    assert getattr(mock, 'build_script') == 'mvn install'
    mock_update.assert_called_once_with(id=1, body=mock)
    assert result == 'SUCCESS'
