import random
import string
from pnc import licenses

def _create_license():
    randname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    return licenses.create_license(randname, "PNC-CLI test license")

def test_list_licenses():
    l = licenses.list_licenses()
    assert l is not None

def test_list_licenses_attribute():
    l = licenses.list_licenses(attributes="fullName")
    assert l is not None

def test_create_license():
    new_license = _create_license()
    l = licenses.list_licenses()
    license_ids = [x['id'] for x in l]
    assert new_license['id'] in license_ids

def test_get_license():
    new_license = _create_license()
    assert licenses.get_license(new_license['id']) is not None

def test_delete_license():
    new_license = _create_license()
    licenses.delete_license(new_license['id'])
    l = licenses.list_licenses(attributes='id')
    l_ids = [x['id'] for x in l]
    assert new_license['id'] not in l_ids

def test_update_license():
    new_license = _create_license()
    licenses.update_license(new_license['id'], 'PNC-CLI updated license', 'updated content')
    updated_license = licenses.get_license(new_license['id'])
    assert updated_license['fullName'] == 'PNC-CLI updated license' and updated_license['fullContent'] == 'updated content'


