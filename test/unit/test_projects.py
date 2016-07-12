__author__ = 'Tom'
from mock import MagicMock, patch
import argh
import pytest

import pnc_cli.projects as projects
from pnc_cli.swagger_client import ProjectRest
from pnc_cli.swagger_client import ProjectsApi


def test_create_project_object():
    compare = ProjectRest()
    compare.name = 'test'
    compare.description = 'description'
    result = projects._create_project_object(name='test', description='description')
    assert result.to_dict() == compare.to_dict()


@patch('pnc_cli.projects._create_project_object', return_value='created-project')
@patch('pnc_cli.projects.projects_api.create_new', return_value=MagicMock(content='SUCCESS'))
def test_create_project(mock_create_new, mock_create_project_object):
    result = projects.create_project(name='testerino')
    mock_create_project_object.assert_called_once_with(name='testerino')
    mock_create_new.assert_called_once_with(body='created-project')
    assert result == 'SUCCESS'


def test_update_project_no_modifications():
    with pytest.raises(argh.exceptions.CommandError):
        result = projects.update_project(1)


@patch('pnc_cli.projects.projects_api.get_specific')
@patch('pnc_cli.projects.projects_api.update', return_value='SUCCESS')
def test_update_project(mock_update, mock_get_specific):
    mock = MagicMock()
    mockcontent = MagicMock(content=mock)
    mock_get_specific.return_value = mockcontent
    result = projects.update_project(1, configuration_ids=[1, 2, 3])
    assert mock.configuration_ids == [1, 2, 3]
    mock_get_specific.assert_called_once_with(id=1)
    mock_update.assert_called_once_with(id=1, body=mock)
    assert result == 'SUCCESS'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.projects.projects_api.get_specific', return_value=MagicMock(content='SUCCESS'))
@patch('pnc_cli.projects.projects_api', autospec=ProjectsApi)
def test_get_project_id(mock_projects_api, mock_get_specific, mock_set_id):
    result = projects.get_project(id=1)
    mock_set_id.assert_called_once_with(mock_projects_api, 1, None)
    mock_get_specific.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.projects.projects_api.get_specific', return_value=MagicMock(content='SUCCESS'))
@patch('pnc_cli.projects.projects_api', autospec=ProjectsApi)
def test_get_project_name(mock_projects_api, mock_get_specific, mock_set_id):
    result = projects.get_project(name='testerino')
    mock_set_id.assert_called_once_with(mock_projects_api, None, 'testerino')
    mock_get_specific.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.projects.projects_api.delete_specific', return_value=MagicMock(content='SUCCESS'))
@patch('pnc_cli.projects.projects_api', autospec=ProjectsApi)
def test_delete_project_id(mock_projects_api, mock_delete, mock_set_id):
    result = projects.delete_project(id=1)
    mock_set_id.assert_called_once_with(mock_projects_api, 1, None)
    mock_delete.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.projects.projects_api.delete_specific', return_value=MagicMock(content='SUCCESS'))
@patch('pnc_cli.projects.projects_api', autospec=ProjectsApi)
def test_delete_project_name(mock_projects_api, mock_delete, mock_set_id):
    result = projects.delete_project(name='testerino')
    mock_set_id.assert_called_once_with(mock_projects_api, None, 'testerino')
    mock_delete.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.projects.projects_api.get_all', return_value=MagicMock(content='SUCCESS'))
def test_list_projects(mock):
    result = projects.list_projects()
    mock.assert_called_once_with(page_size=200, q="", sort="")
    assert result == 'SUCCESS'
