from pnc_cli import makemead
import random
import string

def test_eap():
    makemead.make_mead(config="cfg/eap.cfg", product_name="eap", product_version="7.1", sufix=get_sufix())

def test_sso():
    makemead.make_mead(config="cfg/sso.cfg", product_name="sso", product_version="7.1", run_build=True, sufix=get_sufix())

def test_jdg():
    makemead.make_mead(config="cfg/jdg.cfg", product_name="jdg", product_version="7.1", run_build=True, sufix=get_sufix())

def get_sufix():
    return "-" + ''.join(random.choice(string.ascii_uppercase + string.digits)
                         for _ in range(10))