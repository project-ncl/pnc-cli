__author__ = 'Tom'

from mock import MagicMock, patch
from test import testutils
from pnc_cli import products
from pnc_cli.swagger_client import ProductRest


def test_create_product_object():
    compare = ProductRest()
    compare.name = 'test-product'
    compare.description = 'description'
    result = products._create_product_object(name='test-product', description='description')
    assert result.to_dict() == compare.to_dict()


@patch('pnc_cli.products.products_api.get_specific', return_value=MagicMock(content=[MagicMock(id=1)]))
def test_product_exists(mock):
    result = products._product_exists(1)
    mock.assert_called_once_with(id=1)
    assert result


@patch('pnc_cli.products.products_api.get_specific', return_value=None)
def test_product_exists_notexist(mock):
    result = products._product_exists(2)
    mock.assert_called_once_with(id=2)
    assert not result


@patch('pnc_cli.products._product_exists', return_value=True)
def test_get_product_id_id(mock):
    result = products.get_product_id(1, None)
    mock.assert_called_once_with(1)
    assert result == 1


@patch('pnc_cli.products._product_exists', return_value=False)
def test_get_product_id_id_notexist(mock):
    result = products.get_product_id(1, None)
    mock.assert_called_once_with(1)
    assert not result


@patch('pnc_cli.products.get_product_id_by_name', return_value=1)
def test_get_product_id_name(mock):
    result = products.get_product_id(None, 'testerino')
    mock.assert_called_once_with('testerino')
    assert result == 1


@patch('pnc_cli.products.get_product_id_by_name', return_value=None)
def test_get_product_id_name_notexist(mock):
    result = products.get_product_id(None, 'testerino')
    mock.assert_called_once_with('testerino')
    assert not result


def test_get_product_id_none():
    result = products.get_product_id(None, None)
    assert not result


@patch('pnc_cli.products.products_api.get_all',
       return_value=MagicMock(content=[testutils.create_mock_object_with_name_attribute('testerino')]))
def test_get_product_id_by_name(mock):
    result = products.get_product_id_by_name('testerino')
    mock.assert_called_once_with()
    assert result == 1


@patch('pnc_cli.products.products_api.get_all',
       return_value=MagicMock(content=[testutils.create_mock_object_with_name_attribute('nope')]))
def test_get_product_id_by_name_notexist(mock):
    result = products.get_product_id_by_name('testerino')
    mock.assert_called_once_with()
    assert not result


@patch('pnc_cli.products._create_product_object', return_value='test-product')
@patch('pnc_cli.products.products_api.create_new', return_value=MagicMock(content='SUCCESS'))
def test_create_product(mock_create_new, mock_create_product_object):
    result = products.create_product(name='testerino', description='description')
    mock_create_product_object.assert_called_once_with(name='testerino', description='description')
    mock_create_new.assert_called_once_with(body='test-product')
    assert result == 'SUCCESS'


@patch('pnc_cli.products.get_product_id', return_value=1)
@patch('pnc_cli.products.products_api.get_specific')
@patch('pnc_cli.products.products_api.update', return_value=MagicMock(content='SUCCESS'))
def test_update_product(mock_update, mock_get_specific, mock_get_product_id):
    mock = MagicMock()
    mock_get_specific.return_value = MagicMock(content=mock)
    result = products.update_product(1, description='new-description')
    mock_get_product_id.assert_called_once_with(1, None)
    mock_get_specific.assert_called_once_with(id=1)
    mock_update.assert_called_once_with(id=1, body=mock)
    assert result == 'SUCCESS'


@patch('pnc_cli.products.get_product_id', return_value=None)
@patch('pnc_cli.products.products_api.get_specific')
@patch('pnc_cli.products.products_api.update')
def test_update_product_notexist(mock_update, mock_get_specific, mock_get_product_id):
    result = products.update_product(1, name='testerino')
    mock_get_product_id.assert_called_once_with(1, None)
    assert not mock_get_specific.called
    assert not mock_update.called
    assert not result


@patch('pnc_cli.products.get_product_id', return_value=1)
@patch('pnc_cli.products.products_api.get_specific', return_value=MagicMock(content='SUCCESS'))
def test_get_product_id(mock_get_specific, mock_get_product_id):
    result = products.get_product(id=1)
    mock_get_product_id.assert_called_once_with(1, None)
    mock_get_specific.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.products.get_product_id', return_value=1)
@patch('pnc_cli.products.products_api.get_specific', return_value=MagicMock(content='SUCCESS'))
def test_get_product_name(mock_get_specific, mock_get_product_id):
    result = products.get_product(name='testerino')
    mock_get_product_id.assert_called_once_with(None, 'testerino')
    mock_get_specific.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.products.get_product_id', return_value=None)
@patch('pnc_cli.products.products_api.get_specific')
def test_get_product_none(mock_get_specific, mock_get_product_id):
    result = products.get_product(id=1)
    mock_get_product_id.assert_called_once_with(1, None)
    assert not mock_get_specific.called
    assert not result


@patch('pnc_cli.products.get_product_id', return_value=1)
@patch('pnc_cli.products.products_api.get_product_versions', return_value=MagicMock(content='SUCCESS'))
def test_list_versions_for_product_id(mock_get_product_versions, mock_get_product_id):
    result = products.list_versions_for_product(id=1)
    mock_get_product_id.assert_called_once_with(1, None)
    mock_get_product_versions.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.products.get_product_id', return_value=1)
@patch('pnc_cli.products.products_api.get_product_versions', return_value=MagicMock(content='SUCCESS'))
def test_list_versions_for_product_name(mock_get_product_versions, mock_get_product_id):
    result = products.list_versions_for_product(name='testerino')
    mock_get_product_id.assert_called_once_with(None, 'testerino')
    mock_get_product_versions.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.products.get_product_id', return_value=None)
@patch('pnc_cli.products.products_api.get_product_versions')
def test_list_versions_for_product_none(mock_get_product_versions, mock_get_product_id):
    result = products.list_versions_for_product(id=1)
    mock_get_product_id.assert_called_once_with(1, None)
    assert not mock_get_product_versions.called
    assert not result

@patch('pnc_cli.products.products_api.get_all', return_value=MagicMock(content='SUCCESS'))
def test_list_products(mock):
    result = products.list_products()
    mock.assert_called_once_with(page_size=200, q="", sort="")
    assert result == 'SUCCESS'
