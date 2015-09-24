from mock import MagicMock, patch

__author__ = 'Tom'
from pnc_cli import buildrecordsets
from pnc_cli.swagger_client import BuildRecordSetRest


def test_create_buildrecordset_object():
    compare = BuildRecordSetRest()
    compare.build_record_ids = [1, 2, 3]
    result = buildrecordsets.create_buildrecordset_object(build_record_ids=[1, 2, 3])
    assert compare.to_dict() == result.to_dict()


@patch('pnc_cli.buildrecordsets.brs_api.get_all', return_value=MagicMock(content=[MagicMock(id=1), MagicMock(id=2)]))
def test_get_brs_id(mock):
    result = buildrecordsets.get_brs_id(1)
    mock.assert_called_once_with()
    assert result == 1


@patch('pnc_cli.buildrecordsets.brs_api.get_all', return_value=MagicMock(content=[MagicMock(id=1), MagicMock(id=2)]))
def test_get_brs_id_none(mock):
    result = buildrecordsets.get_brs_id(3)
    mock.assert_called_once_with()
    assert not result


@patch('pnc_cli.buildrecordsets.brs_api.get_all', return_value=MagicMock(content='SUCCESS'))
def test_list_build_record_sets(mock):
    result = buildrecordsets.list_build_record_sets()
    mock.assert_called_once_with()
    assert result == 'SUCCESS'


@patch('pnc_cli.buildrecordsets.get_brs_id', return_value=1)
@patch('pnc_cli.buildrecordsets.brs_api.get_specific', return_value=MagicMock(content='SUCCESS'))
def test_get_build_record_set(mock_get_specific, mock_get_brs_id):
    result = buildrecordsets.get_build_record_set(1)
    mock_get_brs_id.assert_called_once_with(1)
    mock_get_specific.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.buildrecordsets.get_brs_id', return_value=None)
@patch('pnc_cli.buildrecordsets.brs_api.get_specific')
def test_get_build_record_set_notexist(mock_get_specific, mock_get_brs_id):
    result = buildrecordsets.get_build_record_set(2)
    mock_get_brs_id.assert_called_once_with(2)
    assert not mock_get_specific.called
    assert not result


@patch('pnc_cli.buildrecordsets.create_buildrecordset_object', return_value='created-object')
@patch('pnc_cli.buildrecordsets.brs_api.create_new', return_value=MagicMock(content='SUCCESS'))
def test_create_build_record_set(mock_create_new, mock_create_buildrecordset_object):
    result = buildrecordsets.create_build_record_set(build_record_ids=[1, 2, 3])
    mock_create_buildrecordset_object.assert_called_once_with(build_record_ids=[1, 2, 3])
    mock_create_new.assert_called_once_with(body='created-object')
    assert result == 'SUCCESS'


@patch('pnc_cli.buildrecordsets.brs_api.get_all_for_product_milestone', return_value=MagicMock(content='SUCCESS'))
def test_list_build_record_sets_for_milestone(mock):
    result = buildrecordsets.list_build_record_sets_for_milestone(1)
    mock.assert_called_once_with(version_id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.buildrecordsets.get_brs_id', return_value=1)
@patch('pnc_cli.buildrecordsets.brs_api.delete_specific', return_value=MagicMock(content='SUCCESS'))
def test_delete_build_record(mock_delete_specific, mock_get_brs_id):
    result = buildrecordsets.delete_build_record_set(1)
    mock_get_brs_id.assert_called_once_with(1)
    mock_delete_specific.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.buildrecordsets.get_brs_id', return_value=None)
@patch('pnc_cli.buildrecordsets.brs_api.delete_specific', return_value=MagicMock(content='SUCCESS'))
def test_delete_build_record_notexist(mock_delete_specific, mock_get_brs_id):
    result = buildrecordsets.delete_build_record_set(1)
    mock_get_brs_id.assert_called_once_with(1)
    assert not mock_delete_specific.called
    assert not result


@patch('pnc_cli.buildrecordsets.get_brs_id', return_value=1)
@patch('pnc_cli.buildrecordsets.brs_api.get_specific')
@patch('pnc_cli.buildrecordsets.brs_api.update', return_value=MagicMock(content='SUCCESS'))
def test_update_build_record(mock_update, mock_get_specific, mock_get_brs_id):
    mock = MagicMock()
    mockcontent = MagicMock(content=mock)
    mock_get_specific.return_value = mockcontent
    result = buildrecordsets.update_build_record_set(1, build_record_ids=[1, 2, 3])
    mock_get_brs_id.assert_called_once_with(1)
    mock_get_specific.assert_called_once_with(id=1)
    mock_update.assert_called_once_with(id=1, body=mock)
    assert result == 'SUCCESS'
