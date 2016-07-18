__author__ = 'thauser'
from mock import MagicMock, patch

from pnc_cli import environments
from pnc_cli.swagger_client import BuildEnvironmentRest
from pnc_cli.swagger_client import EnvironmentsApi


def test_create_environment_object():
    compare = BuildEnvironmentRest()
    compare.build_type = 'JAVA'
    compare.name = 'test-environment'
    result = environments.create_environment_object(name='test-environment', build_type='java')
    assert result.to_dict() == compare.to_dict()


@patch('pnc_cli.environments.create_environment_object', return_value='test-environment-object')
@patch('pnc_cli.environments.envs_api.create_new', return_value=MagicMock(content='buildenvironment1'))
def test_create_environment(mock_create_new, mock_create_environment_object):
    result = environments.create_environment(name='testerino', build_type='JAVA', attributes='test=test')
    mock_create_environment_object.assert_called_once_with(name='testerino', build_type='JAVA', attributes='test=test')
    mock_create_new.assert_called_once_with(body='test-environment-object')
    assert result == 'buildenvironment1'


@patch('pnc_cli.environments.envs_api.get_specific')
@patch('pnc_cli.environments.envs_api.update', return_value=MagicMock(content='buildenvironment1'))
def test_update_environment(mock_update, mock_get_specific):
    mock = MagicMock()
    mockcontent = MagicMock(content=mock)
    mock_get_specific.return_value = mockcontent
    result = environments.update_environment(id=1, name='testerino2', build_type='JAVA', attributes='test=test')
    mock_get_specific.assert_called_once_with(id=1)
    mock_update.assert_called_once_with(id=1, body=mock)
    assert getattr(mock, 'build_type') == 'JAVA'
    assert result == 'buildenvironment1'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.environments.envs_api.delete', return_value=True)
@patch('pnc_cli.environments.envs_api', autospec=EnvironmentsApi)
def test_delete_environment_id(mock_envs_api, mock_delete, mock_set_id):
    result = environments.delete_environment(id=1)
    mock_set_id.assert_called_once_with(mock_envs_api, 1, None)
    mock_delete.assert_called_once_with(id=1)
    assert result


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.environments.envs_api.delete', return_value=True)
@patch('pnc_cli.environments.envs_api', autospec=EnvironmentsApi)
def test_delete_environment_name(mock_envs_api, mock_delete, mock_set_id):
    result = environments.delete_environment(name='testenv')
    mock_set_id.assert_called_once_with(mock_envs_api, None, 'testenv')
    mock_delete.assert_called_once_with(id=1)
    assert result


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.environments.envs_api.get_specific', return_value=MagicMock(content='buildenvironment1'))
@patch('pnc_cli.environments.envs_api', autospec=EnvironmentsApi)
def test_get_environment_id(mock_envs_api, mock_get_specific, mock_set_id):
    result = environments.get_environment(id=1)
    mock_set_id.assert_called_once_with(mock_envs_api, 1, None)
    mock_get_specific.assert_called_once_with(id=1)
    assert result == 'buildenvironment1'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.environments.envs_api.get_specific', return_value=MagicMock(content='buildenvironment1'))
@patch('pnc_cli.environments.envs_api', autospec=EnvironmentsApi)
def test_get_environment_name(mock_envs_api, mock_get_specific, mock_set_id):
    result = environments.get_environment(name='testerino')
    mock_set_id.assert_called_once_with(mock_envs_api, None, 'testerino')
    mock_get_specific.assert_called_once_with(id=1)
    assert result == 'buildenvironment1'


@patch('pnc_cli.environments.envs_api.get_all', return_value=MagicMock(content=['env1', 'env2', 'env3']))
def test_list_environments(mock):
    result = environments.list_environments()
    mock.assert_called_once_with(page_size=200, q="", sort="")
    assert result == ['env1', 'env2', 'env3']
