from mock import MagicMock, patch

__author__ = 'Tom'
from pnc_cli import users
from pnc_cli.swagger_client import UserRest
from pnc_cli import utils
from test import testutils


@patch('pnc_cli.users.users_api.get_all',
       return_value=MagicMock(content=[MagicMock(id=1), MagicMock(id=2), MagicMock(id=3)]))
def test_user_exists(mock):
    result = users.user_exists(1)
    mock.assert_called_once_with()
    assert result


@patch('pnc_cli.users.users_api.get_all',
       return_value=MagicMock(content=[MagicMock(id=1, username='test1'), MagicMock(id=2, username='testerino')]))
def test_get_user_id_by_name(mock):
    result = users.get_user_id_by_name('testerino')
    mock.assert_called_once_with()
    assert result == 2


@patch('pnc_cli.users.users_api.get_all',
       return_value=MagicMock(content=[MagicMock(id=1, username='test1'), MagicMock(id=2, username='testerino')]))
def test_get_user_id_by_name_notexist(mock):
    result = users.get_user_id_by_name('notexist')
    mock.assert_called_once_with()
    assert not result

@patch('pnc_cli.users.user_exists', return_value=True)
def test_get_user_id_id(mock):
    result = users.get_user_id(1, None)
    mock.assert_called_once_with(1)
    assert result == 1


@patch('pnc_cli.users.user_exists', return_value=False)
def test_get_user_id_id_notexist(mock):
    result = users.get_user_id(1, None)
    mock.assert_called_once_with(1)
    assert not result


@patch('pnc_cli.users.get_user_id_by_name', return_value=2)
def test_get_user_id_name(mock):
    result = users.get_user_id(None, 'testerino')
    mock.assert_called_once_with('testerino')
    assert result == 2


@patch('pnc_cli.users.get_user_id_by_name', return_value=None)
def test_get_user_id_name_notexist(mock):
    result = users.get_user_id(None, 'testerino')
    mock.assert_called_once_with('testerino')
    assert not result


def test_get_user_id_none():
    result = users.get_user_id(None, None)
    assert not result


def test_create_user_object():
    compare = UserRest()
    compare.username = 'tomhauser'
    compare.email = 'test@test.com'
    result = users.create_user_object(username='tomhauser', email='test@test.com')
    assert compare.to_dict() == result.to_dict()


@patch('pnc_cli.users.users_api.get_all', return_value=MagicMock(content=[1, 2, 3]))
def test_list_users(mock):
    result = users.list_users()
    mock.assert_called_once_with()
    assert result == [1, 2, 3]


@patch('pnc_cli.users.get_user_id', return_value=1)
@patch('pnc_cli.users.users_api.get_specific', return_value=MagicMock(content='SUCCESS'))
def test_get_user_id(mock_get_specific, mock_get_user_id):
    result = users.get_user(id=1)
    mock_get_user_id.assert_called_once_with(1, None)
    mock_get_specific.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.users.get_user_id', return_value=1)
@patch('pnc_cli.users.users_api.get_specific', return_value=MagicMock(content='SUCCESS'))
def test_get_user_name(mock_get_specific, mock_get_user_id):
    result = users.get_user(name='testerino')
    mock_get_user_id.assert_called_once_with(None, 'testerino')
    mock_get_specific.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.users.get_user_id', return_value=None)
@patch('pnc_cli.users.users_api.get_specific')
def test_get_user_notexist(mock_get_specific, mock_get_user_id):
    result = users.get_user(name='testerino')
    mock_get_user_id.assert_called_once_with(None, 'testerino')
    assert not mock_get_specific.called
    assert not result


@patch('pnc_cli.users.create_user_object', return_value='created-user')
@patch('pnc_cli.users.users_api.create_new', return_value=MagicMock(content='SUCCESS'))
def test_create_user(mock_create_new, mock_create_user_object):
    result = users.create_user(username='testuser', email='test.test@test.com')
    mock_create_user_object.assert_called_once_with(username='testuser', email='test.test@test.com')
    mock_create_new.asset_called_once_with(body='created-user')
    assert result == 'SUCCESS'


@patch('pnc_cli.users.get_user_id', return_value=1)
@patch('pnc_cli.users.users_api.get_specific')
@patch('pnc_cli.users.users_api.update', return_value=MagicMock(content='SUCCESS'))
def test_update_user_id(mock_update, mock_get_specific, mock_get_user_id):
    mock = MagicMock()
    mockcontent = MagicMock(content=mock)
    mock_get_specific.return_value = mockcontent
    result = users.update_user(id=1, username='newusername')
    mock_get_user_id.assert_called_once_with(1, None)
    mock_get_specific.assert_called_once_with(id=1)
    assert getattr(mock, 'username') == 'newusername'
    mock_update.assert_called_once_with(id=1, body=mock)
    assert result == 'SUCCESS'


@patch('pnc_cli.users.get_user_id', return_value=1)
@patch('pnc_cli.users.users_api.get_specific')
@patch('pnc_cli.users.users_api.update', return_value=MagicMock(content='SUCCESS'))
def test_update_user_name(mock_update, mock_get_specific, mock_get_user_id):
    mock = MagicMock()
    mockcontent = MagicMock(content=mock)
    mock_get_specific.return_value = mockcontent
    result = users.update_user(name='olduser', username='newusername')
    mock_get_user_id.assert_called_once_with(None, 'olduser')
    mock_get_specific.assert_called_once_with(id=1)
    assert getattr(mock, 'username') == 'newusername'
    mock_update.assert_called_once_with(id=1, body=mock)
    assert result == 'SUCCESS'


@patch('pnc_cli.users.get_user_id', return_value=None)
@patch('pnc_cli.users.users_api.get_specific')
@patch('pnc_cli.users.users_api.update')
def test_update_user_notexist(mock_update, mock_get_specific, mock_get_user_id):
    result = users.update_user(name='olduser', username='newusername')
    mock_get_user_id.assert_called_once_with(None, 'olduser')
    assert not mock_get_specific.called
    assert not mock_update.called
    assert not result
