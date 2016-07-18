import pytest

import test.integration.conftest as conftest
from pnc_cli import utils
from pnc_cli.swagger_client.apis import ProductversionsApi
from test import testutils


@pytest.fixture(scope='function', autouse=True)
def get_versions_api():
    global versions_api
    versions_api = ProductversionsApi(utils.get_api_client())


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
    new_version.version = conftest.get_unique_version(new_version.product_id)
    versions_api.update(id=new_version.id, body=new_version)
    updated = versions_api.get_specific(id=new_version.id).content
    assert updated.version == new_version.version


def test_get_build_configuration_sets_no_id():
    testutils.assert_raises_valueerror(versions_api, 'get_build_configuration_sets', id=None)


def test_get_build_configuration_sets_invalid_param():
    testutils.assert_raises_typeerror(versions_api, 'get_build_configuration_sets', id=1)


def test_get_build_configuration_sets():
    sets = versions_api.get_build_configuration_sets(id=1)
    assert sets is not None
