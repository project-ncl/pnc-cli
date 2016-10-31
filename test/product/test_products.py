from pnc_cli import buildconfigurations
from pnc_cli import buildconfigurationsets
from pnc_cli import makemead
from pnc_cli import projects
import random
import string

def test_eap():
    # EAP 7.0.3.GA
    sufix = get_sufix()
    set_name = "jb-eap-7.0-rhel-7-candidate" + sufix
    set = buildconfigurationsets.create_build_configuration_set(name=set_name)
    project = projects.get_project(name="eap7")
    eap_name = "org.jboss.eap-jboss-eap-parent-7.0.3.GA-redhat-2" + sufix
    build_config = buildconfigurations.create_build_configuration(
                                                                  name=eap_name,
                                                                  project=project.id,
                                                                  environment=1,
                                                                  scm_repo_url="git+ssh://user-pnc-gerrit@pnc-gerrit.pnc.dev.eng.bos.redhat.com:29418/pnc/org.jboss.eap-jboss-eap-parent-7.0.3.GA-redhat-2.git",
                                                                  scm_revision="branch-7.0.3.GA-redhat-2-pnc",
                                                                  build_script="mvn clean deploy -DskipTests -Prelease")

    buildconfigurationsets.add_build_configuration_to_set(set_id=set.id, config_id=build_config.id)
    build_record = buildconfigurationsets.build_set(id=set.id)
    assert build_record is not None
    print set.id

def test_eap71():
    # EAP 7.1.0.Alpha
    sufix = get_sufix()
    set_name = "jb-eap-7.1-rhel-7-candidate" + sufix
    set = buildconfigurationsets.create_build_configuration_set(name=set_name)
    project = projects.get_project(name="eap7")
    eap_name = "org.jboss.eap-jboss-eap-parent-7.1.0.Alpha1-redhat-8" + sufix
    build_config = buildconfigurations.create_build_configuration(
                                                                  name=eap_name,
                                                                  project=project.id,
                                                                  environment=1,
                                                                  scm_repo_url="git+ssh://user-pnc-gerrit@pnc-gerrit.pnc.dev.eng.bos.redhat.com:29418/pnc/org.jboss.eap-jboss-eap-parent-7.1.0.Alpha1-redhat-8.git",
                                                                  scm_revision="branch-EAP_7.1.0.DR7",
                                                                  build_script="mvn clean deploy -DskipTests=true -Prelease")

    buildconfigurationsets.add_build_configuration_to_set(set_id=set.id, config_id=build_config.id)
    build_record = buildconfigurationsets.build_set(id=set.id)
    assert build_record is not None
    print set.id

def test_cfg_sso():
    makemead.make_mead(config="cfg/sso.cfg", artifact=None)

def test_cfg_jdg():
    makemead.make_mead(config="cfg/jdg.cfg", artifact=None)

def get_sufix():
    return "-" + ''.join(random.choice(string.ascii_uppercase + string.digits)
                         for _ in range(10))