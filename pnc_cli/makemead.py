from ConfigParser import Error
from ConfigParser import NoSectionError
import logging
import os
from pprint import pprint
import re

from argh import arg
from pnc_cli import buildconfigurations, bpmbuildconfigurations
from pnc_cli import buildconfigurationsets
from pnc_cli import products
from pnc_cli import projects
from pnc_cli import utils
from pnc_cli.bpmbuildconfigurations import create_bpm_build_configuration
from pnc_cli.swagger_client import BpmApi
from tools.config_utils import ConfigReader


@arg('-c', '--config', help='Configuration file to use to drive the build')
@arg('-b', '--run_build', help='Run Build')
@arg('-e', '--environment', help='Environment ID')
@arg('-s', '--sufix', help='Adding sufix to artifact\'s name')
@arg('-p', '--product_name', help='Product name')
@arg('-v', '--product_version', help='Product version')
@arg('--external', help="""If bc_set the SCM URLs are considered as external and therefore the repositories will be forked to Gerrit
 and the user MUST update the config file with the new values for next runs""")
def make_mead(config=None, run_build=None, environment=1, sufix="", product_name=None, product_version=None, external = False):
    """
    Create Make Mead configuration
    :param config: Make Mead config name
    :return:
    """    
    if validate_input_parameters(config, product_name, product_version) != 0:
        return 1

    try:
        config_reader = ConfigReader(config)
    except NoSectionError as e:
        logging.error('Missing config in %s (%r)', config, e)
        print '-c false'
        return 1
    except Error, err:
        logging.error(err)
        print '-c false'
        return 1

    bc_set = None
    product_version_id = None
    ids = dict()
    (subarts, deps_dict) = config_reader.get_dependency_structure()
    packages = config_reader.get_packages_and_dependencies()
    pprint(packages)
    logging.debug(subarts)
    logging.debug(deps_dict)

    try:
        products_versions = products.list_versions_for_product(name=product_name)
        for product in products_versions:
            if product.version == product_version:
                product_version_id = product.id
    except ValueError:
        logging.error('Product version not found')
        return 1

    for subartifact in subarts:
        art_params = config_reader.get_config(subartifact)
        logging.debug(art_params)
        if 'pnc.projectName' in art_params.keys():
            logging.debug("Overriding project name with " + art_params['pnc.projectName'])
            pprint("Overriding project name with " + art_params['pnc.projectName'])
            artifact = art_params['pnc.projectName']
        else:
            logging.debug("Using default project name " + art_params['artifact'])
            pprint("Using default project name " + art_params['artifact'])
            artifact = art_params['artifact']
            
        logging.debug(art_params)
        package = art_params['package']
        version = art_params['version']
        scm_url = art_params['scmURL']
        (scm_repo_url, scm_revision) = scm_url.split("#", 2)
        artifact_name = package + "-" + re.sub("[\-\.]*redhat\-\d+", "", version) + sufix
        target_name = product_name + "-" + product_version + "-all" + sufix

        if bc_set is None:
            try:
                bc_set = buildconfigurationsets.get_build_configuration_set(name=target_name)
            except ValueError:
                bc_set = buildconfigurationsets.create_build_configuration_set(name=target_name, product_version_id=product_version_id)
            logging.debug(target_name + ":")
            logging.debug(bc_set.id)

        try:
            project = projects.get_project(name=artifact)        
        except ValueError:
            logging.debug('No project ' + artifact + ". Creating a new one")
            project = projects.create_project(name=artifact)
        logging.debug(artifact_name + ":")
        logging.debug(project.id)

        try:
            build_config = update_build_configuration(environment, product_version_id, art_params, scm_repo_url, 
                                                      scm_revision, artifact_name, project)
        except ValueError:
            logging.debug('No build config with name ' + artifact_name)
            build_config = create_build_configuration(environment, bc_set, product_version_id, art_params, scm_repo_url, 
                                                      scm_revision, artifact_name, project)
            
        ids[artifact] = build_config
        logging.debug(build_config.id)
        
    logging.debug(ids)
    for package, dependencies in packages.iteritems():
        for artifact in dependencies:
            id = ids[package]
            subid = ids[artifact]
            logging.debug(id.id, subid.id)
            buildconfigurations.add_dependency(id=id.id, dependency_id=subid.id)

    if run_build is not None:
        build_record = buildconfigurationsets.build_set(id=bc_set.id)
        pprint(build_record)

    return bc_set

def validate_input_parameters(config, product_name, product_version):
    if config is None:
        logging.error('Config file --config is not specified.')
        return 1

    if product_name is None:
        logging.error('Product Name --product-name is not specified.')
        return 1

    if product_version is None:
        logging.error('Product Version --product-version is not specified.')
        return 1

    if not os.path.isfile(config):
        logging.error('Config file %s not found.', os.path.abspath(config))
        return 1
    
    return 0
    
def get_maven_options(params):
    result = ""

    if 'profiles' in params['options'].keys():
        for profile in params['options']['profiles']:
            if profile.strip() != "":
                result += ' -P%s' % profile
    if 'maven_options' in params['options'].keys():
        for maven_option in params['options']['maven_options']:
            if maven_option == '-pl':
                result += ' %s' % maven_option
            else:
                result += ' \'%s\'' % maven_option

    return result

def get_pme_properties(params):
    not_supported_params = ("strictAlignment", "version.suffix", "overrideTransitive")
    result = ""

    if 'properties' in params['options'].keys():
        for prop in sorted(list(params['options']['properties'].keys())):
            value = params['options']['properties'][prop]
            if prop not in not_supported_params:
                result += ' -D%s=%s' % (prop, value)

    return result 

def get_generic_parameters(params):
    pme_properties = get_pme_properties(params)
    if pme_properties == "":
        return dict()
    else:
        return {'CUSTOM_PME_PARAMETERS': pme_properties}
    
    
def update_build_configuration(environment, product_version_id, art_params, scm_repo_url, scm_revision, artifact_name, project):
    build_config_id = buildconfigurations.get_build_configuration_id_by_name(name=artifact_name)
    buildconfigurations.update_build_configuration(
                                                   id=build_config_id,
                                                   name=artifact_name,
                                                   project=project.id,
                                                   environment=environment, 
                                                   scm_repo_url=scm_repo_url,
                                                   scm_revision=scm_revision,
                                                   build_script="mvn clean deploy -DskipTests" + get_maven_options(art_params),
                                                   product_version_id=product_version_id,
                                                   generic_parameters=get_generic_parameters(art_params))
    return buildconfigurations.get_build_configuration(id=build_config_id)

def create_build_configuration(environment, bc_set, product_version_id, art_params, scm_repo_url, 
                               scm_revision, artifact_name, project):
    build_config = buildconfigurations.create_build_configuration(name=artifact_name, 
        project=project.id, 
        environment=environment, 
        scm_repo_url=scm_repo_url, 
        scm_revision=scm_revision, 
        build_script="mvn clean deploy -DskipTests" + get_maven_options(art_params), 
        product_version_id=product_version_id, 
        generic_parameters=get_generic_parameters(art_params))
    buildconfigurationsets.add_build_configuration_to_set(set_id=bc_set.id, config_id=build_config.id)
    return build_config


