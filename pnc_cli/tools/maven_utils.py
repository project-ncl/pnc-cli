# -*- coding: utf-8 -*-

import logging
import os
import shutil
import string
import urllib2
import urlparse
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
from xml.dom import minidom


""" Dictionary with following structure: repo url => GAV (string) => effective pom (string). """
effective_pom_cache = {}
""" Dictionary with following structure: repo url => GAV (string) => management type => MavenArtifact[]. """
managed_gavs_cache = {}


class MGMT_TYPE:
    PLUGINS = "plugins"
    DEPENDENCIES = "dependencies"
    BOTH = "both"


def read_managed_gavs(artifact, repo_url=None, mgmt_type=MGMT_TYPE.DEPENDENCIES, mvn_repo_local=None):
    global managed_gavs_cache

    gav = artifact.get_gav()
    result = None
    if repo_url in managed_gavs_cache.keys():
        if gav in managed_gavs_cache[repo_url].keys():
            if mgmt_type in managed_gavs_cache[repo_url][gav]:
                result = managed_gavs_cache[repo_url][gav][mgmt_type]
    if not result:
        result = _read_managed_gavs(artifact, repo_url, mgmt_type, mvn_repo_local)
        if result:
            cache = managed_gavs_cache.setdefault(repo_url, {}).setdefault(gav, {})
            if mgmt_type in [MGMT_TYPE.BOTH, MGMT_TYPE.DEPENDENCIES]:
                cache[MGMT_TYPE.DEPENDENCIES] = result[MGMT_TYPE.DEPENDENCIES]
            if mgmt_type in [MGMT_TYPE.BOTH, MGMT_TYPE.PLUGINS]:
                result[MGMT_TYPE.PLUGINS] = result[MGMT_TYPE.PLUGINS]
    return result


def _read_managed_gavs(artifact, repo_url=None, mgmt_type=MGMT_TYPE.DEPENDENCIES, mvn_repo_local=None):
    """
    Reads all artifacts managed in dependencyManagement section of effective pom of the given artifact. It places the
    repo_url in settings.xml and then runs help:effective-pom with these settings. There should be the POM with its
    parent and dependencies available in the repository and there should also be all plugins available needed to execute
    help:effective-pom goal.

    :param artifact: MavenArtifact instance representing the POM
    :param repo_url: repository URL to use
    :param mgmt_type: type of management to read, values available are defined in MGMT_TYPE class
    :param mvn_repo_local: path to local Maven repository to be used when getting effective POM
    :returns: dictionary, where key is the management type and value is the list of artifacts managed by
              dependencyManagement/pluginManagement or None, if a problem occurs
    """

    # download the pom
    pom_path = download_pom(repo_url, artifact)
    if pom_path:
        pom_dir = os.path.split(pom_path)[0]

        # get effective pom
        eff_pom = get_effective_pom(pom_dir, repo_url, mvn_repo_local)
        shutil.rmtree(pom_dir, True)
        if not eff_pom:
            return None

        # read dependencyManagement/pluginManagement section
        managed_arts = read_management(eff_pom, mgmt_type)
    else:
        managed_arts = None

    return managed_arts


def get_effective_pom(pom_dir, repo_url, mvn_repo_local, profiles=None, additional_params=None):
    """
    Gets the effective pom from the downloaded pom. There has to be complete source tree (at least the pom tree) in case
    that the root pom contains some modules.

    :param pom_dir: directory where the pom is prepared (including potential patches)
    :param repo_url: repository URL, where all dependencies needed to resolve the effective POM are available
    :param mvn_repo_local: path to local repository to use if a non-default location is required
    :returns: the effective pom as a string or None if a problem occurs
    """
    global effective_pom_cache

    pom_file = None
    try:
        pom_file = open(os.path.join(pom_dir, "pom.xml"))
        pom = pom_file.read()
    finally:
        if pom_file:
            pom_file.close()
    artifact = MavenArtifact(pom=pom)
    gav = artifact.get_gav()

    eff_pom = None
    if repo_url in effective_pom_cache.keys():
        if gav in effective_pom_cache[repo_url].keys():
            if profiles in effective_pom_cache[repo_url][gav].keys():
                if additional_params in effective_pom_cache[repo_url][gav][profiles].keys():
                    eff_pom = effective_pom_cache[repo_url][gav][profiles][additional_params]

    if not eff_pom:
        try:
            eff_pom = _read_effective_pom(pom_dir, repo_url, mvn_repo_local, profiles, additional_params)
        finally:
            if eff_pom:
                effective_pom_cache.setdefault(repo_url, {}).setdefault(gav, {}).setdefault(profiles, {})[additional_params] = eff_pom

    return eff_pom


def _read_effective_pom(pom_dir, repo_url, mvn_repo_local, profiles, additional_params):
    work_dir = os.getcwd()
    os.chdir(pom_dir)

    try:
        settings_filename = create_mirror_settings(repo_url)

        eff_pom_filename = "effective-pom.xml"
        args = ["mvn", "org.apache.maven.plugins:maven-help-plugin:2.2:effective-pom", "-Doutput=%s" % eff_pom_filename,
                "-s", settings_filename]
        if mvn_repo_local:
            args.append("-Dmaven.repo.local=%s" % mvn_repo_local)
        if profiles:
            args.append("-P%s" % profiles)
        if additional_params:
            param_list = additional_params.split(" ")
            args.extend(param_list)

        logging.debug("Running command: %s", " ".join(args))
        command = Popen(args, stdout=PIPE, stderr=STDOUT)
        stdout = command.communicate()[0]
        if command.returncode:
            logging.error("Getting effective POM failed. Output:\n%s" % stdout)
            eff_pom = None
        else:
            logging.debug("Getting effective POM succeeded. Output:\n%s" % stdout)
            eff_pom_file = None
            try:
                eff_pom_file = open(eff_pom_filename)
                eff_pom = eff_pom_file.read()
            finally:
                if eff_pom_file:
                    eff_pom_file.close()
    finally:
        os.chdir(work_dir)

    return eff_pom


def alter_poms(pom_dir, additional_params, repo_url=None, mvn_repo_local=None):
    """
    Runs mvn clean command with provided additional parameters to perform pom updates by pom-manipulation-ext.
    """
    work_dir = os.getcwd()
    os.chdir(pom_dir)

    try:
        if repo_url:
            settings_filename = create_mirror_settings(repo_url)
        else:
            settings_filename = None

        args = ["mvn", "clean"]
        if mvn_repo_local:
            args.extend(["-s", settings_filename])
        if mvn_repo_local:
            args.append("-Dmaven.repo.local=%s" % mvn_repo_local)
        param_list = additional_params.split(" ")
        args.extend(param_list)

        logging.debug("Running command: %s", " ".join(args))
        command = Popen(args, stdout=PIPE, stderr=STDOUT)
        stdout = command.communicate()[0]
        if command.returncode:
            logging.error("POM manipulation failed. Output:\n%s" % stdout)
        else:
            logging.debug("POM manipulation succeeded. Output:\n%s" % stdout)
    finally:
        os.chdir(work_dir)

def pom_contains_modules():
    """
    Reads pom.xml in current working directory and checks, if there is non-empty modules tag.
    """
    pom_file = None
    try:
        pom_file = open("pom.xml")
        pom = pom_file.read()
    finally:
        if pom_file:
            pom_file.close()

    artifact = MavenArtifact(pom=pom)
    if artifact.modules:
        return True
    else:
        return False


def get_repo_url(mead_tag, nexus_base_url, prefix="hudson-", suffix=""):
    """
    Creates repository Nexus group URL composed of:
        <nexus_base_url>/content/groups/<prefix><mead_tag><suffix>

    :param mead_tag: name of the MEAD tag used to create the proxy URL in settings.xml
    :param nexus_base_url: the base URL of a Nexus instance
    :param prefix: Nexus group name prefix, default is "hudson-"
    :param suffix: Nexus group name suffix, e.g. "-jboss-central" or "-reverse"
    :returns:
    """
    result = urlparse.urljoin(nexus_base_url, "content/groups/")
    result = urlparse.urljoin(result, "%s%s%s/" % (prefix, mead_tag, suffix))
    return result


def download_pom(repo_url=None, artifact=None, pom_url=None, target_dir=None):
    """
    Downloads a pom file with give GAV (as array) or from given pom_url and saves it as pom.xml into target_dir.

    :param repo_url: repository URL from which the pom should be downloaded, mandatory only if no pom_url provided
    :param artifact: MavenArtifact instance, mandatory only if no pom_url provided
    :param pom_url: URL of the pom to download, not mandatory
    :target_dir: target directory path, where the pom should be saved, not mandatory
    :returns: path to the saved pom, useful if no target_dir provided
    """
    if not pom_url:
        pom_url = urlparse.urljoin(repo_url, "%s/" % string.replace(artifact.groupId, ".", "/"))
        pom_url = urlparse.urljoin(pom_url, "%s/" % artifact.artifactId)
        pom_url = urlparse.urljoin(pom_url, "%s/" % artifact.version)
        pom_url = urlparse.urljoin(pom_url, "%s-%s.pom" % (artifact.artifactId, artifact.version))

    handler = None
    try:
        handler = urllib2.urlopen(pom_url)
    except urllib2.HTTPError, err:
        logging.error("Failed to download POM %s. %s", pom_url, err)
        return None

    if not target_dir:
        num = 1
        while not target_dir or os.path.exists(target_dir):
            target_dir = "/tmp/maven-temp-path-%s" % num
            num += 1

    pom_path = os.path.join(target_dir, "pom.xml")

    if handler.getcode() == 200:
        pom = handler.read()
        handler.close()
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        pom_file = None
        try:
            pom_file = open(pom_path, "w")
            pom_file.write(pom)
        finally:
            if pom_file:
                pom_file.close()

    return pom_path


def read_management(pom, mgmt_type):
    xmldoc = minidom.parseString(pom)

    result = {}
    if mgmt_type in [MGMT_TYPE.BOTH, MGMT_TYPE.DEPENDENCIES]:
        result[MGMT_TYPE.DEPENDENCIES] = _read_management(xmldoc, "dependencyManagement", "dependency")
    if mgmt_type in [MGMT_TYPE.BOTH, MGMT_TYPE.PLUGINS]:
        result[MGMT_TYPE.PLUGINS] = _read_management(xmldoc, "pluginManagement", "plugin")

    return result


def _read_management(xmldoc, management_tag, artifact_tag):
    mgmts = xmldoc.getElementsByTagName(management_tag)
    result = []
    if len(mgmts):
        mgmt = mgmts[0]
        art_elem_list = mgmt.getElementsByTagName(artifact_tag)

        for art_elem in art_elem_list:
            groupid = None
            artifactid = None
            version = None

            g_elem_list = art_elem.getElementsByTagName('groupId')
            for groupid_elem in g_elem_list:
                if groupid_elem.parentNode.localName == artifact_tag:
                    groupid = groupid_elem.childNodes[0].data
                    break
            a_elem_list = art_elem.getElementsByTagName('artifactId')
            for artifactid_elem in a_elem_list:
                if artifactid_elem.parentNode.localName == artifact_tag:
                    artifactid = artifactid_elem.childNodes[0].data
                    break
            v_elem_list = art_elem.getElementsByTagName('version')
            for version_elem in v_elem_list:
                if version_elem.parentNode.localName == artifact_tag:
                    version = version_elem.childNodes[0].data
                    break

            if not groupid or not artifactid or not version:
                logging.warning("Incomplete GAV information in %s: %s:%s:%s", management_tag, groupid, artifactid,
                                version)
            else:
                artifact = MavenArtifact(groupId=groupid, artifactId=artifactid, version=version)
                result.append(artifact)

    return result


def get_properties(gav, repo_url, mvn_repo_local):
    artifact = MavenArtifact(gav=gav)
    pom_path = download_pom(repo_url, artifact)
    if pom_path:
        pom_dir = os.path.split(pom_path)[0]

        eff_pom = get_effective_pom(pom_dir, repo_url, mvn_repo_local)
        shutil.rmtree(pom_dir, True)
        if not eff_pom:
            return None

        return read_properties(eff_pom)
    else:
        return None


def read_properties(pom):
    xmldoc = minidom.parseString(pom)
    propertiesElemList = xmldoc.getElementsByTagName("properties")

    result = {}
    for propertiesElem in propertiesElemList:
        for propertyElem in propertiesElem.childNodes:
            if propertyElem.nodeType == propertyElem.ELEMENT_NODE:
                name = propertyElem.localName
                value_list = []
                for childnode in propertyElem.childNodes:
                    if childnode.nodeType == childnode.TEXT_NODE:
                        value_list.append(childnode.data)
                value = ''.join(value_list)
                result[name] = value

    return result


def create_mirror_settings(repo_url):
    """
    Creates settings.xml in current working directory, which when used makes Maven use given repo URL as a mirror of all
    repositories to look at.

    :param repo_url: the repository URL to use
    :returns: filepath to the created file
    """
    cwd = os.getcwd()
    settings_path = os.path.join(cwd, "settings.xml")

    settings_file = None
    try:
        settings_file = open(settings_path, "w")
        settings_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        settings_file.write('<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"\n')
        settings_file.write('          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n')
        settings_file.write('          xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 http://maven.apache.org/xsd/settings-1.0.0.xsd">\n')
        settings_file.write('<mirrors>\n')
        settings_file.write('    <mirror>\n')
        settings_file.write('      <id>repo-mirror</id>\n')
        settings_file.write('        <url>%s</url>\n' % repo_url)
        settings_file.write('      <mirrorOf>*</mirrorOf>\n')
        settings_file.write('    </mirror>\n')
        settings_file.write('  </mirrors>\n')
        settings_file.write('</settings>\n')
    finally:
        if settings_file:
            settings_file.close()

    return settings_path


class MavenArtifact:

    def __init__(self, pom=None, profiles=[], gav=None, groupId=None, artifactId=None, version=None, parentGav=None):
        self.parentGav = parentGav
        self.modules = None
        if pom:
            xmldoc = minidom.parseString(pom)
            project = xmldoc.getElementsByTagName('project')[0]

            groupIdElemList = project.getElementsByTagName('groupId')
            groupId = None
            for groupIdElem in groupIdElemList:
                if groupIdElem.parentNode.localName == "parent":
                    groupId = groupIdElem.childNodes[0].data
                elif groupIdElem.parentNode.localName == "project":
                    groupId = groupIdElem.childNodes[0].data
                    break
            self.groupId = groupId

            artifactIdElemList = project.getElementsByTagName('artifactId')
            for artifactIdElem in artifactIdElemList:
                if artifactIdElem.parentNode.localName == "project":
                    self.artifactId = artifactIdElem.childNodes[0].data
                    break

            version = None
            versionElemList = project.getElementsByTagName('version')
            for versionElem in versionElemList:
                if versionElem.parentNode.localName == "parent":
                    version = versionElem.childNodes[0].data
                elif versionElem.parentNode.localName == "project":
                    version = versionElem.childNodes[0].data
                    break
            self.version = version

            parentElemList = project.getElementsByTagName('parent')
            if len(parentElemList):
                groupIdElemList = parentElemList[0].getElementsByTagName('groupId')
                groupId = groupIdElemList[0].childNodes[0].data
                artifactIdElemList = parentElemList[0].getElementsByTagName('artifactId')
                artifactId = artifactIdElemList[0].childNodes[0].data
                versionElemList = parentElemList[0].getElementsByTagName('version')
                version = versionElemList[0].childNodes[0].data
                self.parentGav = "%s:%s:%s" % (groupId, artifactId, version)
            else:
                self.parentGav = None

            modulesElemList = project.getElementsByTagName('modules')
            if len(modulesElemList):
                for modulesElem in modulesElemList:
                    modulesActive = False
                    if modulesElem.parentNode.localName == "project":
                        modulesActive = True
                    elif modulesElem.parentNode.localName == "profile":
                        profileElem = modulesElem.parentNode
                        profileIdElems = profileElem.getElementsByTagName('id')
                        if len(profileIdElems):
                            profileIdElem = profileElem.getElementsByTagName('id')[0]
                            profileId = profileIdElem.childNodes[0].data
                        else:
                            profileId = "<no profile id specified>"
                        if profileId in profiles:
                            modulesActive = True
                        else:
                            abdElemList = profileElem.getElementsByTagName('activeByDefault')
                            if len(abdElemList):
                                abdElem = abdElemList[0]
                                abd = abdElem.childNodes[0].data
                                if abd == "true" and ("!%s" % profileId) not in profiles:
                                    modulesActive = True

                    if modulesActive:
                        moduleElemList = modulesElem.getElementsByTagName('module')
                        for moduleElem in moduleElemList:
                            if not self.modules:
                                self.modules = {}
                            module_name = moduleElem.childNodes[0].data
                            if not self.modules.__contains__(module_name):
                                self.modules[module_name] = None

        elif gav:
            parts = string.split(gav, ":")
            if len(parts) != 3:
                raise ValueError("%s is not a GAV." % gav)
            else:
                self.groupId = parts[0]
                self.artifactId = parts[1]
                self.version = parts[2]
        else:
            self.groupId = groupId
            self.artifactId = artifactId
            self.version = version

    def get_ga(self):
        return "%s:%s" % (self.groupId, self.artifactId)

    def get_gav(self):
        return "%s:%s:%s" % (self.groupId, self.artifactId, self.version)
