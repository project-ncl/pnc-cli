__author__ = 'Tom'
from test import testutils
from mock import MagicMock, patch
from pnc_cli import licenses
from pnc_cli.swagger_client import LicenseRest

def test_create_license_object():
    compare = LicenseRest()
    compare.full_name = 'test-fullname'
    compare.full_content = 'test-fullcontent'
    result = licenses._create_license_object(full_name='test-fullname', full_content='test-fullcontent')
    assert result.to_dict() == compare.to_dict()

@patch('pnc_cli.licenses._license_exists', return_value=True)
def test_get_license_id_id(mock):
    result = licenses.get_license_id(1, None)
    mock.assert_called_once_with(1)
    assert result == 1

@patch('pnc_cli.licenses._license_exists', return_value=False)
def test_get_license_id_id_notexist(mock):
    result = licenses.get_license_id(1, None)
    mock.assert_called_once_with(1)
    assert not result


@patch('pnc_cli.licenses._get_license_id_by_name', return_value=1)
def test_get_license_id_name(mock):
    result = licenses.get_license_id(None, 'testerino')
    mock.assert_called_once_with('testerino')
    assert result == 1

@patch('pnc_cli.licenses._get_license_id_by_name', return_value=None)
def test_get_license_id_name(mock):
    result = licenses.get_license_id(None, 'testerino')
    mock.assert_called_once_with('testerino')
    assert not result


def test_get_license_id_none():
    result = licenses.get_license_id(None, None)
    assert not result


@patch('pnc_cli.licenses.licenses_api.get_all', return_value=MagicMock(content=[MagicMock(id=1)]))
def test_license_exists(mock):
    result = licenses._license_exists(1)
    mock.assert_called_once_with()
    assert result

@patch('pnc_cli.licenses.licenses_api.get_all', return_value=MagicMock(content=[MagicMock(full_name='testerino', id=1)]))
def test_get_license_id_by_name(mock):
    result = licenses._get_license_id_by_name('testerino')
    mock.assert_called_once_with(q='name==testerino')
    assert result == 1

@patch('pnc_cli.licenses.licenses_api.get_all', return_value=MagicMock(content=[]))
def test_get_license_id_by_name_notexist(mock):
    result = licenses._get_license_id_by_name('notexist')
    mock.assert_called_once_with(q='name==notexist')
    assert not result

@patch('pnc_cli.licenses._create_license_object', return_value='test-license')
@patch('pnc_cli.licenses.licenses_api.create_new', return_value=MagicMock(content='SUCCESS'))
def test_create_license(mock_create_new, mock_license_object):
    result = licenses.create_license(full_name='license', full_content='anothertest')
    mock_license_object.assert_called_once_with(full_name='license', full_content='anothertest')
    mock_create_new.assert_called_once_with(body='test-license')
    assert result == 'SUCCESS'

@patch('pnc_cli.licenses.get_license_id', return_value=1)
@patch('pnc_cli.licenses.licenses_api.get_specific', return_value=MagicMock(content='SUCCESS'))
def test_get_license_id(mock_get_specific, mock_get_license_id):
    result = licenses.get_license(id=1)
    mock_get_license_id.assert_called_once_with(1, None)
    mock_get_specific.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.licenses.get_license_id', return_value=1)
@patch('pnc_cli.licenses.licenses_api.get_specific', return_value=MagicMock(content='SUCCESS'))
def test_get_license_name(mock_get_specific, mock_get_license_id):
    result = licenses.get_license(name='testerino')
    mock_get_license_id.assert_called_once_with(None, 'testerino')
    mock_get_specific.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.licenses.get_license_id', return_value=None)
@patch('pnc_cli.licenses.licenses_api.get_specific')
def test_get_license_notexist(mock_get_specific, mock_get_license_id):
    result = licenses.get_license(name='testerino')
    mock_get_license_id.assert_called_once_with(None, 'testerino')
    assert not mock_get_specific.called
    assert not result


@patch('pnc_cli.licenses.licenses_api.delete', return_value=MagicMock(content='SUCCESS'))
def test_delete_license(mock):
    result = licenses.delete_license(1)
    mock.assert_called_once_with(id=1)
    assert result == 'SUCCESS'

@patch('pnc_cli.licenses.licenses_api.get_all', return_value=MagicMock(content='SUCCESS'))
def test_list_licenses(mock):
    result = licenses.list_licenses()
    mock.assert_called_once_with(page_size=200, q="", sort="")
    assert result == 'SUCCESS'


@patch('pnc_cli.licenses._create_license_object', return_value='test-license')
@patch('pnc_cli.licenses._license_exists', return_value=True)
@patch('pnc_cli.licenses.licenses_api.update', return_value=MagicMock(content='SUCCESS'))
def test_update_license(mock_update, mock_license_exists, mock_create_object):
    result = licenses.update_license(1, full_name='update')
    mock_create_object.assert_called_once_with(full_name='update')
    mock_license_exists.assert_called_once_with(1)
    mock_update.assert_called_once_with(id=1, body='test-license')
    assert result == 'SUCCESS'


@patch('pnc_cli.licenses._create_license_object', return_value='test-license')
@patch('pnc_cli.licenses._license_exists', return_value=False)
@patch('pnc_cli.licenses.licenses_api.update')
def test_update_license_notexist(mock_update, mock_license_exists, mock_create_object):
    result = licenses.update_license(1, full_name='update')
    mock_create_object.assert_called_once_with(full_name='update')
    mock_license_exists.assert_called_once_with(1)
    assert not mock_update.called
    assert not result