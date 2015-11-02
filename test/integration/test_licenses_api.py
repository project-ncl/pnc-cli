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
        existing_licenses = licenses_api.get_all().content
        if existing_licenses and license.id in [x.id for x in existing_licenses]:
            licenses_api.delete(id=license.id)
    request.addfinalizer(teardown)
    return license

def test_get_all(new_license):
    # empty at first. create one to test.
    l = licenses_api.get_all().content
    assert l is not None


def test_create_license(new_license):
    license_ids = [x.id for x in licenses_api.get_all().content]
    assert new_license.id in license_ids


def test_get_specific(new_license):
    assert licenses_api.get_specific(new_license.id) is not None


def test_delete(new_license):
    licenses_api.delete(new_license.id)
    assert not licenses_api.get_all().content


def test_update(new_license):
    licenses_api.update(id=new_license.id, body=licenses._create_license_object(full_name='PNC-CLI updated license',                                                                                full_content='updated content'))
    updated_license = licenses_api.get_specific(new_license.id).content
    assert updated_license.full_name == 'PNC-CLI updated license' and updated_license.full_content == 'updated content'
