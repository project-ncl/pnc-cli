import random
import string
from pnc_cli import productversions


def create_product_version():
    randversion = random.choice(string.digits) + '.' + random.choice(string.digits)
    return productversions.create_product_version(randversion, )


def test_list_product_versions():
    pass


def test_create_product_version():
    pass


def test_get_product_version():
    pass


def test_update_product_version():
    pass


def test_version_exists():
    pass
