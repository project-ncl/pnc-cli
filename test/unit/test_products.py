__author__ = 'Tom'

from mock import MagicMock, patch

from pnc_cli import products
from pnc_cli.swagger_client import ProductRest
from pnc_cli.swagger_client import ProductsApi


def test_create_product_object():
    compare = ProductRest()
    compare.name = 'test-product'
    compare.description = 'description'
    result = products.create_product_object(name='test-product', description='description')
    assert result.to_dict() == compare.to_dict()


@patch('pnc_cli.products.create_product_object', return_value='test-product')
@patch('pnc_cli.products.products_api.create_new', return_value=MagicMock(content='SUCCESS'))
def test_create_product(mock_create_new, mock_create_product_object):
    result = products.create_product_raw(name='testerino', abbreviation='TR', description='description')
    mock_create_product_object.assert_called_once_with(name='testerino', abbreviation='TR', description='description')
    mock_create_new.assert_called_once_with(body='test-product')
    assert result == 'SUCCESS'


@patch('pnc_cli.products.products_api.get_specific')
@patch('pnc_cli.products.products_api.update', return_value=MagicMock(content='SUCCESS'))
def test_update_product(mock_update, mock_get_specific):
    mock = MagicMock()
    mock_get_specific.return_value = MagicMock(content=mock)
    result = products.update_product_raw(1, description='new-description')
    mock_get_specific.assert_called_once_with(id=1)
    mock_update.assert_called_once_with(id=1, body=mock)
    assert result == 'SUCCESS'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.products.products_api.get_specific', return_value=MagicMock(content='SUCCESS'))
@patch('pnc_cli.products.products_api', autospec=ProductsApi)
def test_get_product_id(mock_products_api, mock_get_specific, mock_set_id):
    result = products.get_product_raw(id=1)
    mock_set_id.assert_called_once_with(mock_products_api, 1, None)
    mock_get_specific.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.products.products_api.get_specific', return_value=MagicMock(content='SUCCESS'))
@patch('pnc_cli.products.products_api', autospec=ProductsApi)
def test_get_product_name(mock_products_api, mock_get_specific, mock_set_id):
    result = products.get_product_raw(name='testerino')
    mock_set_id.assert_called_once_with(mock_products_api, None, 'testerino')
    mock_get_specific.assert_called_once_with(id=1)
    assert result == 'SUCCESS'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.products.products_api.get_product_versions', return_value=MagicMock(content='SUCCESS'))
@patch('pnc_cli.products.products_api', autospec=ProductsApi)
def test_list_versions_for_product_id(mock_products_api, mock_get_product_versions, mock_set_id):
    result = products.list_versions_for_product_raw(id=1)
    mock_set_id.assert_called_once_with(mock_products_api, 1, None)
    mock_get_product_versions.assert_called_once_with(id=1, page_index=0, page_size=200, q='', sort='')
    assert result == 'SUCCESS'


@patch('pnc_cli.common.set_id', return_value=1)
@patch('pnc_cli.products.products_api.get_product_versions', return_value=MagicMock(content='SUCCESS'))
@patch('pnc_cli.products.products_api', autospec=ProductsApi)
def test_list_versions_for_product_name(mock_products_api, mock_get_product_versions, mock_set_id):
    result = products.list_versions_for_product_raw(name='testerino')
    mock_set_id.assert_called_once_with(mock_products_api, None, 'testerino')
    mock_get_product_versions.assert_called_once_with(id=1, page_index=0, page_size=200, q='', sort='')
    assert result == 'SUCCESS'


@patch('pnc_cli.products.products_api.get_all', return_value=MagicMock(content='SUCCESS'))
def test_list_products(mock):
    result = products.list_products_raw()
    mock.assert_called_once_with(page_index=0, page_size=200, q="", sort="")
    assert result == 'SUCCESS'
