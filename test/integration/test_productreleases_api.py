__author__ = 'thauser'
import pytest

from pnc_cli.swagger_client.apis import ProductsApi
from pnc_cli.swagger_client.apis import ProductreleasesApi
from pnc_cli.swagger_client.apis import ProductmilestonesApi
from pnc_cli.swagger_client.apis import ProductversionsApi
from test import testutils
import pnc_cli.user_config as uc


@pytest.fixture(scope='module', autouse=True)
def get_product_api():
    global product_api
    product_api = ProductsApi(uc.user.get_api_client())


@pytest.fixture(scope='module', autouse=True)
def get_milestones_api():
    global milestones_api
    milestones_api = ProductmilestonesApi(uc.user.get_api_client())


@pytest.fixture(scope='module', autouse=True)
def get_releases_api():
    global releases_api
    releases_api = ProductreleasesApi(uc.user.get_api_client())


@pytest.fixture(scope='module', autouse=True)
def get_version_api():
    global versions_api
    versions_api = ProductversionsApi(uc.user.get_api_client())


def test_get_all_invalid_param():
    testutils.assert_raises_typeerror(releases_api, 'get_all')


def test_get_all(new_release):
    existing = releases_api.get_all(page_index=0, sort='', q='').content
    assert existing is not None


def test_create_new_invalid_param():
    testutils.assert_raises_typeerror(releases_api, 'create_new')


def test_create_new(new_release):
    release_ids = [r.id for r in releases_api.get_all(page_size=1000000).content]
    assert new_release.id in release_ids


def test_get_all_by_product_version_id_no_version_id():
    testutils.assert_raises_valueerror(releases_api, 'get_all_by_product_version_id', version_id=None)


def test_get_all_by_product_version_id_invalid_param():
    testutils.assert_raises_typeerror(releases_api, 'get_all_by_product_version_id', version_id=1)


def test_get_all_by_product_version_id():
    assert releases_api.get_all_by_product_version_id(version_id=1, page_index=0, page_size=1000000, sort='',
                                                      q='').content is not None


def test_get_all_support_level_invalid_param():
    testutils.assert_raises_typeerror(releases_api, 'get_all_support_level')


def test_get_all_support_level():
    assert releases_api.get_all_support_level().content is not None


def test_get_specific_no_id():
    testutils.assert_raises_valueerror(releases_api, 'get_specific', id=None)


def test_get_specific_invalid_param():
    testutils.assert_raises_typeerror(releases_api, 'get_specific', id=1)


def test_get_specific(new_release):
    retrieved_release = releases_api.get_specific(id=new_release.id).content
    assert retrieved_release.to_dict() == new_release.to_dict()


def test_update_no_id():
    testutils.assert_raises_valueerror(releases_api, 'update', id=None)


def test_update_invalid_param():
    testutils.assert_raises_typeerror(releases_api, 'update', id=1)


def test_update(new_release):
    new_release.download_url = 'updated-download-url'
    releases_api.update(id=new_release.id, body=new_release)
    updated = releases_api.get_specific(id=new_release.id).content
    assert updated.to_dict() == new_release.to_dict()


def test_get_all_builds_in_distributed_recordset_of_product_release_no_id():
    testutils.assert_raises_valueerror(releases_api, 'get_all_builds_in_distributed_recordset_of_product_release',
                                       id=None)


def test_get_all_builds_in_distributed_recordset_of_product_release_invalid_param():
    testutils.assert_raises_typeerror(releases_api, 'get_all_builds_in_distributed_recordset_of_product_release', id=1)


def test_get_all_builds_in_distributed_recordset_of_product_release(new_release):
    response = releases_api.get_all_builds_in_distributed_recordset_of_product_release(id=new_release.id)
    assert response