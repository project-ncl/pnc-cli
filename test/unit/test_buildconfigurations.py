__author__ = 'thauser'
from mock import MagicMock, patch
from pnc_cli import buildconfigurations

@patch('pnc_cli.buildconfigurations.get_config_id', return_value=1)
@patch('pnc_cli.buildconfigurations.configs_api.trigger', return_value=MagicMock(content='buildstarted'))
def test_build_id(mock_trigger,mock_get_config_id):
    result = buildconfigurations.build(id=1)
    mock_get_config_id.assert_called_once_with(1,None)
    mock_trigger.assert_called_once_with(id=1)
    assert result == 'buildstarted'

@patch('pnc_cli.buildconfigurations.get_config_id', return_value=1)
@patch('pnc_cli.buildconfigurations.configs_api.trigger', return_value=MagicMock(content='buildstarted'))
def test_build_name(mock_trigger, mock_get_config_id):
    result = buildconfigurations.build(name='testerino')
    mock_get_config_id.assert_called_once_with(None,'testerino')
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
    mock_get_config_id.assert_called_once_with(1,None)
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
    mock_get_config_id.assert_called_once_with(1,None)
    assert not mock_get_specific.called
    assert not result

@patch('pnc_cli.buildconfigurations.get_config_id', return_value=1)
@patch('pnc_cli.buildconfigurations.configs_api.get_specific', return_value=MagicMock(content=buildconfigurations.create_build_conf_object(build_script='testerino')))
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
@patch('pnc_cli.buildconfigurations.configs_api.get_specific', return_value=MagicMock(content=buildconfigurations.create_build_conf_object(build_script='testerino')))
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
    mock_get_config_id.assert_called_once_with(1,None)
    mock_delete_specific.assert_called_once_with(id=1)
    assert result

@patch('pnc_cli.buildconfigurations.get_config_id', return_value=1)
@patch('pnc_cli.buildconfigurations.configs_api.delete_specific', return_value=MagicMock(content=True))
def test_delete_build_configuration_name(mock_delete_specific, mock_get_config_id):
    result = buildconfigurations.delete_build_configuration(name='testerino')
    mock_get_config_id.assert_called_once_with(None,'testerino')
    mock_delete_specific.assert_called_once_with(id=1)
    assert result

@patch('pnc_cli.buildconfigurations.get_config_id', return_value=None)
@patch('pnc_cli.buildconfigurations.configs_api.delete_specific')
def test_delete_build_configuration_notexist(mock_delete_specific, mock_get_config_id):
    result = buildconfigurations.delete_build_configuration(name='testerino')
    mock_get_config_id.assert_called_once_with(None, 'testerino')
    assert not mock_delete_specific.called
    assert not result


def test_list_build_configurations_for_product():
    pass

def test_list_build_configurations_for_product_version():
    pass

def test_list_dependencies():
    pass

def test_add_dependency():
    pass

def test_remove_dependency():
    pass

def test_list_product_versions_for_build_configuration():
    pass

def test_add_product_version_to_build_configuration():
    pass

def test_remove_product_version_from_build_configuration():
    pass

def test_list_revisions_of_build_configuration():
    pass

@patch('pnc_cli.buildconfigurations.get_config_id', return_value=1)
@patch('pnc_cli.buildconfigurations.configs_api.get_revision', return_value=MagicMock(content='test-revision'))
def test_get_revision_of_build_configuration_id(mock_get_revision, mock_get_config_id):
    result = buildconfigurations.get_revision_of_build_configuration(id=1,revision_id=1)
    mock_get_config_id.assert_called_once_with(1, None)
    mock_get_revision.assert_called_once_with(id=1, rev=1)
    assert result == 'test-revision'

@patch('pnc_cli.buildconfigurations.get_config_id', return_value=1)
@patch('pnc_cli.buildconfigurations.configs_api.get_revision', return_value=MagicMock(content='test-revision'))
def test_get_revision_of_build_configuration_name(mock_get_revision, mock_get_config_id):
    result = buildconfigurations.get_revision_of_build_configuration(name="testerino", revision_id=1)
    mock_get_config_id.assert_called_once_with(None,'testerino')
    mock_get_revision.assert_called_once_with(id=1,rev=1)
    assert result == 'test-revision'

@patch('pnc_cli.buildconfigurations.get_config_id', return_value=None)
@patch('pnc_cli.buildconfigurations.configs_api.get_revision')
def test_get_revision_of_build_configuration_notexist(mock_get_revision, mock_get_config_id):
    result = buildconfigurations.get_revision_of_build_configuration(name="testerino", revision_id=1)
    mock_get_config_id.assert_called_once_with(None,'testerino')
    assert not mock_get_revision.called
    assert not result

@patch('pnc_cli.projects.get_project_id', return_value=1)
@patch('pnc_cli.buildconfigurations.configs_api.get_all_by_project_id', return_value=MagicMock(content=[1,2,3]))
def test_list_build_configurations_for_project_id(mock_get_all_by_project_id, mock_get_project_id):
    result = buildconfigurations.list_build_configurations_for_project(id=1)
    mock_get_project_id.assert_called_once_with(1, None)
    mock_get_all_by_project_id.assert_called_once_with(project_id=1)
    assert result == [1,2,3]

@patch('pnc_cli.projects.get_project_id', return_value=1)
@patch('pnc_cli.buildconfigurations.configs_api.get_all_by_project_id', return_value=MagicMock(content=[1,2,3]))
def test_list_build_configurations_for_project_name(mock_get_all_by_project_id, mock_get_project_id):
    result = buildconfigurations.list_build_configurations_for_project(name='testerino-project')
    mock_get_project_id.assert_called_once_with(None, 'testerino-project')
    mock_get_all_by_project_id.assert_called_once_with(project_id=1)
    assert result == [1,2,3]

@patch('pnc_cli.projects.get_project_id', return_value=None)
@patch('pnc_cli.buildconfigurations.configs_api.get_all_by_project_id')
def test_list_build_configurations_for_project_notexist(mock_get_all_by_project_id, mock_get_project_id):
    result = buildconfigurations.list_build_configurations_for_project(name='testerino-project')
    mock_get_project_id.assert_called_once_with(None, 'testerino-project')
    assert not mock_get_all_by_project_id.called
    assert not result

@patch('pnc_cli.buildconfigurations.configs_api.get_all', return_value=MagicMock(content=[1,2,3]))
def test_list_build_configurations(mock):
    result = buildconfigurations.list_build_configurations()
    mock.assert_called_once_with()
    assert result == [1,2,3]