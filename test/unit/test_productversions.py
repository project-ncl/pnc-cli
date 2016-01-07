import test.testutils

__author__ = 'thauser'
from pnc_cli import productversions
from pnc_cli.swagger_client import ProductVersionRest
from mock import MagicMock, patch


def test_create_product_version_object():
    productversion = productversions.create_product_version_object(name='test', product_id=1, product_milestones=[1, 2])
    test_version = ProductVersionRest()
    test_version.name = 'test'
    test_version.product_id = 1
    test_version.product_milestones = [1, 2]
    assert productversion.to_dict() == test_version.to_dict()


@patch('pnc_cli.productversions.versions_api.get_all',
       return_value=MagicMock(content=[MagicMock(id=1)]))
def test_version_exists(mock):
    result = productversions.version_exists(1)
    mock.assert_called_once_with(q='id==1')
    assert result


@patch('pnc_cli.productversions.versions_api.get_all',
       return_value=None)
def test_version_exists_notexist(mock):
    result = productversions.version_exists(10)
    mock.assert_called_once_with(q='id==10')
    assert not result


@patch('pnc_cli.productversions.products_api.get_product_versions',
       return_value=MagicMock(content=[MagicMock(version='1.0')]))
def test_version_exists_for_product(mock):
    result = productversions.version_exists_for_product(1, '1.0')
    mock.assert_called_once_with(id=1)
    assert result


@patch('pnc_cli.productversions.products_api.get_product_versions',
       return_value=MagicMock(content=[MagicMock(version='1.0')]))
def test_version_exists_for_product_notexist(mock):
    result = productversions.version_exists_for_product(1, '10.10')
    mock.assert_called_once_with(id=1)
    assert not result


@patch('pnc_cli.productversions.versions_api.get_all', return_value=MagicMock(content=['1.0', '1.6', '2.0']))
def test_list_product_versions(mock):
    result = productversions.list_product_versions()
    mock.assert_called_once_with(page_size=200, q="", sort="")
    assert result == ['1.0', '1.6', '2.0']


@patch('pnc_cli.productversions.version_exists_for_product', return_value=True)
@patch('pnc_cli.productversions.products_api.get_specific',
       return_value=MagicMock(content=test.testutils.create_mock_object_with_name_attribute('productname')))
def test_create_product_version_already_exists(mock_get_specific, mock_version_exists_for_product):
    result = productversions.create_product_version(1, '1.0')
    mock_version_exists_for_product.assert_called_once_with(1, '1.0')
    mock_get_specific.assert_called_once_with(id=1)
    assert not result


@patch('pnc_cli.productversions.version_exists_for_product', return_value=False)
@patch('pnc_cli.productversions.create_product_version_object', return_value='mock-product-version')
@patch('pnc_cli.productversions.versions_api.create_new_product_version', return_value=MagicMock(content='SUCCESS'))
def test_create_product_version(mock_create_new_product_version, mock_create_product_version_object,
                                mock_version_exists_for_product):
    result = productversions.create_product_version(1, '1.0')
    mock_version_exists_for_product.assert_called_once_with(1, '1.0')
    mock_create_product_version_object.assert_called_once_with(product_id=1, version='1.0')
    mock_create_new_product_version.assert_called_once_with(body='mock-product-version')
    assert result == 'SUCCESS'


@patch('pnc_cli.productversions.version_exists', return_value=True)
@patch('pnc_cli.productversions.versions_api.get_specific', return_value=MagicMock(content='mock-product-version'))
def test_get_product_version(mock_get_specific, mock_version_exists):
    result = productversions.get_product_version(1)
    mock_version_exists.assert_called_once_with(1)
    mock_get_specific.assert_called_once_with(id=1)
    assert result == 'mock-product-version'


@patch('pnc_cli.productversions.version_exists', return_value=False)
@patch('pnc_cli.productversions.versions_api.get_specific')
def test_get_product_version_notexist(mock_get_specific, mock_version_exists):
    result = productversions.get_product_version(1)
    mock_version_exists.assert_called_once_with(1)
    assert not mock_get_specific.called
    assert not result


@patch('pnc_cli.productversions.version_exists', return_value=True)
@patch('pnc_cli.productversions.versions_api.get_specific')
@patch('pnc_cli.productversions.versions_api.update', return_value=MagicMock(content='SUCCESS'))
def test_update_product_version(mock_update, mock_get_specific, mock_version_exists):
    # cannot set return value in patch decorator because the comparison to particular
    # mock object must be made
    mock = MagicMock()
    mockcontent = MagicMock(content=mock)
    mock_get_specific.return_value = mockcontent
    result = productversions.update_product_version(1, version='2.0')
    mock_version_exists.assert_called_once_with(1)
    mock_get_specific.assert_called_once_with(id=1)
    mock_update.assert_called_once_with(id=1, body=mock)
    # object returned by get_specific is appropriately modified
    assert getattr(mock, 'version') == '2.0'
    assert result == 'SUCCESS'


@patch('pnc_cli.productversions.version_exists', return_value=False)
@patch('pnc_cli.productversions.versions_api.get_specific')
@patch('pnc_cli.productversions.versions_api.update')
def test_update_product_version_notexist(mock_update, mock_get_specific, mock_version_exists):
    result = productversions.update_product_version(1, version='2.0')
    mock_version_exists.assert_called_once_with(1)
    assert not mock_get_specific.called
    assert not mock_update.called
    assert not result
