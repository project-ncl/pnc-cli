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
def make_mead(config="builder.cfg"):
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

    #pprint (vars(config_reader))
    set = None
    sufix = get_sufix()
    (subarts, deps_dict) = config_reader.get_dependency_structure()
    for subartifact in subarts:
        art_params = config_reader.get_config(subartifact)
        artifact = art_params['artifact']
        version = art_params['version']
        scm_url = art_params['scmURL']
        (scm_repo_url, scm_revision) = scm_url.split("#", 2)
        #pprint(art_params)
        try:
            project = projects.get_project(name=artifact)        
        except ValueError:
            logging.error('No project ' + artifact)
            return 1
        artifact_name = artifact + "-" + version + sufix
        build_config = buildconfigurations.create_build_configuration(
                                                                      name=artifact_name,
                                                                      project=project.id,
                                                                      environment=1, 
                                                                      scm_repo_url=scm_repo_url,
                                                                      scm_revision=scm_revision,
                                                                      build_script="mvn clean deploy")
        if set is None:
            set = buildconfigurationsets.create_build_configuration_set(name=artifact_name)
            print set.id
        buildconfigurationsets.add_build_configuration_to_set(set_id=set.id, config_id=build_config.id)
        print build_config.id
    build_record = buildconfigurationsets.build_set(id=set.id)
    pprint(build_record)

    return config

def get_sufix():
    return "-" + ''.join(random.choice(string.ascii_uppercase + string.digits)
                         for _ in range(10))
