__author__ = 'thauser'
import pytest
import datetime


from pnc_cli.swagger_client.apis import ProductsApi
from pnc_cli.swagger_client.apis import ProductreleasesApi
from pnc_cli.swagger_client.apis import ProductmilestonesApi
from pnc_cli.swagger_client.apis import ProductversionsApi
from pnc_cli import utils
from pnc_cli import productreleases
from pnc_cli import productmilestones
from pnc_cli import productversions
from pnc_cli import products
from test import testutils


@pytest.fixture(scope='function', autouse=True)
def get_product_api():
    global product_api
    product_api = ProductsApi(utils.get_api_client())

milestones_api = ProductmilestonesApi(utils.get_api_client())
releases_api = ProductreleasesApi(utils.get_api_client())
versions_api = ProductversionsApi(utils.get_api_client())

@pytest.fixture(scope='function')
def new_product():
    product = product_api.create_new(body=products._create_product_object(name=testutils.gen_random_name(),
                                                                          description="PNC CLI: test_productreleases_api product"
                                                                          )).content
    return product

@pytest.fixture(scope='function')
def new_version(new_product):
    version_number = testutils.gen_random_version()
    existing = product_api.get_product_versions(id=new_product.id).content
    while existing is not None and version_number in [x.version for x in existing]:
        version_number = testutils.gen_random_version()
    version = versions_api.create_new_product_version(body=productversions.create_product_version_object(
        version=version_number,
        product_id=1,
        current_product_milestone_id=1
    )).content
    return version


@pytest.fixture(scope='function')
def new_milestone(new_version):
    starting = utils.unix_time_millis(datetime.datetime(2016, 1, 2, 12, 0, 0))
    ending = utils.unix_time_millis(datetime.datetime(2017, 1, 2, 12, 0, 0))
    milestone = milestones_api.create_new(body=productmilestones.create_milestone_object(
        version=new_version.version+'.1.build3',
        starting_date=starting,
        planned_end_date=ending,
        download_url='localhost:8080/build3',
        product_version_id=new_version.id
    )).content
    return milestone


@pytest.fixture(scope='function')
def new_release(new_milestone):
    release_time = utils.unix_time_millis(datetime.datetime(2016, 1, 2, 12, 0, 0))
    associated_version = versions_api.get_specific(id=new_milestone.product_version_id).content.version
    release = releases_api.create_new(body=productreleases.create_product_release_object(
        version= associated_version + ".1.DR1",
        release_date=release_time,
        download_url="pnc-cli-test-url",
        product_version_id=new_milestone.product_version_id,
        product_milestone_id=new_milestone.id,
        support_level='EOL'
    )).content
    return release


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