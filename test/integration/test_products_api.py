import pytest
from pnc_cli import products
from pnc_cli import productversions
from pnc_cli import utils
from pnc_cli.swagger_client.apis.products_api import ProductsApi
from pnc_cli.swagger_client.apis.productversions_api import ProductversionsApi
from test import testutils

@pytest.fixture(scope='function', autouse=True)
def get_product_api():
    global product_api
    product_api = ProductsApi(utils.get_api_client())


def test_get_all_invalid_param():
    testutils.assert_raises_typeerror(product_api, 'get_all')


def test_get_all():
    p = product_api.get_all(page_index=0, page_size=1000000, sort='', q='').content
    assert p is not None


def test_create_new_invalid_param():
    testutils.assert_raises_typeerror(product_api, 'create_new')


def test_create_new(new_product):
    prod_ids = [x.id for x in product_api.get_all(page_size=1000000).content]
    assert new_product.id in prod_ids


def test_get_specific_no_id():
    testutils.assert_raises_valueerror(product_api, 'get_specific', id=None)


def test_get_specific_invalid_param():
    testutils.assert_raises_typeerror(product_api, 'get_specific', id=1)


def test_get_specific(new_product):
    assert product_api.get_specific(id=new_product.id) is not None


def test_update_no_id():
    testutils.assert_raises_valueerror(product_api, 'update', id=None)


def test_update_invalid_param():
    testutils.assert_raises_typeerror(product_api, 'update', id=1)


def test_update(new_product):
    NEW_DESC = 'PNC CLI: test_products_api updated description'
    newname = 'newname' + testutils.gen_random_name()
    product_api.update(id=new_product.id,
                       body=products.create_product_object(name=newname, description=NEW_DESC))
    updated_prod = product_api.get_specific(id=new_product.id).content
    assert updated_prod.name == newname and updated_prod.description == NEW_DESC


def test_get_product_versions_no_id():
    testutils.assert_raises_valueerror(product_api, 'get_product_versions', id=None)


def test_get_product_versions_invalid_param():
    testutils.assert_raises_typeerror(product_api, 'get_product_versions', id=1)


def test_get_product_versions(new_product):
    versions_api = ProductversionsApi(utils.get_api_client())
    randversion = testutils.gen_random_version()
    versions_api.create_new_product_version(
        body=productversions.create_product_version_object(product_id=new_product.id, version=randversion))
    versions = [x.version for x in product_api.get_product_versions(id=new_product.id).content]
    assert versions is not None and randversion in versions