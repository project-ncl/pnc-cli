import argparse

import pytest

__author__ = 'thauser'
from mock import MagicMock, patch

from pnc_cli import environments
from pnc_cli.swagger_client import EnvironmentsApi


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.environments.envs_api.get_specific', return_value=MagicMock(content='buildenvironment1'))
@patch('pnc_cli.environments.envs_api', autospec=EnvironmentsApi)
def test_get_environment_id(mock_envs_api, mock_get_specific, mock_set_id):
    result = environments.get_environment_raw(id=1)
    mock_set_id.assert_called_once_with(mock_envs_api, 1, None)
    mock_get_specific.assert_called_once_with(id=1)
    assert result == 'buildenvironment1'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.environments.envs_api.get_specific', return_value=MagicMock(content='buildenvironment1'))
@patch('pnc_cli.environments.envs_api', autospec=EnvironmentsApi)
def test_get_environment_name(mock_envs_api, mock_get_specific, mock_set_id):
    result = environments.get_environment_raw(name='testerino')
    mock_set_id.assert_called_once_with(mock_envs_api, None, 'testerino')
    mock_get_specific.assert_called_once_with(id=1)
    assert result == 'buildenvironment1'


@patch('pnc_cli.environments.envs_api.get_all', return_value=MagicMock(content=['env1', 'env2', 'env3']))
def test_list_environments(mock):
    result = environments.list_environments_raw()
    mock.assert_called_once_with(page_index=0, page_size=200, q="", sort="")
    assert result == ['env1', 'env2', 'env3']
