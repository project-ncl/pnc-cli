__author__ = 'Tom'
from mock import MagicMock, patch
from pnc_cli import projects
from pnc_cli.swagger_client import ProjectRest
from test import testutils


def test_create_project_object():
    compare = ProjectRest()
    compare.name = 'test'
    compare.description = 'description'
    result = projects._create_project_object(name='test', description='description')
    assert result.to_dict() == compare.to_dict()


@patch('pnc_cli.projects._project_exists', return_value=True)
def test_get_project_id_id(mock):
    result = projects.get_project_id(1, None)
    mock.assert_called_once_with(1)
    assert result == 1


@patch('pnc_cli.projects._project_exists', return_value=False)
def test_get_project_id_notexist(mock):
    result = projects.get_project_id(1, None)
    mock.assert_called_once_with(1)
    assert not result


@patch('pnc_cli.projects._get_project_id_by_name', return_value=1)
def test_get_project_id_name(mock):
    result = projects.get_project_id(None, 'testerino')
    mock.assert_called_once_with('testerino')
    assert result == 1


@patch('pnc_cli.projects._get_project_id_by_name', return_value=None)
def test_get_project_id_name_notexist(mock):
    result = projects.get_project_id(None, 'testerino')
    mock.assert_called_once_with('testerino')
    assert not result


def test_get_project_id_none():
    result = projects.get_project_id(None, None)
    assert not result


@patch('pnc_cli.projects.projects_api.get_all', return_value=testutils.create_mock_list_with_name_attribute())
def test_get_project_id_by_name(mock):
    result = projects._get_project_id_by_name('testerino')
    mock.assert_called_once_with()
    assert result == 1


@patch('pnc_cli.projects.projects_api.get_all', return_value=testutils.create_mock_list_with_name_attribute())
def test_get_project_id_by_name_notexist(mock):
    result = projects._get_project_id_by_name('doesntexist')
    mock.assert_called_once_with()
    assert not result


@patch('pnc_cli.projects.projects_api.get_all', return_value=MagicMock(content=[MagicMock(id=1), MagicMock(id=2)]))
def test_project_exists(mock):
    result = projects._project_exists(1)
    mock.assert_called_once_with()
    assert result


@patch('pnc_cli.projects.projects_api.get_all', return_value=MagicMock(content=[MagicMock(id=1), MagicMock(id=2)]))
def test_project_exists_notexist(mock):
    result = projects._project_exists(10)
    mock.assert_called_once_with()
    assert not result


@patch('pnc_cli.projects._create_project_object', return_value='created-project')
@patch('pnc_cli.projects.projects_api.create_new', return_value=MagicMock(content='SUCCESS'))
def test_create_project(mock_create_new, mock_create_project_object):
    result = projects.create_project(name='testerino')
    mock_create_project_object.assert_called_once_with(name='testerino')
    mock_create_new.assert_called_once_with(body='created-project')
    assert result == 'SUCCESS'


@patch('pnc_cli.projects.projects_api.get_specific')
@patch('pnc_cli.projects.projects_api.update', return_value=MagicMock(content='SUCCESS'))
def test_update_project(mock_update, mock_get_specific):
    mock = MagicMock()
    mockcontent = MagicMock(content=mock)
    mock_get_specific.return_value = mockcontent
    result = projects.update_project(1, configuration_ids=[1, 2, 3])
    assert mock.configuration_ids == [1, 2, 3]
    mock_get_specific.assert_called_once_with(id=1)
    mock_update.assert_called_once_with(id=1, body=mock)
    assert result == 'SUCCESS'


@patch('pnc_cli.projects.get_project_id', return_value=1)
@patch('pnc_cli.projects.projects_api.get_specific', return_value=MagicMock(content='SUCCESS'))
def test_get_project_id(mock_get_specific, mock_get_project_id):
    result = projects.get_project(id=1)
    mock_get_project_id.assert_called_once_with(1, None)
    mock_get_specific.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.projects.get_project_id', return_value=1)
@patch('pnc_cli.projects.projects_api.get_specific', return_value=MagicMock(content='SUCCESS'))
def test_get_project_name(mock_get_specific, mock_get_project_id):
    result = projects.get_project(name='testerino')
    mock_get_project_id.assert_called_once_with(None, 'testerino')
    mock_get_specific.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.projects.get_project_id', return_value=None)
@patch('pnc_cli.projects.projects_api.get_specific')
def test_get_project_notexist(mock_get_specific, mock_get_project_id):
    result = projects.get_project(name='testerino')
    mock_get_project_id.assert_called_once_with(None, 'testerino')
    assert not mock_get_specific.called
    assert not result


@patch('pnc_cli.projects.get_project_id', return_value=1)
@patch('pnc_cli.projects.projects_api.delete_specific', return_value=MagicMock(content='SUCCESS'))
def test_delete_project_id(mock_delete, mock_get_project_id):
    result = projects.delete_project(id=1)
    mock_get_project_id.assert_called_once_with(1, None)
    mock_delete.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.projects.get_project_id', return_value=1)
@patch('pnc_cli.projects.projects_api.delete_specific', return_value=MagicMock(content='SUCCESS'))
def test_delete_project_name(mock_delete, mock_get_project_id):
    result = projects.delete_project(name='testerino')
    mock_get_project_id.assert_called_once_with(None, 'testerino')
    mock_delete.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.projects.get_project_id', return_value=None)
@patch('pnc_cli.projects.projects_api.delete_specific')
def test_delete_project_notexist(mock_delete, mock_get_project_id):
    result = projects.delete_project(name='testerino')
    mock_get_project_id.assert_called_once_with(None, 'testerino')
    assert not mock_delete.called
    assert not result


@patch('pnc_cli.projects.projects_api.get_all', return_value=MagicMock(content='SUCCESS'))
def test_list_projects(mock):
    result = projects.list_projects()
    mock.assert_called_once_with(page_size=200, q="", sort="")
    assert result == 'SUCCESS'
