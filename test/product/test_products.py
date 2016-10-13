from pnc_cli import buildconfigurations
from pnc_cli import buildconfigurationsets
from pnc_cli import projects
import random
import string

def test_sso190():
    sufix = get_sufix()
    set_name = "org.keycloak-keycloak-parent-1.9.0.Final" + sufix
    set = buildconfigurationsets.create_build_configuration_set(name=set_name)
    # RH-SSO 1.9.0
    project = projects.get_project(name="keycloak")
    keycloak_name = "org.keycloak-keycloak-parent-1.9.0.Final-redhat-1" + sufix
    keycloak_config = buildconfigurations.create_build_configuration(
                                                                     name=keycloak_name,
                                                                     project=project.id,
                                                                     environment=1,
                                                                     scm_repo_url="git+ssh://user-pnc-gerrit@pnc-gerrit.pnc.dev.eng.bos.redhat.com:29418/pnc/org.keycloak-keycloak-parent-1.9.0.Final-redhat-1-da.git",
                                                                     scm_revision="branch-1.9.0.Final-redhat-1-pnc-da",
                                                                     build_script="mvn clean deploy -Pdistribution")
    buildconfigurationsets.add_build_configuration_to_set(set_id=set.id, config_id=keycloak_config.id)
    build_record = buildconfigurationsets.build_set(id=set.id)
    assert build_record is not None
    print set.id

def test_sso221():
    sufix = get_sufix()
    set_name = "org.keycloak-keycloak-parent-2.2.1.Final" + sufix
    set = buildconfigurationsets.create_build_configuration_set(name=set_name)
    # freemarker
    project = projects.get_project(name="freemarker")
    freemarker_name = "freemarker-2.3.23.redhat" + sufix
    freemarker_config = buildconfigurations.create_build_configuration(
                                                                       name=freemarker_name,
                                                                       project=project.id,
                                                                       environment=1,
                                                                       scm_repo_url="git+ssh://user-pnc-gerrit@pnc-gerrit.pnc.dev.eng.bos.redhat.com:29418/pnc/freemarker-2.3.23.redhat.git",
                                                                       scm_revision="branch-v2.3.23",
                                                                       build_script="mvn clean deploy -DskipTests")
    buildconfigurationsets.add_build_configuration_to_set(set_id=set.id, config_id=freemarker_config.id)
    # liquibase
    project = projects.get_project(name="liquibase")
    liquibase_name = "liquibase-parent-3.4.1.redhat" + sufix
    liquibase_config = buildconfigurations.create_build_configuration(
                                                                      name=liquibase_name,
                                                                      project=project.id,
                                                                      environment=1,
                                                                      scm_repo_url="git+ssh://user-pnc-gerrit@pnc-gerrit.pnc.dev.eng.bos.redhat.com:29418/pnc/liquibase-parent-3.4.1.redhat.git",
                                                                      scm_revision="branch-liquibase-parent-3.4.1",
                                                                      build_script="mvn -P'!rpm' -pl '!liquibase-debian' clean deploy -DskipTests")
    buildconfigurationsets.add_build_configuration_to_set(set_id=set.id, config_id=liquibase_config.id)
    # twitter4j
    project = projects.get_project(name="twitter4j")
    twitter4j_name = "twitter4j-4.0.4.redhat" + sufix
    twitter4j_config = buildconfigurations.create_build_configuration(
                                                                      name=twitter4j_name,
                                                                      project=project.id,
                                                                      environment=1,
                                                                      scm_repo_url="git+ssh://user-pnc-gerrit@pnc-gerrit.pnc.dev.eng.bos.redhat.com:29418/pnc/twitter4j-4.0.4.redhat.git",
                                                                      scm_revision="branch-4.0.4",
                                                                      build_script="mvn clean deploy -DskipTests")
    buildconfigurationsets.add_build_configuration_to_set(set_id=set.id, config_id=twitter4j_config.id)
    # zxing
    project = projects.get_project(name="zxing")
    zxing_name = "zxing-parent-3.2.1.redhat" + sufix
    zxing_config = buildconfigurations.create_build_configuration(
                                                                  name=zxing_name,
                                                                  project=project.id,
                                                                  environment=1,
                                                                  scm_repo_url="git+ssh://user-pnc-gerrit@pnc-gerrit.pnc.dev.eng.bos.redhat.com:29418/pnc/zxing-parent-3.2.1.redhat.git",
                                                                  scm_revision="branch-zxing-3.2.1",
                                                                  build_script="mvn clean deploy -DskipTests -Drat.numUnapprovedLicenses=2")
    buildconfigurationsets.add_build_configuration_to_set(set_id=set.id, config_id=zxing_config.id)
    # RH-SSO 2.2.1
    project = projects.get_project(name="keycloak")
    keycloak_name = "org.keycloak-keycloak-parent-2.2.1.Final-redhat-1" + sufix
    keycloak_config = buildconfigurations.create_build_configuration(
                                                                  name=keycloak_name,
                                                                  project=project.id,
                                                                  environment=1, 
                                                                  scm_repo_url="git+ssh://user-pnc-gerrit@pnc-gerrit.pnc.dev.eng.bos.redhat.com:29418/pnc/org.keycloak-keycloak-parent-2.2.1.Final-redhat-1-da.git",
                                                                  scm_revision="branch-2.2.1.Final-redhat-1-pnc-da",
                                                                  build_script="mvn clean deploy -Pdistribution -pl '!adapters/oidc/jetty/jetty9.1' -pl '!adapters/oidc/jetty/jetty9.3' -pl '!adapters/oidc/spring-boot' -pl '!adapters/oidc/spring-security' -pl '!adapters/oidc/tomcat/tomcat6' -pl '!adapters/oidc/tomcat/tomcat7' -pl '!adapters/oidc/tomcat/tomcat8' -pl '!adapters/oidc/wildfly/wf8-subsystem' -pl '!adapters/saml/jetty/jetty-core' -pl '!adapters/saml/jetty/jetty8.1' -pl '!adapters/saml/jetty/jetty9.1' -pl '!adapters/saml/jetty/jetty9.2' -pl '!adapters/saml/jetty/jetty9.3' -pl '!adapters/saml/tomcat/tomcat6' -pl '!adapters/saml/tomcat/tomcat7' -pl '!adapters/saml/tomcat/tomcat8' -pl '!distribution/adapters/as7-eap6-adapter/as7-adapter-zip' -pl '!distribution/adapters/tomcat6-adapter-zip' -pl '!distribution/adapters/tomcat7-adapter-zip' -pl '!distribution/adapters/tomcat8-adapter-zip' -pl '!distribution/adapters/jetty81-adapter-zip' -pl '!distribution/adapters/jetty91-adapter-zip' -pl '!distribution/adapters/jetty92-adapter-zip' -pl '!distribution/adapters/jetty93-adapter-zip' -pl '!distribution/adapters/wf8-adapter/wf8-adapter-zip' -pl '!distribution/adapters/wf8-adapter/wf8-modules' -pl '!distribution/api-docs-dist' -pl '!distribution/feature-packs/adapter-feature-pack' -pl '!distribution/demo-dist' -pl '!distribution/examples-dist' -pl '!distribution/proxy-dist' -pl '!distribution/saml-adapters/as7-eap6-adapter/as7-adapter-zip' -pl '!distribution/saml-adapters/tomcat6-adapter-zip' -pl '!distribution/saml-adapters/tomcat7-adapter-zip' -pl '!distribution/saml-adapters/tomcat8-adapter-zip' -pl '!distribution/saml-adapters/jetty81-adapter-zip' -pl '!distribution/saml-adapters/jetty92-adapter-zip' -pl '!distribution/saml-adapters/jetty93-adapter-zip' -pl '!distribution/src-dist' -pl '!model/mongo' -pl '!proxy/proxy-server' -pl '!proxy/launcher/' -pl '!testsuite/proxy' -pl '!testsuite/tomcat6' -pl '!testsuite/tomcat7' -pl '!testsuite/tomcat8' -pl '!testsuite/jetty/jetty81' -pl '!testsuite/jetty/jetty91' -pl '!testsuite/jetty/jetty92' -pl '!testsuite/jetty/jetty93'")
    buildconfigurations.add_dependency(id=keycloak_config.id, dependency_id=liquibase_config.id)
    buildconfigurations.add_dependency(id=keycloak_config.id, dependency_id=twitter4j_config.id)
    buildconfigurations.add_dependency(id=keycloak_config.id, dependency_id=zxing_config.id)
    buildconfigurationsets.add_build_configuration_to_set(set_id=set.id, config_id=keycloak_config.id)
    build_record = buildconfigurationsets.build_set(id=set.id)   
    assert build_record is not None
    print set.id

def test_jdg830er4():
    sufix = get_sufix()
    set_name = "org.infinispan-infinispan-8.3.0.ER4" + sufix
    set = buildconfigurationsets.create_build_configuration_set(name=set_name)
    # JDG Management console 8.3.0.ER4
    project = projects.get_project(name="jdg-management-console")
    jdg_name = "org.infinispan-infinispan-management-console-8.3.0.ER4-redhat-1" + sufix
    build_config = buildconfigurations.create_build_configuration(
                                                                  name=jdg_name,
                                                                  project=project.id,
                                                                  environment=1, 
                                                                  scm_repo_url="git+ssh://user-pnc-gerrit@pnc-gerrit.pnc.dev.eng.bos.redhat.com:29418/pnc/org.infinispan-infinispan-management-console-8.3.0.ER4-redhat-1.git",
                                                                  scm_revision="branch-JDG_7.0.0.ER4_pnc_wa__4",
                                                                  build_script="export NVM_NODEJS_ORG_MIRROR=http://rcm-guest.app.eng.bos.redhat.com/rcm-guest/staging/jboss-dg/node\n\n"
                                                                  + "mvn clean deploy "
                                                                  + "-DnpmDownloadRoot=http://rcm-guest.app.eng.bos.redhat.com/rcm-guest/staging/jboss-dg/node/npm/ "
                                                                  + "-DnodeDownloadRoot=http://rcm-guest.app.eng.bos.redhat.com/rcm-guest/staging/jboss-dg/node/ "
                                                                  + "-DnpmRegistryURL=http://jboss-prod-docker.app.eng.bos.redhat.com:49155")
    
    buildconfigurationsets.add_build_configuration_to_set(set_id=set.id, config_id=build_config.id)
    # JDG Infinispan 8.3.0.ER4
    project = projects.get_project(name="jdg-infinispan")
    jdg_name = "org.infinispan-infinispan-8.3.0.ER4-redhat-1" + sufix
    build_config = buildconfigurations.create_build_configuration(
                                                                  name=jdg_name,
                                                                  project=project.id,
                                                                  environment=1,
                                                                  scm_repo_url="git+ssh://user-pnc-gerrit@pnc-gerrit.pnc.dev.eng.bos.redhat.com:29418/pnc/org.infinispan-infinispan-8.3.0.ER4-redhat-1.git",
                                                                  scm_revision="branch-JDG_7.0.0.ER4_pnc_wa",
                                                                  build_script="mvn clean deploy -DskipTests -Pdistribution")

    buildconfigurationsets.add_build_configuration_to_set(set_id=set.id, config_id=build_config.id)
    build_record = buildconfigurationsets.build_set(id=set.id)
    assert build_record is not None
    print set.id

def test_jdg830ga():
    sufix = get_sufix()
    set_name = "org.infinispan-infinispan-8.3.0.Final" + sufix
    set = buildconfigurationsets.create_build_configuration_set(name=set_name)
    # JDG Management console 8.3.0.GA
    project = projects.get_project(name="jdg-management-console")
    jdg_name = "org.infinispan-infinispan-management-console-8.3.0.Final-redhat-1" + sufix
    build_config = buildconfigurations.create_build_configuration(
                                                                  name=jdg_name,
                                                                  project=project.id,
                                                                  environment=1, 
                                                                  scm_repo_url="git+ssh://user-pnc-gerrit@pnc-gerrit.pnc.dev.eng.bos.redhat.com:29418/pnc/org.infinispan-infinispan-management-console-8.3.0.Final-redhat-1.git",
                                                                  scm_revision="branch-JDG_7.0.0.GA-pnc",
                                                                  build_script="export NVM_NODEJS_ORG_MIRROR=http://rcm-guest.app.eng.bos.redhat.com/rcm-guest/staging/jboss-dg/node\n\n"
                                                                  + "mvn clean deploy "
                                                                  + "-DnpmDownloadRoot=http://rcm-guest.app.eng.bos.redhat.com/rcm-guest/staging/jboss-dg/node/npm/ "
                                                                  + "-DnodeDownloadRoot=http://rcm-guest.app.eng.bos.redhat.com/rcm-guest/staging/jboss-dg/node/ "
                                                                  + "-DnpmRegistryURL=http://jboss-prod-docker.app.eng.bos.redhat.com:49155")

    buildconfigurationsets.add_build_configuration_to_set(set_id=set.id, config_id=build_config.id)
    # JDG Infinispan 8.3.0.GA
    project = projects.get_project(name="jdg-infinispan")
    jdg_name = "org.infinispan-infinispan-8.3.0.Final-redhat-1" + sufix
    build_config = buildconfigurations.create_build_configuration(
                                                                  name=jdg_name,
                                                                  project=project.id,
                                                                  environment=1, 
                                                                  scm_repo_url="git+ssh://user-pnc-gerrit@pnc-gerrit.pnc.dev.eng.bos.redhat.com:29418/pnc/org.infinispan-infinispan-8.3.0.Final-redhat-1.git",
                                                                  scm_revision="branch-JDG_7.0.0.GA-pnc",
                                                                  build_script="mvn clean deploy -DskipTests -Pdistribution")

    buildconfigurationsets.add_build_configuration_to_set(set_id=set.id, config_id=build_config.id)
    build_record = buildconfigurationsets.build_set(id=set.id)   
    assert build_record is not None
    print set.id

def test_eap703ga():
    # EAP 7.0.3.GA
    sufix = get_sufix()
    set_name = "org.jboss.eap-jboss-eap-parent-7.0.3.GA" + sufix
    set = buildconfigurationsets.create_build_configuration_set(name=set_name)
    project = projects.get_project(name="eap7")
    eap_name = "org.jboss.eap-jboss-eap-parent-7.0.3.GA-redhat-2" + sufix
    build_config = buildconfigurations.create_build_configuration(
                                                                  name=eap_name,
                                                                  project=project.id,
                                                                  environment=1,
                                                                  scm_repo_url="git+ssh://user-pnc-gerrit@pnc-gerrit.pnc.dev.eng.bos.redhat.com:29418/pnc/org.jboss.eap-jboss-eap-parent-7.0.3.GA-redhat-2.git",
                                                                  scm_revision="branch-7.0.3.GA-redhat-2-pnc",
                                                                  build_script="mvn clean deploy -Prelease")

    buildconfigurationsets.add_build_configuration_to_set(set_id=set.id, config_id=build_config.id)
    build_record = buildconfigurationsets.build_set(id=set.id)
    assert build_record is not None
    print set.id

def test_eap710():
    # EAP 7.1.0.Alpha
    sufix = get_sufix()
    set_name = "org.jboss.eap-jboss-eap-parent-7.1.0.Alpha1" + sufix
    set = buildconfigurationsets.create_build_configuration_set(name=set_name)
    project = projects.get_project(name="eap7")
    eap_name = "org.jboss.eap-jboss-eap-parent-7.1.0.Alpha1-redhat-7" + sufix
    build_config = buildconfigurations.create_build_configuration(
                                                                  name=eap_name,
                                                                  project=project.id,
                                                                  environment=1,
                                                                  scm_repo_url="git+ssh://user-pnc-gerrit@pnc-gerrit.pnc.dev.eng.bos.redhat.com:29418/pnc/org.jboss.eap-jboss-eap-parent-7.1.0.Alpha1-redhat-7.git",
                                                                  scm_revision="branch-7.1.0.Alpha1-redhat-7",
                                                                  build_script="mvn clean deploy -Prelease -DskipTests=true")

    buildconfigurationsets.add_build_configuration_to_set(set_id=set.id, config_id=build_config.id)
    build_record = buildconfigurationsets.build_set(id=set.id)
    assert build_record is not None
    print set.id

def get_sufix():
    return "-" + ''.join(random.choice(string.ascii_uppercase + string.digits)
                         for _ in range(10))