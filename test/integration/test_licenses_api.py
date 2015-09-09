import random
import string
from pnc import licenses
from pnc.swagger_client.apis.licenses_api import LicensesApi
from pnc import utils
licenses_api = LicensesApi(utils.get_api_client())

def _create_license():
    randname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    return licenses_api.create_new(body=licenses._create_license_object(full_name=randname, full_content="pnc-cli test license")).content

def test_get_all():
    # empty at first. create one to test.
    l = licenses_api.get_all().content
    assert l is not None

def test_create_license():
    new_license = _create_license()
    license_ids = [x.id for x in licenses_api.get_all().content]
    assert new_license.id in license_ids

def test_get_specific():
    new_license = _create_license()
    assert licenses_api.get_specific(new_license.id) is not None

def test_delete():
    new_license = _create_license()
    licenses_api.delete(new_license.id)
    l_ids = [x.id for x in licenses_api.get_all().content]
    assert new_license.id not in l_ids

def test_update():
    new_license = _create_license()
    licenses_api.update(id=new_license.id, body=licenses._create_license_object(full_name='PNC-CLI updated license', full_content='updated content'))
    updated_license = licenses_api.get_specific(new_license.id).content
    assert updated_license.full_name == 'PNC-CLI updated license' and updated_license.full_content == 'updated content'


