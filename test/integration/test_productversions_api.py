import pytest
from pnc_cli import utils
from pnc_cli import productversions
from pnc_cli.swagger_client.apis import ProductversionsApi
from test import testutils


versions_api = ProductversionsApi(utils.get_api_client())

@pytest.fixture(scope='function')
def new_version():
    version = versions_api.create_new_product_version(
            body=productversions.create_product_version_object(
            product_id=1,
            version=testutils.gen_random_version())).content
    return version


def test_get_all(new_version):
    product_versions = versions_api.get_all().content
    assert product_versions is not None


def test_create_product_version(new_version):
    product_versions = [v.version for v in versions_api.get_all().content]
    assert new_version.version in product_versions


def test_get_product_version(new_version):
    retrieved_version = versions_api.get_specific(id=new_version.id).content
    assert new_version.to_dict() == retrieved_version.to_dict()


#currently unable to update build_configuration_ids
def test_update_product_version(new_version):
    new_version.build_configuration_ids = [1, 2, 3]
    versions_api.update(id=new_version.id, body=new_version)
    updated = versions_api.get_specific(id=new_version.id).content
    assert updated.to_dict() == new_version.to_dict()


def test_version_exists(new_version):
    assert productversions.version_exists(new_version.id)

