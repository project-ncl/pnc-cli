import argh
from mock import MagicMock, patch, create_autospec
# used for mock's autospec
import pytest
from pnc_cli.swagger_client import BuildconfigurationsApi

import pnc_cli.common as common
import test.testutils as utils


@patch('pnc_cli.utils.checked_api_call', return_value=1)
def test_id_exists(mock):
    api = 'test-api'
    search_id = 'search-id'
    assert common.id_exists(api, search_id)
    mock.assert_called_once_with('test-api', 'get_specific', id='search-id')


@patch('pnc_cli.utils.checked_api_call', return_value=None)
def test_id_exists_notexist(mock):
    api = 'test-api'
    search_id = 'search-id'
    assert not common.id_exists(api, search_id)
    mock.assert_called_once_with('test-api', 'get_specific', id='search-id')


def test_get_id_by_name():
    mock_api = create_autospec(BuildconfigurationsApi)
    mock_api.get_all.return_value = utils.create_mock_list_with_name_attribute()
    result = common.get_id_by_name(mock_api, 'testerino')
    assert result == 1


def test_get_id_by_name_notfound():
    mock_api = create_autospec(BuildconfigurationsApi)
    mock_api.get_all.return_value = MagicMock(content=[])
    result = common.get_id_by_name(mock_api, 'testerino')
    assert not result


def test_set_id():
    result = common.set_id(None, 1, None)
    assert result == 1


@patch('pnc_cli.common.get_id_by_name', return_value=2)
def test_set_id_name(mock):
    mock_api = create_autospec(BuildconfigurationsApi)
    result = common.set_id(mock_api, None, 'anotherone')
    mock.assert_called_once_with(mock_api, 'anotherone')
    assert result == 2


def test_set_id_exception():
    with pytest.raises(argh.exceptions.CommandError):
        result = common.set_id(None, None, None)


def test_get_entity():
    mock_api = create_autospec(BuildconfigurationsApi)
    mock_api.get_specific.return_value = MagicMock(content='specific')
    result = common.get_entity(mock_api, 1)
    assert result == 'specific'


def test_get_entity():
    mock_api = create_autospec(BuildconfigurationsApi)
    mock_api.get_specific.return_value = None
    result = common.get_entity(mock_api, 1)
    assert not result
