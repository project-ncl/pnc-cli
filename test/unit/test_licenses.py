import pytest

__author__ = 'Tom'
from test import testutils
from mock import MagicMock, patch
from pnc_cli import licenses
from pnc_cli.swagger_client import LicenseRest
from pnc_cli.swagger_client import LicensesApi


def test_create_license_object():
    compare = LicenseRest()
    compare.full_name = 'test-fullname'
    compare.full_content = 'test-fullcontent'
    result = licenses.create_license_object(full_name='test-fullname', full_content='test-fullcontent')
    assert result.to_dict() == compare.to_dict()

@pytest.mark.skip(reason="Not used now")
@patch('pnc_cli.licenses.create_license_object', return_value='test-license')
@patch('pnc_cli.licenses.pnc_api.licenses.create_new', return_value=MagicMock(content='SUCCESS'))
def test_create_license(mock_create_new, mock_license_object):
    result = licenses.create_license(full_name='license', full_content='anothertest')
    mock_license_object.assert_called_once_with(full_name='license', full_content='anothertest')
    mock_create_new.assert_called_once_with(body='test-license')
    assert result == 'SUCCESS'

@pytest.mark.skip(reason="Not used now")
@patch('pnc_cli.licenses.pnc_api.licenses.get_specific', return_value=MagicMock(content='SUCCESS'))
def test_get_license_id(mock):
    result = licenses.get_license(id=1)
    mock.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@pytest.mark.skip(reason="Not used now")
@patch('pnc_cli.licenses.pnc_api.licenses.delete', return_value=MagicMock(content='SUCCESS'))
def test_delete_license(mock):
    result = licenses.delete_license(1)
    mock.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@pytest.mark.skip(reason="Not used now")
@patch('pnc_cli.licenses.pnc_api.licenses.get_all', return_value=MagicMock(content='SUCCESS'))
def test_list_licenses(mock):
    result = licenses.list_licenses()
    mock.assert_called_once_with(page_size=200, q="", sort="")
    assert result == 'SUCCESS'


@pytest.mark.skip(reason="Not used now")
@patch('pnc_cli.licenses.pnc_api.licenses.get_specific')
@patch('pnc_cli.licenses.pnc_api.licenses.update', return_value=MagicMock(content='SUCCESS'))
def test_update_license(mock_update, mock_get_specific):
    license = LicenseRest()
    response = MagicMock(content=license)
    mock_get_specific.return_value = response
    result = licenses.update_license(1, full_name='update')
    mock_get_specific.assert_called_once_with(id=1)
    mock_update.assert_called_once_with(id=1, body=license)
    assert result == 'SUCCESS'


