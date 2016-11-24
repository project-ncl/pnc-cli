from pnc_cli import makemead
import random
import string

def test_eap():
    makemead.make_mead(config="cfg/eap.cfg", sufix=get_sufix())

def test_sso():
    makemead.make_mead(config="cfg/sso.cfg", run_build=True, sufix=get_sufix())

def test_jdg():
    makemead.make_mead(config="cfg/jdg.cfg", run_build=True, sufix=get_sufix())

def get_sufix():
    return "-" + ''.join(random.choice(string.ascii_uppercase + string.digits)
                         for _ in range(10))