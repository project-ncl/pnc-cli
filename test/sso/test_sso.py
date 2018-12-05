from pnc_cli import makemead
import random
import string

def test_sso():
    makemead.make_mead(config="configs/sso.cfg", product_name="sso", product_version="7.1", run_build=True, suffix=get_suffix())

def get_suffix():
    return "-" + ''.join(random.choice(string.ascii_uppercase + string.digits)
                         for _ in range(10))
