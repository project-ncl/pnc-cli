from argh import arg
from pnc_cli import buildconfigurations
from pnc_cli import buildconfigurationsets
from pnc_cli import projects
import random
import string

@arg("-c", "--config", help="Mead Make Config file")
def make_mead(config="sso.cfg"):
    """
    Create Make Mead configuration
    :param config: Make Mead config name
    :return:
    """
    return config

def sso():
    sufix = get_sufix();
    keycloak_project = "keycloak"
    build_name = keycloak_project + sufix
    project = projects.get_project(name=keycloak_project)
    keycloak_name = "keycloak-parent-2.2.0.Final-redhat-1" + sufix
    build_config = buildconfigurations.create_build_configuration(
                                                                  name=keycloak_name,
                                                                  project=project.id,
                                                                  environment=1,
                                                                  build_script="mvn clean deploy -Pdistribution -pl '!adapters/oidc/jetty/jetty9.1' -pl '!adapters/oidc/jetty/jetty9.3' -pl '!adapters/oidc/spring-boot' -pl '!adapters/oidc/spring-security' -pl '!adapters/oidc/tomcat/tomcat6' -pl '!adapters/oidc/tomcat/tomcat7' -pl '!adapters/oidc/tomcat/tomcat8' -pl '!adapters/oidc/wildfly/wf8-subsystem' -pl '!adapters/saml/jetty/jetty-core' -pl '!adapters/saml/jetty/jetty8.1' -pl '!adapters/saml/jetty/jetty9.1' -pl '!adapters/saml/jetty/jetty9.2' -pl '!adapters/saml/jetty/jetty9.3' -pl '!adapters/saml/tomcat/tomcat6' -pl '!adapters/saml/tomcat/tomcat7' -pl '!adapters/saml/tomcat/tomcat8' -pl '!distribution/adapters/as7-eap6-adapter/as7-adapter-zip' -pl '!distribution/adapters/tomcat6-adapter-zip' -pl '!distribution/adapters/tomcat7-adapter-zip' -pl '!distribution/adapters/tomcat8-adapter-zip' -pl '!distribution/adapters/jetty81-adapter-zip' -pl '!distribution/adapters/jetty91-adapter-zip' -pl '!distribution/adapters/jetty92-adapter-zip' -pl '!distribution/adapters/jetty93-adapter-zip' -pl '!distribution/adapters/wf8-adapter/wf8-adapter-zip' -pl '!distribution/adapters/wf8-adapter/wf8-modules' -pl '!distribution/api-docs-dist' -pl '!distribution/feature-packs/adapter-feature-pack' -pl '!distribution/demo-dist' -pl '!distribution/examples-dist' -pl '!distribution/proxy-dist' -pl '!distribution/saml-adapters/as7-eap6-adapter/as7-adapter-zip' -pl '!distribution/saml-adapters/tomcat6-adapter-zip' -pl '!distribution/saml-adapters/tomcat7-adapter-zip' -pl '!distribution/saml-adapters/tomcat8-adapter-zip' -pl '!distribution/saml-adapters/jetty81-adapter-zip' -pl '!distribution/saml-adapters/jetty92-adapter-zip' -pl '!distribution/saml-adapters/jetty93-adapter-zip' -pl '!distribution/src-dist' -pl '!model/mongo' -pl '!proxy/proxy-server' -pl '!proxy/launcher/' -pl '!testsuite/proxy' -pl '!testsuite/tomcat6' -pl '!testsuite/tomcat7' -pl '!testsuite/tomcat8' -pl '!testsuite/jetty/jetty81' -pl '!testsuite/jetty/jetty91' -pl '!testsuite/jetty/jetty92' -pl '!testsuite/jetty/jetty93'",
                                                                  scm_repo_url="http://git.app.eng.bos.redhat.com/git/keycloak-prod.git",
                                                                  scm_revision="2.2.0.Final-redhat-1-pnc")
                                                                 
    set = buildconfigurationsets.create_build_configuration_set(name=build_name)
    buildconfigurationsets.add_build_configuration_to_set(set_id=set.id, config_id=build_config.id)
    buildconfigurationsets.build_set(id=set.id)
    
    return set.id

def get_sufix():
    return "-" + ''.join(random.choice(string.ascii_uppercase + string.digits)
                         for _ in range(10))