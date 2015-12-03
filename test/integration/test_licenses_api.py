import pytest
from pnc_cli import licenses
from pnc_cli.swagger_client.apis.licenses_api import LicensesApi
from pnc_cli import utils
from test import testutils

licenses_api = LicensesApi(utils.get_api_client())


@pytest.fixture(scope='function')
def new_license(request):
    license = licenses_api.create_new(body=licenses._create_license_object(full_name=testutils.gen_random_name(),
                                                                           full_content="pnc_cli-cli test license")).content

    def teardown():
        existing_licenses = licenses_api.get_all(page_size=1000000).content
        if existing_licenses and license.id in [x.id for x in existing_licenses]:
            licenses_api.delete(id=license.id)

    request.addfinalizer(teardown)
    return license


def test_get_all_invalid_param():
    testutils.assert_raises_typeerror(licenses_api, 'get_all')


def test_get_all(new_license):
    # empty at first. create one to test.
    l = licenses_api.get_all(page_index=0, page_size=1000000, sort='', q='').content
    assert l is not None


def test_create_new_invalid_param():
    testutils.assert_raises_typeerror(licenses_api, 'create_new')


def test_create_new(new_license):
    license_ids = [x.id for x in licenses_api.get_all(page_size=1000000).content]
    assert new_license.id in license_ids


def test_get_specific_no_id():
    testutils.assert_raises_valueerror(licenses_api, 'get_specific', id=None)


def test_get_specific_invalid_param():
    testutils.assert_raises_typeerror(licenses_api, 'get_specific', id=1)


def test_get_specific(new_license):
    assert licenses_api.get_specific(new_license.id) is not None


def test_update_no_id():
    testutils.assert_raises_valueerror(licenses_api, 'update', id=None)


def test_update_invalid_param():
    testutils.assert_raises_typeerror(licenses_api, 'update', id=1)


def test_update(new_license):
    licenses_api.update(id=new_license.id, body=licenses._create_license_object(full_name='PNC-CLI updated license',
                                                                                full_content='updated content'))
    updated_license = licenses_api.get_specific(new_license.id).content
    assert updated_license.full_name == 'PNC-CLI updated license' and updated_license.full_content == 'updated content'


def test_delete_no_id():
    testutils.assert_raises_valueerror(licenses_api, 'delete', id=None)


def test_delete_invalid_param():
    testutils.assert_raises_typeerror(licenses_api, 'delete', id=1)


def test_delete(new_license):
    assert new_license.id in [x.id for x in licenses_api.get_all(page_size=1000000).content]
    licenses_api.delete(new_license.id)
    existing = licenses_api.get_all(page_size=1000000).content
    if existing:
        assert new_license.id not in [x.id for x in existing]
    else:
        assert not existing


