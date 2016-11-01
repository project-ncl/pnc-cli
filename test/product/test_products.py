from pnc_cli import makemead
import random
import string

def test_eap():
    makemead.make_mead(config="cfg/eap.cfg", cproject=True)

def test_sso():
    makemead.make_mead(config="cfg/sso.cfg", cproject=True)

def test_jdg():
    makemead.make_mead(config="cfg/jdg.cfg", cproject=True)

def get_sufix():
    return "-" + ''.join(random.choice(string.ascii_uppercase + string.digits)
                         for _ in range(10))