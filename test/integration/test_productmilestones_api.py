import pytest

__author__ = 'thauser'
from pnc_cli.swagger_client.apis import ProductmilestonesApi
from pnc_cli.swagger_client.apis import ProductversionsApi
from pnc_cli import utils
from pnc_cli import productmilestones
from pnc_cli import productversions
from test import testutils

versions_api = ProductversionsApi(utils.get_api_client())
milestone_api = ProductmilestonesApi(utils.get_api_client())


@pytest.fixture(scope='function')
def new_version():
    version_number = testutils.gen_random_version()
    while version_number in [x.version for x in versions_api.get_all(page_size=1000000).content]:
        version_number = testutils.gen_random_version()
    version = versions_api.create_new_product_version(body=productversions.create_product_version_object(
        version=version_number,
        product_id=1,
        current_product_milestone_id=1
    )).content
    return version


@pytest.fixture(scope='function')
def new_milestone(new_version):
    milestone = milestone_api.create_new(body=productmilestones.create_milestone_object(
        product_version_id=new_version.id, version=new_version.version + ".1.GA", start_date="2015-01-01",
        planned_release_date="2015-01-02"
    )).content
    return milestone


def test_get_all_invalid_param():
    testutils.assert_raises_typeerror(milestone_api, 'get_all')


def test_get_all(new_milestone):
    assert milestone_api.get_all(page_index=0, page_size=1000000, sort='', q='').content is not None


def test_create_new_invalid_param():
    testutils.assert_raises_typeerror(milestone_api, 'create_new')


def test_create_new(new_milestone):
    milestones = [m.id for m in milestone_api.get_all(page_size=1000000).content]
    assert new_milestone.id in milestones


def test_get_all_by_product_version_id_no_version_id():
    testutils.assert_raises_valueerror(milestone_api, 'get_all_by_product_version_id', version_id=None)


def test_get_all_by_product_version_id_invalid_param():
    testutils.assert_raises_typeerror(milestone_api, 'get_all_by_product_version_id', version_id=1)


def test_get_all_by_product_version_id():
    milestones = milestone_api.get_all_by_product_version_id(version_id=1, page_index=0, page_size=1000000, sort='',
                                                             q='').content
    assert milestones is not None


def test_get_specific_no_id():
    testutils.assert_raises_valueerror(milestone_api, 'get_specific', id=None)


def test_get_specific_invalid_param():
    testutils.assert_raises_typeerror(milestone_api, 'get_specific', id=1)


def test_get_specific(new_milestone):
    retrieved = milestone_api.get_specific(new_milestone.id).content
    assert new_milestone.to_dict() == retrieved.to_dict()


def test_update_no_id():
    testutils.assert_raises_valueerror(milestone_api, 'update', id=None)


def test_update_invalid_param():
    testutils.assert_raises_typeerror(milestone_api, 'update', id=1)


def test_update(new_milestone):
    new_milestone.download_url = "updatedUrlHere"
    milestone_api.update(id=new_milestone.id, body=new_milestone)
    updated = milestone_api.get_specific(new_milestone.id).content
    assert updated.to_dict() == new_milestone.to_dict()


