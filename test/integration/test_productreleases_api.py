__author__ = 'thauser'
import pytest
from pnc_cli.swagger_client.apis import ProductreleasesApi
from pnc_cli import utils
from pnc_cli import productreleases
from test import testutils

releases_api = ProductreleasesApi(utils.get_api_client())


@pytest.fixture(scope='function')
def new_release():
    release = releases_api.create_new(body=productreleases.create_product_release_object(
        version=testutils.gen_random_version() + ".9.DR1",
        release_date="2016-01-01",
        download_url="pnc-cli-test-url",
        product_version_id=1,
        product_milestone_id=1,
        support_level='EOL'
    ))
    return release


def test_get_all_invalid_param():
    testutils.assert_raises_typeerror(releases_api, 'get_all')


def test_get_all(new_release):
    assert releases_api.get_all(page_index=0, page_size=1000, sort='', q='').content is not None


def test_create_new_invalid_param():
    testutils.assert_raises_typeerror(releases_api, 'create_new')


def test_create_new(new_release):
    release_ids = [r.id for r in releases_api.get_all().content]
    assert new_release.id in release_ids


def test_get_all_by_product_version_id_no_version_id():
    testutils.assert_raises_valueerror(releases_api, 'get_all_by_product_version_id', version_id=None)


def test_get_all_by_product_version_id_invalid_param():
    testutils.assert_raises_typeerror(releases_api, 'get_all_by_product_version_id', version_id=1)


def test_get_all_by_product_version_id():
    assert releases_api.get_all_by_product_version_id(version_id=1, page_index=0, page_size=1000, sort='',
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
    retrieved_release = releases_api.get_specific(id=new_release.id)
    assert retrieved_release.to_dict() == new_release.to_dict()


def test_update_no_id():
    testutils.assert_raises_valueerror(releases_api, 'update', id=None)


def test_update_invalid_param():
    testutils.assert_raises_typeerror(releases_api, 'update', id=1)


def test_update(new_release):
    new_release.download_url = 'updated-download-url'
    releases_api.update(id=new_release.id, body=new_release)
    updated = releases_api.get_specific(id=new_release.id)
    assert updated.to_dict() == new_release.to_dict()