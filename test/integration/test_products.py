import random
import string
from pnc import products, productversions

def _create_product():
    randname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    return products.create_product(randname)

def test_list_products():
    p = products.list_products()
    assert p is not None

def test_list_products_attribute():
    p = products.list_products(attributes="name")
    assert p is not None

def test_create_product():
    new_prod = _create_product()
    prod_ids = [x['id'] for x in products.list_products()]
    assert new_prod['id'] in prod_ids

def test_get_product():
    new_prod = _create_product()
    assert products.get_product(id=new_prod['id']) is not None

def test_update_product():
    new_prod = _create_product()
    products.update_product(new_prod['id'], 'updated product name', 'updated description')
    updated_prod = products.get_product(id=new_prod['id'])
    assert updated_prod['name'] == 'updated product name' and updated_prod['description'] == 'updated description'

def test_list_versions_for_product():
    randversion = random.choice(string.digits)+'.'+random.choice(string.digits)
    new_prod = _create_product()
    productversions.create_product_version(new_prod['id'], randversion)
    versions = [x['version'] for x in products.list_versions_for_product(id=new_prod['id'])]
    assert versions is not None and randversion in versions

def test_list_versions_for_product_attributes():
    randversion = random.choice(string.digits)+'.'+random.choice(string.digits)
    new_prod = _create_product()
    productversions.create_product_version(new_prod['id'], randversion)
    versions = [x['version'] for x in products.list_versions_for_product(id=new_prod['id'])]
    assert versions is not None and randversion in versions

def test_product_exists():
    new_prod = _create_product()
    assert products._product_exists(new_prod['id'])

def test_get_product_id_by_name():
    new_prod = _create_product()
    assert products._product_exists(products._get_product_id_by_name(new_prod['name']))

