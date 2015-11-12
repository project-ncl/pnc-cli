__author__ = 'thauser'
import pytest
from pnc_cli.swagger_client.apis import BuildrecordsetsApi
from pnc_cli import buildrecordsets
from pnc_cli import utils
from test import testutils

brs_api = BuildrecordsetsApi(utils.get_api_client())


@pytest.fixture(scope='function')
def new_brs(request):
    set = brs_api.create_new(body=buildrecordsets.create_buildrecordset_object(
        build_records_ids=[1, 2]
    )).content
    def teardown():
        existing = [x.id for x in brs_api.get_all().content]
        if set.id in existing:
            brs_api.delete_specific(id=set.id)
    request.addfinalizer(teardown)
    return set


def test_get_all_invalid_param():
    testutils.assert_raises_typeerror(brs_api, 'get_all')


def test_get_all():
    response = brs_api.get_all(page_index=0, page_size=1000, sort='', q='').content
    assert response is not None


def test_create_new_invalid_param():
    testutils.assert_raises_typeerror(brs_api, 'create_new')


def test_create_new(new_brs):
    existing = [x.id for x in brs_api.get_all().content]
    assert new_brs.id in existing


def test_get_all_for_build_record_no_record_id():
    testutils.assert_raises_valueerror(brs_api, 'get_all_for_build_record', record_id=None)


def test_get_all_for_build_record_invalid_param():
    testutils.assert_raises_typeerror(brs_api, 'get_all_for_build_record', record_id=1)


def test_get_all_for_build_record():
    response = brs_api.get_all_for_build_record(record_id=1, page_index=0, page_size=1000, sort='', q='').content
    assert response is not None


def test_get_all_for_product_milestone_no_version_id():
    testutils.assert_raises_valueerror(brs_api, 'get_all_for_product_milestone', version_id=None)


def test_get_all_for_product_milestone_invalid_param():
    testutils.assert_raises_typeerror(brs_api, 'get_all_for_product_milestone', version_id=1)


def test_get_all_for_product_milestone():
    response = brs_api.get_all_for_product_milestone(version_id=1).content
    assert response is not None


def test_get_specific_no_id():
    testutils.assert_raises_valueerror(brs_api, 'get_specific', id=None)


def test_get_specific_invalid_param():
    testutils.assert_raises_typeerror(brs_api, 'get_specific', id=1)


def test_get_specific(new_brs):
    response = brs_api.get_specific(id=new_brs.id).content
    assert response is not None


def test_update_no_id():
    testutils.assert_raises_valueerror(brs_api, 'update', id=None)


def test_update_invalid_param():
    testutils.assert_raises_typeerror(brs_api, 'update', id=1)


def test_update(new_brs):
    new_brs.build_record_ids = []
    brs_api.update(id=new_brs.id, body=new_brs)
    updated = brs_api.get_specific(id=new_brs.id).content
    assert updated.to_dict() == new_brs.to_dict()


def test_delete_specific_no_id():
    testutils.assert_raises_valueerror(brs_api, 'delete_specific', id=None)


def test_delete_specific_invalid_param():
    testutils.assert_raises_typeerror(brs_api, 'delete_specific', id=1)


def test_delete_specific(new_brs):
    existing = [x.id for x in brs_api.get_all().content]
    assert new_brs.id in existing
    brs_api.delete_specific(id=new_brs.id)
    existing = [x.id for x in brs_api.get_all().content]
    assert new_brs.id not in existing

