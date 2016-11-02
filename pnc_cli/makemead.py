from ConfigParser import Error
from ConfigParser import NoSectionError
from argh import arg
import logging
import os
from pnc_cli import buildconfigurations
from pnc_cli import buildconfigurationsets
from pnc_cli import projects
from pprint import pprint
import random
import string
from tools.config_utils import ConfigReader

@arg('-c', '--config', help='Configuration file to use to drive the build')
@arg('-p', '--cproject', help='Create project if needed')
@arg('-s', '--sufix', help='Adding sufix to artifact\'s name')
def make_mead(config="cfg/builder.cfg", cproject=None, sufix=""):
    """
    Create Make Mead configuration
    :param config: Make Mead config name
    :return:
    """    
    if not os.path.isfile(config):
        logging.error('Config file %s not found.', os.path.abspath(config))
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

    set = None
    ids = dict()
    (subarts, deps_dict) = config_reader.get_dependency_structure()
    packages = config_reader.get_packages_and_dependencies()
    pprint(packages)
    logging.debug(subarts)
    logging.debug(deps_dict)
    for subartifact in subarts:
        art_params = config_reader.get_config(subartifact)
        logging.debug(art_params)
        artifact = art_params['artifact']
        package = art_params['package']
        version = art_params['version']
        scm_url = art_params['scmURL']
        target = art_params['target']
        (scm_repo_url, scm_revision) = scm_url.split("#", 2)
        artifact_name = package + "-" + version + sufix
        target_name = target + sufix
        if set is None:
            set = buildconfigurationsets.create_build_configuration_set(name=target_name)
            logging.debug(target_name + ":")
            logging.debug(set.id)
        try:
            project = projects.get_project(name=artifact)        
        except ValueError:
            logging.error('No project ' + artifact)
            if cproject is None:
                return 1
            else:
                project = projects.create_project(name=artifact)
        build_config = buildconfigurations.create_build_configuration(
                                                                      name=artifact_name,
                                                                      project=project.id,
                                                                      environment=1, 
                                                                      scm_repo_url=scm_repo_url,
                                                                      scm_revision=scm_revision,
                                                                      build_script="mvn clean deploy -DskipTests" + get_maven_options(art_params))
        buildconfigurationsets.add_build_configuration_to_set(set_id=set.id, config_id=build_config.id)
        ids[artifact] = build_config
        logging.debug(artifact_name + ":")
        logging.debug(build_config.id)
    logging.debug(ids)
    for package, dependencies in packages.iteritems():
        for artifact in dependencies:
            id = ids[package]
            subid = ids[artifact]
            logging.debug(id.id, subid.id)
            buildconfigurations.add_dependency(id=id.id, dependency_id=subid.id)
    build_record = buildconfigurationsets.build_set(id=set.id)

    return build_record

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
    if 'properties' in params['options'].keys():
        for prop in sorted(list(params['options']['properties'].keys())):
            value = params['options']['properties'][prop]
            result += ' -D%s=%s' % (prop, value)
    return result
