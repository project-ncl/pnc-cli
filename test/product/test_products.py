from pnc_cli import makemead
import random
import string

def test_eap():
    makemead.make_mead(config="cfg/eap.cfg", product_name="Test pnc-cli eap", product_version="7.1", suffix=get_suffix(), external=True)

def test_sso():
    makemead.make_mead(config="cfg/sso.cfg", product_name="Test pnc-cli sso", product_version="7.1", run_build=True, suffix=get_suffix(), external=True)

def test_jdg():
    makemead.make_mead(config="cfg/jdg.cfg", product_name="Test pnc-cli jdg", product_version="7.1", run_build=True, suffix=get_suffix(), external=True)

def get_suffix():
    return "-" + ''.join(random.choice(string.ascii_uppercase + string.digits)
                         for _ in range(10))
