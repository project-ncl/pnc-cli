import random
import string
from pnc import licenses

def _create_license_obj(name, content):
    return licenses._create_license_object(name, content)

def _create_license():
    randname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    new_license = licenses._create_license_object(randname, "pnc-cli test license")
    return licenses.create(new_license).json()

def test_get_all():
    l = licenses.get_all().json()
    assert l is not None

def test_create_license():
    new_license = _create_license()
    l = licenses.get_all().json()
    license_ids = [x['id'] for x in l]
    assert new_license['id'] in license_ids

def test_get_specific():
    new_license = _create_license()
    assert licenses.get_specific(new_license['id']) is not None

def test_delete():
    new_license = _create_license()
    licenses.delete(new_license['id'])
    l = licenses.get_all().json()
    l_ids = [x['id'] for x in l]
    assert new_license['id'] not in l_ids

def test_update():
    new_license = _create_license()
    licenses.update(new_license['id'], _create_license_obj('PNC-CLI updated license', 'updated content'))
    updated_license = licenses.get_specific(new_license['id']).json()
    assert updated_license['fullName'] == 'PNC-CLI updated license' and updated_license['fullContent'] == 'updated content'


