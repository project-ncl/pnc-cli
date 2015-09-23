from pnc_cli import products
from pnc_cli import productversions
from pnc_cli import utils
from pnc_cli.swagger_client.apis.products_api import ProductsApi
from pnc_cli.swagger_client.apis.productversions_api import ProductversionsApi
from test import testutils

product_api = ProductsApi(utils.get_api_client())
versions_api = ProductversionsApi(utils.get_api_client())


def _create_product():
    return product_api.create_new(body=products._create_product_object(name=testutils.gen_random_name())).content


def test_get_all():
    p = product_api.get_all().content
    assert p is not None


def test_create_new():
    new_prod = _create_product()
    prod_ids = [x.id for x in product_api.get_all().content]
    assert new_prod.id in prod_ids


def test_get_specific():
    new_prod = _create_product()
    assert product_api.get_specific(id=new_prod.id) is not None


def test_update_product():
    new_prod = _create_product()
    newname = 'newname' + testutils.gen_random_name()
    product_api.update(id=new_prod.id,
                       body=products._create_product_object(name=newname, description='updated description'))
    updated_prod = product_api.get_specific(id=new_prod.id).content
    assert updated_prod.name == newname and updated_prod.description == 'updated description'


def test_list_versions_for_product():
    randversion = testutils.gen_random_version()
    new_prod = _create_product()
    versions_api.create_new_product_version(
        body=productversions.create_product_version_object(product_id=new_prod.id, version=randversion))
    versions = [x.version for x in product_api.get_product_versions(id=new_prod.id).content]
    assert versions is not None and randversion in versions


def test_get_product_id_by_name():
    new_prod = _create_product()
    assert product_api.get_specific(
        id=products.get_product_id_by_name(new_prod.name)).content.id == product_api.get_specific(
        id=new_prod.id).content.id
