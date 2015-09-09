import random
import string

from pnc import products
from pnc import productversions
from pnc import utils
from pnc.swagger_client.apis.products_api import ProductsApi
from pnc.swagger_client.apis.productversions_api import ProductversionsApi


product_api = ProductsApi(utils.get_api_client())
versions_api = ProductversionsApi(utils.get_api_client())

def _create_product():
    randname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    return product_api.create_new(body=products._create_product_object(name=randname)).content

def test_get_all():
    p = product_api.get_all().content
    assert p is not None

def test_create_new():
    new_prod = _create_product()
    prod_ids = [x.id for x in product_api.get_all().content]
    assert new_prod.id in prod_ids

def test_get_specific():
    new_prod = _create_product()
    assert product_api.get_specific(id=new_prod.id) is not None

def test_update_product():
    new_prod = _create_product()
    newname = 'newname'.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    product_api.update(id=new_prod.id, body=products._create_product_object(name=newname, description='updated description'))
    updated_prod = product_api.get_specific(id=new_prod.id).content
    assert updated_prod.name == newname and updated_prod.description == 'updated description'

def test_list_versions_for_product():
    randversion = random.choice(string.digits)+'.'+random.choice(string.digits)
    new_prod = _create_product()
    versions_api.create_new_product_version(body=productversions.create_product_version_object(product_id=new_prod.id,version=randversion))
    versions = [x.version for x in product_api.get_product_versions(id=new_prod.id).content]
    assert versions is not None and randversion in versions

def test_get_product_id_by_name():
    new_prod = _create_product()
    assert product_api.get_specific(id=products.get_product_id_by_name(new_prod.name)).content.id == product_api.get_specific(id=new_prod.id).content.id

