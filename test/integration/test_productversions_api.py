from pnc_cli import utils
from pnc_cli import productversions
from pnc_cli.swagger_client.apis import ProductversionsApi
from test import testutils


versions_api = ProductversionsApi(utils.get_api_client())


def create_product_version():
    return versions_api.create_new_product_version(
            body=productversions.create_product_version_object(
            product_id=1,
            version=testutils.gen_random_version())).content


def test_get_all():
    create_product_version()
    product_versions = versions_api.get_all().content
    assert product_versions is not None


def test_create_product_version():
    created_version = create_product_version()
    product_versions = [v.version for v in versions_api.get_all().content]
    assert created_version.version in product_versions


def test_get_product_version():
    created_version = create_product_version()
    retrieved_version = versions_api.get_specific(id=created_version.id).content
    assert created_version.to_dict() == retrieved_version.to_dict()


#currently unable to update build_configuration_ids
def test_update_product_version():
    created_version = create_product_version()
    created_version.build_configuration_ids = [1, 2, 3]
    versions_api.update(id=created_version.id, body=created_version)
    updated = versions_api.get_specific(id=created_version.id).content
    assert updated.to_dict() == created_version.to_dict()


def test_version_exists():
    created_version = create_product_version()
    assert productversions.version_exists(created_version.id)

