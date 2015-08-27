import random
import string
from pnc import products

def _create_product():
    randname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    return products.create_product(randname)

def test_list_products():
    pass

def test_list_products_attribute():
    pass

def test_create_product():
    pass

def test_get_product():
    pass

def test_update_product():
    pass

def test_list_versions_for_product():
    pass

def test_create_product_version():
    pass

def test_product_exists():
    pass

def test_get_product_id_by_name():
    pass

