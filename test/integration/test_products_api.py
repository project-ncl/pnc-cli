import random
import utils
import string
from pnc import products
from swagger_client.apis.products_api import ProductsApi

api = ProductsApi(utils.get_api_client())

def _create_product():
    randname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    return api.create_new(products._create_product_object(name=randname))

def test_list_products():
    p = api.get_all().json()
    assert p is not None

def test_create_product():
    new_prod = _create_product()
    prod_ids = [x['id'] for x in products.get_all()]
    assert new_prod['id'] in prod_ids

def test_get_product():
    new_prod = _create_product()
    assert products.get_specific(new_prod['id']).json() is not None

def test_update_product():
    new_prod = _create_product()
    products.update(new_prod['id'], products._create_product_object(name='updated product name', description='updated description'))
    updated_prod = products.get_specific(new_prod['id']).json()
    assert updated_prod['name'] == 'updated product name' and updated_prod['description'] == 'updated description'

def test_list_versions_for_product():
    randversion = random.choice(string.digits)+'.'+random.choice(string.digits)
    new_prod = _create_product()
    productversions.create(productversions.create_product_version_object(productId=new_prod['id'],version=randversion))
    versions = [x['version'] for x in products.get_product_versions(new_prod['id']).json()]
    assert versions is not None and randversion in versions

def test_product_exists():
    new_prod = _create_product()
    assert products.product_exists(new_prod['id'])

def test_get_product_id_by_name():
    new_prod = _create_product()
    assert products.product_exists(products.get_product_id_by_name(new_prod['name']))

