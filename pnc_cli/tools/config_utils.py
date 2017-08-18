# -*- coding: utf-8 -*-

import logging
import os
import re
import string
from ConfigParser import ConfigParser, NoOptionError, NoSectionError, DuplicateSectionError

import utils
from scm_utils import ScmInfo, get_scm_info
from tasks import Tasks


def get_config_option(params, option):
    ret = None
    if option  in params['options'].keys():
        ret = params['options'][option]
    return ret


class ConfigDefaults:
    force = False
    scratch = False
    debug_build = False
    errors_build = False
    pom_manipulator_ext = ''


class ConfigReader:

    common_section = {}
    package_configs = {}
    pom_manipulator_config = {}

    def __init__(self, config_file, config_defaults=ConfigDefaults):
        self.config_file = config_file
        self.config_defaults = config_defaults
        (self.common_section, self.package_configs, self.pom_manipulator_config) = self._do_read_config(config_file, config_defaults.pom_manipulator_ext)
        self.check_config()

    def get_configs(self, artifacts):
        configs = {}
        for artifact in artifacts:
            configs[artifact] = self.get_config(artifact)
        return configs

    def override_config_with_options_prop(self, config, options_properties, config_prop_name, option_prop_name):
        if option_prop_name in options_properties:
            config[config_prop_name] = options_properties[option_prop_name]

    def get_config(self, artifact=None):
        if artifact and artifact not in self.package_configs:
            raise NoSectionError(artifact)

        config = self.common_section.copy()
        config.update(self.pom_manipulator_config.copy())
        if artifact and artifact in self.package_configs:
            config.update(self.package_configs[artifact].copy())

        if self.config_defaults.force:
            config['force'] = self.config_defaults.force

        if self.config_defaults.scratch:
            config['options']['scratch'] = self.config_defaults.scratch

        if self.config_defaults.debug_build:
            config['options']['debug'] = self.config_defaults.debug_build

        if self.config_defaults.errors_build:
            config['options']['errors'] = self.config_defaults.errors_build

        if self.config_defaults.pom_manipulator_ext:
            config['pommanipext'] = self.config_defaults.pom_manipulator_ext

        if not artifact:
            config['artifact'] = None
            config['jobtimeout'] = self.common_section['jobtimeout']
            return config

        config['artifact'] = artifact

        options = config['options']

        if 'properties' not in options:
            options['properties'] = dict()

        options_properties = options['properties']
        if "redhat-" in config['version'] :
           if options['properties'].has_key('versionAddSuffix') and options['properties']['versionAddSuffix'] == 'false':
             logging.info("Skip adding version suffix since versionAddSuffix=false")
           else:
            options['properties'].update (dict({'version.suffix' : "redhat-%s" % re.split(".redhat-", config['version'])[1]}))

        self.override_config_with_options_prop(config, options_properties, 'dependencyManagement', 'dependencyManagement')
        self.override_config_with_options_prop(config, options_properties, 'pluginManagement', 'pluginManagement')
        self.override_config_with_options_prop(config, options_properties, 'propertyManagement', 'propertyManagement')
        self.override_config_with_options_prop(config, options_properties, 'profileInjection', 'profileInjection')
        self.override_config_with_options_prop(config, options_properties, 'repoReportingRemoval', 'repo-reporting-removal')
        self.override_config_with_options_prop(config, options_properties, 'repositoryInjection', 'repositoryInjection')
        self.override_config_with_options_prop(config, options_properties, 'skipDeployment', 'enforce-skip')
        self.override_config_with_options_prop(config, options_properties, 'overrideTransitive', 'overrideTransitive')
        if 'manipulation.disable' not in options_properties:
            if 'dependencyManagement' in config:
                options['properties'].update (dict({'dependencyManagement' : config['dependencyManagement']}))
            if 'pluginManagement' in config:
                options['properties'].update (dict({'pluginManagement' : config['pluginManagement']}))
            if 'propertyManagement' in config:
                options['properties'].update (dict({'propertyManagement' : config['propertyManagement']}))
            if 'repositoryInjection' in config:
                options['properties'].update (dict({'repositoryInjection' : config['repositoryInjection']}))
            if 'profileInjection' in config:
                options['properties'].update (dict({'profileInjection' : config['profileInjection']}))
            if 'repoReportingRemoval' in config:
                options['properties'].update (dict({'repo-reporting-removal' : config['repoReportingRemoval']}))
            if 'skipDeployment' in config:
                options['properties'].update (dict({'enforce-skip' : config['skipDeployment']}))
            if 'overrideTransitive' in config:
                options['properties'].update (dict({'overrideTransitive' : config['overrideTransitive']}))

        #Merge the common section properties into the build properties, do not override if the build has already
        #set the property
        temp = self.common_section['options']['properties'].copy()
        temp.update(options['properties'])
        options['properties'] = temp.copy()
        # Do the same for profiles
        temp = set(self.common_section['options']['profiles'])
        if 'profiles' in options:
            temp.update(options['profiles'])
        options['profiles'] = list(temp)

        return config

    def get_artifact_by_package(self, package_name):
        for artifact, config in self.package_configs.iteritems():
            if package_name == self.package_configs[artifact]['package']:
                return artifact
        return None

    def get_packages_and_dependencies(self):
        packages = {}
        for package, config in self.package_configs.iteritems():
            if 'buildrequires' in config and len(config['buildrequires']) > 0:
                packages[package] = list(config['buildrequires'].split(' '))
            else:
                packages[package] = list()

        return packages

    def get_dependency_structure(self, artifact=None, include_dependencies=False):
        """
        Reads dependency structure. If an artifact is passed in you get only its dependencies otherwise the complete
        structure is returned.

        :param artifact: an artifact task or artifact name if only an artifact's deps are needed
        :param include_dependencies: flag to include also dependencies in returned artifacts and their dependencies in
                                     dependencies dict
        :return: tuple of artifact names list and dependencies dictionary where value is a Task list
        """
        artifacts = []
        dependencies_dict = {}
        if artifact:
            if isinstance(artifact, basestring):
                artifact = self.get_tasks().get_task(artifact)
            artifacts.append(artifact.name)
            dependencies_dict[artifact.name] =  artifact.ordered_dependencies()

            if include_dependencies:
                for dep in dependencies_dict[artifact.name]:
                    artifacts.append(dep.name)
                    dependencies_dict[dep.name] =  dep.ordered_dependencies()
        else:
            for key, task in self.get_tasks().tasks.iteritems():
                artifacts.append(task.name)
                dependencies_dict[task.name] = task.ordered_dependencies()

        return artifacts, dependencies_dict

    def get_tasks(self):
        packages = self.get_packages_and_dependencies()
        tasks = Tasks()
        for package, dependencies in packages.iteritems():
            tasks.add(package, dependencies)

        return tasks

    def get_config_dir(self):
        return utils.get_dir(self.config_file)

    def get_config_name(self):
        base=os.path.basename(self.config_file)
        return os.path.splitext(base)[0]

    def get_all_scm_urls(self):
        scm_urls = {}

        for package, section in self.package_configs:
            logging.debug('Checking section: %s', section)
            if section == "common" \
                    or self.get_config_type(section) == "common"\
                    or self.get_config_type(section) == "bom-builder-meta" :
                logging.debug ('Skipping section %s', section)
                continue
            scm_url = section["scmURL"]
            logging.debug('Got scm_url: %s' % scm_url)
            if scm_url:
                scm_urls[section] = scm_url

        return scm_urls

    def _do_read_section(self, config_path, config_file, package_configs, parser, section):
        # Hack for backwards compatibility. This should really be controlled by the property
        # bom-builder-meta but the older configurations do not have that.
        if set(parser.options(section)) == set(['mapping', 'version']) or set(parser.options(section)) == set(['mapping', 'version', 'package']):
            logging.debug ("Skipping mapping/version section %s" , section)
            return

        section_config = {}
        package_configs[section] = section_config
        section_config['artifact'] = section

        if parser.has_option(section, 'config_type'):
            section_config['config_type'] = parser.get(section, 'config_type')

        if parser.has_option(section, 'buildrequires'):
            section_config['buildrequires'] = parser.get(section, 'buildrequires')

        section_config['package'] = parser.get(section, 'package')
        section_config['version'] = parser.get(section, 'version')
        section_config['substvers'] = string.replace(section_config['version'], "-", "_")
        section_config['scmURL'] = parser.get(section, 'scmURL')
        if parser.has_option(section, 'pnc.buildScript'):
            section_config['pnc.buildScript'] = parser.get(section, 'pnc.buildScript')
        if parser.has_option(section, 'pnc.projectName'):
            section_config['pnc.projectName'] = parser.get(section, 'pnc.projectName')
        if parser.has_option(section, 'skiptests'):
            section_config['skiptests'] = parser.get(section, 'skiptests')
        if parser.has_option(section, 'downstreamjobs'):
            section_config['downstreamjobs'] = parser.get(section, 'downstreamjobs')
        else:
            section_config['downstreamjobs'] = None
        if parser.has_option(section, 'jobtimeout'):
            section_config['jobtimeout'] = parser.getint(section, 'jobtimeout')
        else:
            section_config['jobtimeout'] = parser.getint('common', 'jobtimeout')
        options = {}
        section_config['options'] = options
        maven_options = []
        if parser.has_option(section, 'scratch'):
            options['scratch'] = 'True'
        if parser.has_option(section, 'brewpackage'):
            options['packages'] = [x.strip() for x in parser.get(section, 'brewpackage').split(',')]
        if parser.has_option(section, 'goals'):
            options['goals'] = [x.strip() for x in parser.get(section, 'goals').split(',')]
        if parser.has_option(section, 'jvmOpts'):
            options['jvm_options'] = [x.strip() for x in parser.get(section, 'jvmOpts').split(',')]
        if parser.has_option(section, 'mavenOpts'):
            maven_options = [x.strip() for x in parser.get(section, 'mavenOpts').split(',')]
        if parser.has_option(section, 'errors'):
            options['errors'] = True
        if maven_options:
            options['maven_options'] = maven_options
        if parser.has_option(section, 'debug') or self.config_defaults.debug_build == True:
            options.setdefault('maven_options', []).append ("--debug")
        if parser.has_option(section, 'patches'):
            options['patches'] = parser.get(section, 'patches')
        if parser.has_option(section, 'profiles'):
            options['profiles'] = [x.strip() for x in parser.get(section, 'profiles').split(',')]
        if parser.has_option(section, 'properties'):
            properties = utils.split_unescape(parser.get(section, 'properties').replace("\n", ","), ',', '\\')
            options['properties'] = dict(x.strip().split('=') for x in properties if (x != '' and x != '\\'))
        if parser.has_option(section, 'defaultRepoGroup'):
            options['defaultRepoGroup'] = parser.get(section, 'defaultRepoGroup')

        #If versionOverride=true, then parse the version.override from versions, pass it to pm extension later
        if 'properties' in options and options['properties'].has_key('versionOverride') and options['properties']['versionOverride'] == 'true':
            options['properties']['version.override'] = re.split(".redhat-", section_config['version'])[0]
        #Add project.src.skip option since quickstart don't need source plugin
        if 'properties' in options and options['properties'].has_key('project.src.skip') and options['properties']['project.src.skip'] == 'true':
            options['properties']['project.src.skip'] = 'true'
        # Test for if ip.config.sha exists in the current properties set. If it does and only if the value of 'ip.confgi.sha' is empty, fill it in
        # with the full SHA value.
        if 'properties' in options and options['properties'].has_key('ip.config.sha') and options['properties']['ip.config.sha']=='':
                ipsha = get_scm_info(config_path, read_only=True, filePath=config_file).commit_id
                logging.debug("ip.config.sha updated to %s ", ipsha)
                options['properties']['ip.config.sha'] = ipsha

    # read the config file,and parse the 'from common.cfg import a b,import brms.cfg' line
    def read_and_load(self, include):
        parser = InterpolationConfigParser()
        # pom_manipulator_config1 = {}
        package_configs = parser.defaults()
        config = str(include)
        if config is not "":
          # from .. import ..,import ..
            if config.__contains__(','):
                configs = config.split(',')
                for item in configs:
                    self.parseLine(item, parser, package_configs)
            else:
          # from .. import ..
                self.parseLine(config, parser, package_configs)
        return package_configs


    def parseLine(self, item, parser, package_configs):
         dir = self.get_config_dir()
         include_sections = []
         if item is not "":
            if item.strip().startswith('from'):
                # from x.cfg import xmlpull annotation
                file_section = item.replace('from', '').strip().split('import')
                file = file_section[0].strip()
                config_file = dir + '/' + file
                if len(file_section) != 2:
                    raise SyntaxError("Invalid syntax for include; possible missing import on '%s'" %item)
                if file_section[1].strip().__contains__(' '):
                    section = re.split("\\s+", file_section[1].strip())
                    for sec in section:
                        include_sections.append(sec)
                else:
                    include_sections.append(file_section[1].strip())
            elif item.strip().startswith("import"):
                # import x.cfg
                file = item.replace('import', '').strip()
                config_file = dir + "/" + file
            else:
                raise SyntaxError("Invalid syntax: %s ,Please verify that the syntax is correct " %item)

            parser.read(config_file)
            if os.path.dirname(config_file):
                config_path = os.path.dirname(config_file)
            else:
                config_path = os.getcwd()
                logging.info("Configuration file is %s and path %s", os.path.basename(config_file),
                             +                             config_path)
            if include_sections.__len__() > 0:
                for include_section in include_sections:
                    if include_section is not "":
                        if not parser._sections.get(include_section):
                            raise NoSectionError( "No such %s section exists in %s configuration" % (include_section, file))
                        parser._sections.get(include_section)['buildrequires'] = ''
                        parser._sections.get(include_section)['config_type'] = 'bom-builder-meta'
                        package_configs[include_section] = parser._sections.get(include_section)
            else:
                for section in parser.sections():
                    config_type = self.read_config_type(parser, section)
                    # we need to ignore two bom-builder
                    if section == 'common' or config_type == "bom-builder":
                        logging.debug('Skipping import for section %s', section)
                        continue

                    if not parser._sections.get(section):
                        raise NoSectionError("No such %s section exists in %s configuration" % (section, file))
                    parser._sections.get(section)['buildrequires'] = ''
                    parser._sections.get(section)['config_type'] = 'bom-builder-meta'
                    package_configs[section] = parser._sections.get(section)



    def _do_read_config(self, config_file, pommanipext):
        """Reads config for a single job defined by section."""
        parser = InterpolationConfigParser()
        dataset = parser.read(config_file)
        if config_file not in dataset:
            raise IOError("Config file %s not found." % config_file)
        if parser.has_option('common','include'):
            include = parser.get('common', 'include')
            if include is not "":
                sections_ = self.read_and_load(include)
                for section_ in sections_:
                    if parser.has_section(section_):
                        raise DuplicateSectionError( "The config section [%s] is existed in %s and include %s cfg file" % ( section_, config_file, re.split("\\s+", include.strip())[1]))
                parser._sections.update(sections_)

        pom_manipulator_config = {}
        common_section = {}
        package_configs = {}

        if pommanipext and pommanipext != '' and pommanipext != 'None': #TODO ref: remove none check, it is passed over cmd line in jenkins build
            parse_pom_manipulator_ext(pom_manipulator_config, parser, pommanipext)

        if not parser.has_section('common'):
            logging.error('Mandatory common section missing from configuration file.')
            raise NoSectionError, 'Mandatory common section missing from configuration file.'
        common_section['tag'] = parser.get('common', 'tag')
        common_section['target'] = parser.get('common', 'target')
        common_section['jobprefix'] = parser.get('common', 'jobprefix')
        common_section['jobciprefix'] = parser.get('common', 'jobciprefix')
        common_section['jobjdk'] = parser.get('common', 'jobjdk')
        if parser.has_option('common', 'mvnver'):
            common_section['mvnver'] = parser.get('common', 'mvnver')
        if parser.has_option('common', 'skiptests'):
            common_section['skiptests'] = parser.get('common', 'skiptests')
        if parser.has_option('common', 'base'):
            common_section['base'] = parser.get('common', 'base')
        if parser.has_option('common', 'citemplate'):
            common_section['citemplate'] = parser.get('common', 'citemplate')
        if parser.has_option('common', 'jenkinstemplate'):
            common_section['jenkinstemplate'] = parser.get('common', 'jenkinstemplate')
        if parser.has_option('common', 'product_name'):
            common_section['product_name'] = parser.get('common', 'product_name')

        if parser.has_option('common', 'include'):
            common_section['include'] = parser.get('common', 'include')

        common_section['jobfailureemail'] = parser.get('common', 'jobfailureemail')

        config_dir = utils.get_dir(config_file)

        #Jira
        if parser.has_option('common', 'shared_config') and parser.get('common', 'shared_config') is not "":
            parse_shared_config(common_section, config_dir, parser)

        common_section['jobtimeout'] = parser.getint('common', 'jobtimeout')

        common_section['options'] = {}
        # If the configuration file has global properties insert these into the common properties map.
        # These may be overridden later by particular properties.
        if parser.has_option('common', 'globalproperties'):
            common_section['options']['properties'] = dict(x.strip().split('=') for x in parser.get('common', 'globalproperties').replace(",\n", ",").split(','))
        else:
            # Always ensure properties has a valid dictionary so code below doesn't need multiple checks.
            common_section['options']['properties'] = {}
        # The same for global profiles
        if parser.has_option('common', 'globalprofiles'):
            common_section['options']['profiles'] = [x.strip() for x in parser.get('common', 'globalprofiles').split(',')]
        else:
            # Always ensure profiles has a valid list so code below doesn't need multiple checks.
            common_section['options']['profiles'] = []

        if os.path.dirname(config_file):
            config_path = os.path.dirname(config_file)
        else:
            config_path = os.getcwd()
        logging.info("Configuration file is %s and path %s", os.path.basename(config_file), config_path)

        for section in parser.sections():
            config_type = self.read_config_type(parser, section)
            if section == 'common' or config_type == "bom-builder-meta":
                logging.debug ('Skipping section due to meta-type %s', section)
                continue

            self._do_read_section(config_path, os.path.basename(config_file), package_configs, parser, section)

        return (common_section, package_configs, pom_manipulator_config)

    def is_package_configured(self, package):
        return set(package.split(',')).issubset(self.package_configs)

    def check_config(self):
        for key, task in self.get_tasks().get_all().iteritems():
            self.get_config(task.name)

    def get_package_names_for_sections(self, sections):
        packages = list()
        for section in sections:
            section_config = self.get_config(section)
            packages.append(section_config['package'])
        return packages

    def read_config_type(self, parser, section):
        if parser.has_option(section, 'config_type'):
            config_type = parser.get(section, 'config_type')
        else:
            config_type = 'default'
        return config_type

    def get_config_type(self, section):
        if 'config_type' in section:
            config_type = section['config_type']
        else:
            config_type = 'default'
        return config_type


def read_value_add_version_if_not_present(parser, pommanipext, pommanipext_property):
    # If it already includes an inline version don't append the childversion
    if parser.get(pommanipext, pommanipext_property).count(':') == 2:
        return parser.get(pommanipext, pommanipext_property)
    else:
        if parser.has_option (pommanipext, 'childversion' ):
            logging.warn ("Using childversion instead of version for %s", parser.get(pommanipext, pommanipext_property) + ':' + parser.get(pommanipext, 'version'))
            return parser.get(pommanipext, pommanipext_property) + ':' + parser.get(pommanipext, 'childversion')
        else:
            logging.warn ("Using version instead of childversion for %s", parser.get(pommanipext, pommanipext_property) + ':' + parser.get(pommanipext, 'version'))
            return parser.get(pommanipext, pommanipext_property) + ':' + parser.get(pommanipext, 'version')

def config_has_option(parser, pommanipext, option, warn=True):
    if not parser.has_option(pommanipext, option) or parser.get(pommanipext, option) == '':
        if warn:
            logging.warning('Unable to locate %s property for dependency-management-extension.' % option)
        return False
    else:
        return True


def parse_pom_manipulator_ext(params, parser, pommanipext):
    if not parser.has_section(pommanipext):
        logging.error('Unable to locate dependency-management-section "{0}".'.format(pommanipext))
        raise NoSectionError, 'Unable to locate dependency-management-section "{0}".'.format(pommanipext)

    if config_has_option(parser, pommanipext, 'depmgmt'):
        params['dependencyManagement'] = read_value_add_version_if_not_present(parser, pommanipext, 'depmgmt')

    if config_has_option(parser, pommanipext, 'pluginmgmt'):
        params['pluginManagement'] = read_value_add_version_if_not_present(parser, pommanipext, 'pluginmgmt')

    if config_has_option(parser, pommanipext, 'propertymgmt'):
        params['propertyManagement'] = read_value_add_version_if_not_present(parser, pommanipext, 'propertymgmt')

    if config_has_option(parser, pommanipext, 'repositoryInjection'):
        params['repositoryInjection'] = read_value_add_version_if_not_present(parser, pommanipext, 'repositoryInjection')

    if config_has_option(parser, pommanipext, 'profileinject'):
        params['profileInjection'] = read_value_add_version_if_not_present(parser, pommanipext, 'profileinject')

    if config_has_option(parser, pommanipext, 'repoReportingRemoval'):
        params['repoReportingRemoval'] = parser.get(pommanipext, 'repoReportingRemoval')

    if config_has_option(parser, pommanipext, 'skipDeployment', False):
        params['skipDeployment'] = parser.get(pommanipext, 'skipDeployment')

    if config_has_option(parser, pommanipext, 'overrideTransitive', False):
        params['overrideTransitive'] = parser.get(pommanipext, 'overrideTransitive')

#TODO ref: remove parameters that are not part of config file
def parse_shared_config(common_section, config_dir, parser):
    shared_config_file = parser.get('common', 'shared_config')
    if os.path.isabs(shared_config_file):
        shared_cfg_path = shared_config_file
    else:
        shared_cfg_path = os.path.join(config_dir, shared_config_file)
    common_section['shared_config'] = shared_cfg_path
    if parser.has_option('common', 'jira.project_key'):
        common_section['jira'] = {}
        common_section['jira']['project_key'] = parser.get('common', 'jira.project_key')
        if parser.has_option('common', 'jira.version_project'):
            version_project = parser.get('common', 'jira.version_project')
            common_section['jira']['version_project'] = version_project
            common_section['jira']['version_label'] = "%s-%s" % (
               version_project.lower(), parser.get(version_project, 'version'))
            #TODO: make jira.rapid_view required when IPINF-192 is done
            if parser.has_option('common', 'jira.rapid_view'):
                common_section['jira']['rapid_view'] = parser.get('common', 'jira.rapid_view')
        common_section['jira']['projects'] = parser.sections()
    shared_config = InterpolationConfigParser()
    dataset = shared_config.read(shared_cfg_path)
    if shared_cfg_path not in dataset:
        raise IOError("Config file %s not found." % shared_cfg_path)
    if 'jira' in common_section:
        common_section['jira'].update(shared_config.items('jira'))
    for sec in shared_config.sections():
        if sec == 'jira':
            continue
        if sec in common_section:
            raise ValueError("Section %s is both in product-specific config"
                             "and shared config. " % sec)
        common_section[sec] = dict(shared_config.items(sec))


""" Dictionary with following structure: config file name => ConfigParser. """
config_parser_cache = {}

def _get_parser(configfile):
    global config_parser_cache

    if configfile in config_parser_cache.keys():
        parser = config_parser_cache[configfile]
    else:
        parser = InterpolationConfigParser()
        parser.read(configfile)
        config_parser_cache[configfile] = parser

    return parser


def read_value(configfile, section, option):
    parser = _get_parser(configfile)

    return _read_value(parser, section, option)


def _read_value(parser, section, option):
    if not parser.has_section(section):
        raise NoSectionError("%s (available sections: %s)"
            % (section, sorted(parser.sections())))
    if not parser.has_option(section, option):
        raise NoOptionError("%s (available options: %s)" % (option, sorted(parser.options(section))), section)
    else:
        return parser.get(section, option)


def has_option(configfile, section, option):
    parser = _get_parser(configfile)

    return parser.has_option(section, option)


def sections(configfile):
    parser = _get_parser(configfile)

    return parser.sections()


class ArtifactConfig:

    def __init__(self, configfile, section):
        self.artifact = section
        if has_option(configfile, section, "package"):
            self.package = read_value(configfile, section, "package")
        else:
            self.package = None
        self.version = read_value(configfile, section, "version")
        if has_option(configfile, section, "scmUrl"):
            self.src_scm = ScmInfo(read_value(configfile, section, "scmUrl"))
        else:
            self.src_scm = None
        if has_option(configfile, section, "patches"):
            self.patches_scm = ScmInfo(read_value(configfile, section, "patches"))
        else:
            self.patches_scm = None
        if has_option(configfile, section, "profiles"):
            self.profiles = read_value(configfile, section, "profiles")
        else:
            self.profiles = None


class ConfigException(BaseException):

    def __init__(self, message):
        super(ConfigException, self).__init__(message)


from ConfigParser import InterpolationMissingOptionError
from ConfigParser import InterpolationSyntaxError, InterpolationDepthError
from ConfigParser import MAX_INTERPOLATION_DEPTH
from ConfigParser import DEFAULTSECT
_UNSET = object()

class InterpolationConfigParser(ConfigParser):

    """Adds 3.x-style variable interpolation to the 2.x ConfigParser.

    This allows values to contain ${section:key} notation to refer to values
    defined in specified sections. The 'section:' part may be omitted to
    reference values from the same section.

    See: https://docs.python.org/3/library/configparser.html#interpolation-of-values
    """

    _KEYCRE = re.compile(r"\$\{([^}]+)\}")

    def get(self, section, option, raw=False, vars=None, fallback=_UNSET):

        d = self._defaults.copy()
        try:
            d.update(self._sections[section])
        except KeyError:
            if section != DEFAULTSECT:
                raise NoSectionError(section)

        # Update the entry specific variables
        if vars:
            for key, value in vars.items():
                d[self.optionxform(key)] = value
        option = self.optionxform(option)
        try:
            value = d[option]
        except KeyError:
            if fallback is _UNSET:
                raise NoOptionError(option, section)
            else:
                return fallback

        if raw or value is None:
            return value
        else:
            return self._interpolate(section, option, value, d)

    def items(self, section, raw=False, vars=None):
        d = self._defaults.copy()
        try:
            d.update(self._sections[section])
        except KeyError:
            if section != DEFAULTSECT:
                raise NoSectionError(section)
        # Update with the entry specific variables
        if vars:
            for key, value in vars.items():
                d[self.optionxform[key]] = value;
        options = d.keys()
        if "__name__" in options:
            options.remove("__name__")

        if raw:
            return [(option, d[option])
                    for option in options]
        else:
            return [(option, self._interpolate(section, option, d[option], d))
                    for option in options]


    def set(self, section, option, value=None):
        """Set an option, checking the validity of interpolated values."""

        if value:
            value = self._before_set(section, option, value)

        if not section or section == DEFAULTSECT:
            sectdict = self._defaults
        else:
            try:
                sectdict=self._sections[section]
            except KeyError:
                raise NoSectionError(section)
        sectdict[self.optionxform(option)] = value

    def _before_set(self, section, option, value):
        tmp_value = value.replace('$$', '') # escaped dollar signs
        tmp_value = self._KEYCRE.sub('', tmp_value) # valid syntax
        if '$' in tmp_value:
            raise ValueError("invalid interpolation syntax in %r at "
                             "position %d" % (value, tmp_value.find('$')))
        return value

    def _interpolate(self, section, option, value, defaults):
        L = []
        self._interpolate_some(option, L, value, section, defaults, 1)
        return ''.join(L)

    def _interpolate_some(self, option, accum, rest, section, map, depth):
        rawval = self.get(section, option, raw=True, fallback=rest)
        if depth > MAX_INTERPOLATION_DEPTH:
            raise InterpolationDepthError(option, section, rawval)
        while rest:
            p = rest.find("$")
            if p < 0:
                accum.append(rest)
                return
            if p > 0:
                accum.append(rest[:p])
                rest = rest[p:]
            # p is no longer used
            c = rest[1:2]
            if c == "$":
                accum.append("$")
                rest = rest[2:]
            elif c == "{":
                m = self._KEYCRE.match(rest)
                if m is None:
                    raise InterpolationSyntaxError(option, section,
                        "bad interpolation variable reference %r" % rest)
                path = m.group(1).split(':')
                rest = rest[m.end():]
                sect = section
                opt = option
                try:
                    if len(path) == 1:
                        opt = self.optionxform(path[0])
                        v = map[opt]
                    elif len(path) == 2:
                        sect = path[0]
                        opt = self.optionxform(path[1])
                        v = self.get(sect, opt, raw=True)
                    else:
                        raise InterpolationSyntaxError(
                            option, section,
                            "More that one ':' found: %r" % (rest,))
                except (KeyError, NoSectionError, NoOptionError):
                    raise InterpolationMissingOptionError(
                        option, section, rawval, ":".join(path))
                if "$" in v:
                    self._interpolate_some(opt, accum, v, sect,
                                           dict(self.items(sect, raw=True)),
                                           depth + 1)
                else:
                    accum.append(v)
            else:
                raise InterpolationSyntaxError(
                    option, section,
                    "'$' must be followed by '$' or '{', "
                    "found: %r" % (rest,))
