import logging
import os
import re
import sys
import time
from ConfigParser import Error
from ConfigParser import NoSectionError

from argh import arg

import pnc_cli.utils as utils
from pnc_cli import bpmbuildconfigurations
from pnc_cli import buildconfigurations
from pnc_cli import buildconfigurationsets
from pnc_cli import environments
from pnc_cli import products
from pnc_cli import productversions
from pnc_cli import projects
from pnc_cli import repositoryconfigurations
from pnc_cli.buildconfigurations import get_build_configuration_by_name
from pnc_cli.tools.config_utils import ConfigReader


@arg('-c', '--config', help='Make-mead style configuration file possibly extended with pnc.* data fields.')
@arg('-b', '--run_build', help='Run Build')
@arg('-e', '--environment', help='PNC Environment ID')
@arg('-s', '--sufix', help='Adding suffix to artifact\'s name')
@arg('-p', '--product_name', help='Product name')
@arg('-v', '--product_version', help='Product version')
@arg('--look-up-only', help="""You can do a partial import by a config and specify, which Build Configurations
 should be looked up by name. You can specify multiple sections and separate them by comma (no spaces should be included).
 Example: --look-up-only jdg-infinispan
 Will look up jdg-infinispan section and process a look up of BC by name (jdg-infinispan-${version_field}.
""")
def make_mead(config=None, run_build=False, environment=1, sufix="", product_name=None, product_version=None,
              look_up_only=""):
    """
    Create Build group based on Make-Mead configuration file
    :param config: Make Mead config name
    :return:
    """
    ret=make_mead_impl(config, run_build, environment, sufix, product_name, product_version, look_up_only)
    if type(ret) == int and ret != 0:
        sys.exit(ret)
    return ret

def make_mead_impl(config, run_build, environment, sufix, product_name, product_version, look_up_only):
    if not validate_input_parameters(config, product_name, product_version):
        return 1

    try:
        config_reader = ConfigReader(config)
    except NoSectionError as e:
        logging.error('Missing config in %s (%r)', config, e)
        return 1
    except Error, err:
        logging.error(err)
        return 1

    ids = dict()
    (subarts, deps_dict) = config_reader.get_dependency_structure()
    packages = config_reader.get_packages_and_dependencies()
    logging.debug(packages)
    logging.debug(subarts)
    logging.debug(deps_dict)

    product_version_id = get_product_version(product_name, product_version)
    if product_version_id is None:
        return 1

    # Get environment
    env = environments.get_environment_raw(environment)
    if not env:
        logging.error('Environment with id %d not found', environment)
        return 1

    #Create a list for look-up-only
    look_up_only_list = look_up_only.split(",")

    #Lookup or create Build Configuration Set
    target_name = product_name + "-" + product_version + "-all" + sufix
    try:
        bc_set = buildconfigurationsets.get_build_configuration_set_raw(name=target_name)
    except ValueError:
        bc_set = buildconfigurationsets.create_build_configuration_set_raw(name=target_name, product_version_id=product_version_id)
    logging.debug(target_name + ":")
    logging.debug(bc_set.id)

    #Iterate through all sections in configuration file
    for subartifact in subarts:
        art_params = config_reader.get_config(subartifact)
        logging.debug(art_params)
        artifact = art_params['artifact']
        if 'pnc.projectName' in art_params.keys():
            logging.debug("Overriding project name with " + art_params['pnc.projectName'])
            project_name = art_params['pnc.projectName']
        else:
            logging.debug("Using default project name " + artifact)
            project_name = artifact

        logging.debug(art_params)
        package = art_params['package']
        version = art_params['version']
        scm_url = art_params['scmURL']
        (scm_repo_url, scm_revision) = scm_url.split("#", 2)
        artifact_name = package + "-" + re.sub("[\-\.]*redhat\-\d+", "", version) + sufix

        #WA for subfolder builds (? in SCM url)
        if "?" in scm_repo_url:
            folder = scm_repo_url[scm_repo_url.index('?')+1:]
            scm_repo_url = scm_repo_url[:scm_repo_url.index('?')]
            if 'maven_options' not in art_params['options'].keys():
                art_params['options']['maven_options'] = []
            art_params['options']['maven_options'].append("-f./"+folder+"/pom.xml")
            if 'properties' not in art_params['options'].keys():
                art_params['options']['properties'] = {}
            art_params['options']['properties']['exec_folder'] = folder

        # If scm_repo_url starts with git+https protocol, use https protocol instead
        # recent versions of git don't seem to understand 'git+https' anymore
        scm_repo_url = _git_url_use_https_only(scm_repo_url)

        #Lookup or create a Project
        try:
            project = projects.get_project_raw(name=project_name)
        except ValueError:
            logging.debug('No project ' + project_name + ". Creating a new one")
            project = projects.create_project_raw(name=project_name)
        logging.debug(artifact_name + ":")
        logging.debug(project.id)

        #Lookup or update or create Build Config
        build_config = get_build_configuration_by_name(artifact_name)
        if subartifact in look_up_only_list:
            if build_config == None:
                logging.warn("Look up of an existing Build Configuration failed. No build configuration with name " + artifact_name + " found.")
        else:
            if build_config == None:
                logging.debug('No build config with name ' + artifact_name)
                build_config = create_build_configuration(env, bc_set, product_version_id, art_params, scm_repo_url,
                                                          scm_revision, artifact_name, project)
            else:
                build_config = update_build_configuration(env, product_version_id, art_params, scm_repo_url,
                                                          scm_revision, artifact_name, project)

        # Make sure existing configs are added the group
        if build_config is not None and build_config.id not in bc_set.build_configuration_ids:
            buildconfigurationsets.add_build_configuration_to_set(set_id=bc_set.id, config_id=build_config.id)

        if build_config == None:
            return 10

        ids[artifact] = build_config
        logging.debug(build_config.id)

    #Construct dependency tree of Build Configs
    logging.debug(ids)
    for package, dependencies in packages.iteritems():
        for artifact in dependencies:
            bc_id = ids[package]
            subid = ids[artifact]
            logging.debug(bc_id.id, subid.id)
            buildconfigurations.add_dependency(id=bc_id.id, dependency_id=subid.id)

    #Run build if requested
    if run_build:
        build_record = buildconfigurationsets.build_set_raw(id=bc_set.id)
        logging.info("Build started with id %d",build_record.id)

    return utils.format_json(bc_set)

def get_product_version(product_name, product_version):
    products_version = None
    try:
        products_versions = products.list_versions_for_product_raw(name=product_name)
        if products_versions:
            for product in products_versions:
                if product.version == product_version:
                    products_version = product.id
        else:
            logging.debug('Product does not have any versions')
    except ValueError:
        logging.debug('Product version not found')
    if products_version is None:
        p = products.get_product_raw(name=product_name)
        if p is None:
            logging.error('Product not found')
            return None
        pv = productversions.create_product_version_raw(p.id, product_version)
        products_version = pv.id
    return products_version

def validate_input_parameters(config, product_name, product_version):
    valid = True
    if config is None:
        logging.error('Config file --config is not specified.')
        valid = False
    elif not os.path.isfile(config):
        logging.error('Config file %s not found.', os.path.abspath(config))
        valid = False

    if product_name is None:
        logging.error('Product Name --product-name is not specified.')
        valid = False

    if product_version is None:
        logging.error('Product Version --product-version is not specified.')
        valid = False

    return valid

def get_maven_options(params):
    if 'pnc.buildScript' in params.keys():
        return params['pnc.buildScript']

    result = "mvn clean deploy"

    if 'goals' in params['options'].keys():
        for goal in params['options']['goals']:
            if goal.strip() != "":
                result += ' %s' % goal
    if 'profiles' in params['options'].keys():
        for profile in params['options']['profiles']:
            if profile.strip() != "":
                result += ' -P%s' % profile
    result += ' -DskipTests'
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
            if prop == "exec_folder":
                result += ' --file=./%s/pom.xml' % value
            elif prop not in not_supported_params:
                result += ' -D%s=%s' % (prop, value)

    return result

def get_generic_parameters(params):
    pme_properties = get_pme_properties(params)
    if pme_properties == "":
        return dict()
    else:
        return str({'CUSTOM_PME_PARAMETERS': pme_properties})


def update_build_configuration(environment, product_version_id, art_params, scm_repo_url, scm_revision, artifact_name, project):
    build_config = buildconfigurations.get_build_configuration_by_name(name=artifact_name)
    internal_url = build_config.repository_configuration.internal_url
    external_url = build_config.repository_configuration.external_url

    scm_repo_url_no_git_ext = _remove_git_ext(scm_repo_url)

    if _remove_git_ext(internal_url) != scm_repo_url_no_git_ext and (external_url is not None and _remove_git_ext(external_url) != scm_repo_url_no_git_ext):
        logging.error("SCM URL of existing Build Configuration '%s' cannot be changed" % artifact_name)
        return None

    buildconfigurations.update_build_configuration_raw(
                                                   id=build_config.id,
                                                   name=artifact_name,
                                                   project=project.id,
                                                   environment=environment.id,
                                                   scm_repo_url=scm_repo_url,
                                                   scm_revision=scm_revision,
                                                   build_script=get_maven_options(art_params),
                                                   product_version_id=product_version_id,
                                                   generic_parameters=get_generic_parameters(art_params))
    return buildconfigurations.get_build_configuration_raw(id=build_config.id)

def create_build_configuration(environment, bc_set, product_version_id, art_params, scm_repo_url,
                               scm_revision, artifact_name, project):

    scm_repo_url_no_git_ext = _remove_git_ext(scm_repo_url)

    repos = repositoryconfigurations.search_repository_configuration_raw(scm_repo_url)
    repo = None
    if repos is not None:
        for r in repos:
            if (_remove_git_ext(r.internal_url) == scm_repo_url_no_git_ext or
                _remove_git_ext(r.external_url) == scm_repo_url_no_git_ext):
                if repo is None:
                    repo = r
                else:
                    logging.error("Ambiguous repository '%s', there are several repository configurations for it."
                           % scm_repo_url)
                    return None


    if repo is None:
        return create_build_configuration_and_repo(environment, bc_set, product_version_id,
                               art_params, scm_repo_url, scm_revision, artifact_name, project)
    else:
        return create_build_configuration_with_repo(environment, bc_set, product_version_id,
                               art_params, repo, scm_revision, artifact_name, project)

def create_build_configuration_with_repo(environment, bc_set, product_version_id, art_params,
                                         repository, scm_revision, artifact_name, project):
    buildconfigurations.create_build_configuration(
                                                   name=artifact_name,
                                                   project=project.id,
                                                   environment=environment.id,
                                                   repository_configuration=repository.id,
                                                   scm_revision=scm_revision,
                                                   build_script=get_maven_options(art_params),
                                                   product_version_id=product_version_id,
                                                   generic_parameters=get_generic_parameters(art_params))
    build_config = get_build_configuration_by_name(artifact_name)
    if build_config == None:
        logging.error("Creation of Build Configuration failed.")
        return None

    logging.info("Build Configuration " + artifact_name + " is created.")
    return build_config

def create_build_configuration_and_repo(environment, bc_set, product_version_id, art_params,
                               scm_repo_url, scm_revision, artifact_name, project):
    bpm_task_id = 0

    #Create BPM build config using post /bpm/tasks/start-build-configuration-creation
    #Set these SCM fields: scmRepoURL and scmRevision
    #Fields scmExternalRepoURL and scmExternalRevision can be optionally filled too
    bpm_task_id = bpmbuildconfigurations.create_build_configuration_process(
                                             repository=scm_repo_url,
                                             revision=scm_revision,
                                             name=artifact_name,
                                             project=project,
                                             environment=environment,
                                             build_script=get_maven_options(art_params),
                                             product_version_id=product_version_id,
                                             dependency_ids = [],
                                             build_configuration_set_ids = [],
                                             generic_parameters=get_generic_parameters(art_params))


    #Using polling every 30s check this endpoint: get /bpm/tasks/{bpm_task_id}
    #until eventType is:
    # BCC_CONFIG_SET_ADDITION_ERROR BCC_CREATION_ERROR BCC_REPO_CLONE_ERROR BCC_REPO_CREATION_ERROR -> ERROR -> end with error
    # BCC_CREATION_SUCCESS  -> SUCCESS
    error_event_types = ("RC_REPO_CREATION_ERROR", "RC_REPO_CLONE_ERROR", "RC_CREATION_ERROR")
    time.sleep(2)
    while True:
        bpm_task = bpmbuildconfigurations.get_bpm_task_by_id(bpm_task_id)

        if contains_event_type(bpm_task.content.events, ("RC_CREATION_SUCCESS", )):
            break

        if contains_event_type(bpm_task.content.events, error_event_types):
            logging.error("Creation of Build Configuration failed")
            logging.error(bpm_task.content)
            return None

        logging.info("Waiting until Build Configuration " + artifact_name + " is created.")
        time.sleep(10)


    #Get BC - GET build-configurations?q='$NAME'
    #Not found-> BC creation failed and the task was garbage collected -> fail
    #Success -> add BC to BCSet and return BC
    build_config = get_build_configuration_by_name(artifact_name)
    if build_config == None:
        logging.error("Creation of Build Configuration failed. Unfortunately the details were garbage collected on PNC side.")
        return None

    logging.info("Build Configuration " + artifact_name + " is created.")
    return build_config


def contains_event_type(events, types):
    for event in events:
        if(event.event_type in types):
            return True

    return False


def _git_url_use_https_only(git_url):
    return re.sub(r'^git\+https', 'https', git_url)

def _remove_git_ext(git_url):
    return re.sub(r'\.git$', '', git_url)
