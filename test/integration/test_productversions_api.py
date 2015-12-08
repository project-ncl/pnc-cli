import pytest
from pnc_cli import utils
from pnc_cli import productversions
from pnc_cli import products
from pnc_cli.swagger_client.apis import ProductversionsApi
from pnc_cli.swagger_client.apis import ProductsApi
from test import testutils

product_api = ProductsApi(utils.get_api_client())
versions_api = ProductversionsApi(utils.get_api_client())


@pytest.fixture(scope='function')
def new_product():
    product = product_api.create_new(body=products._create_product_object(name=testutils.gen_random_name(),
                                                                          description="PNC CLI: test_productversions_api product"
                                                                          )).content
    return product

@pytest.fixture(scope='function')
def new_version(new_product):
    version = versions_api.create_new_product_version(
        body=productversions.create_product_version_object(
            product_id=new_product.id,
            version=get_unique_version(new_product.id))).content
    return version

def get_unique_version(product_id):
    rand_version = testutils.gen_random_version()
    existing = product_api.get_product_versions(id=product_id, page_size=100000).content
    while existing is not None and rand_version in [x.version for x in existing]:
        rand_version = testutils.gen_random_version()
    return rand_version


def test_get_all_invalid_param():
    testutils.assert_raises_typeerror(versions_api, 'get_all')


def test_get_all():
    product_versions = versions_api.get_all(page_index=0, page_size=1000000, sort='', q='').content
    assert product_versions is not None


def test_create_new_product_version_invalid_param():
    testutils.assert_raises_typeerror(versions_api, 'create_new_product_version')


def test_create_new_product_version(new_version):
    product_versions = [v.id for v in versions_api.get_all(page_size=1000000).content]
    assert new_version.id in product_versions


def test_get_specific_no_id():
    testutils.assert_raises_valueerror(versions_api, 'get_specific', id=None)


def test_get_specific_invalid_param():
    testutils.assert_raises_typeerror(versions_api, 'get_specific', id=1)


def test_get_specific(new_version):
    retrieved_version = versions_api.get_specific(id=new_version.id).content
    assert new_version.to_dict() == retrieved_version.to_dict()


def test_update_no_id():
    testutils.assert_raises_valueerror(versions_api, 'update', id=None)


def test_update_invalid_param():
    testutils.assert_raises_typeerror(versions_api, 'update', id=1)


# currently unable to update build_configuration_ids
def test_update(new_version):
    new_version.version = get_unique_version(new_version.product_id)
    versions_api.update(id=new_version.id, body=new_version)
    updated = versions_api.get_specific(id=new_version.id).content
    assert updated.version == new_version.version


def test_version_exists(new_version):
    assert productversions.version_exists(new_version.id)


def test_get_build_configuration_sets_no_id():
    testutils.assert_raises_valueerror(versions_api, 'get_build_configuration_sets', id=None)


def test_get_build_configuration_sets_invalid_param():
    testutils.assert_raises_typeerror(versions_api, 'get_build_configuration_sets', id=1)


def test_get_build_configuration_sets():
    sets = versions_api.get_build_configuration_sets(id=1)
    assert sets is not None
