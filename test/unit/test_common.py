from mock import MagicMock, patch, create_autospec
# used for mock's autospec
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
def test_id_notexist(mock):
    api = 'test-api'
    search_id = 'search-id'
    assert not common.id_exists(api, search_id)
    mock.assert_called_once_with('test-api', 'get_specific', id='search-id')


def test_get_id_by_name():
    pass


def test_set_id():
    pass


def test_set_id_name():
    pass


def test_set_id_exception():
    pass


def test_get_entity():
    pass
