# -*- coding: utf-8 -*-

import copy
import logging
import os
import re
import shutil
from subprocess import PIPE
from subprocess import Popen
from subprocess import STDOUT

import maven_utils
import web_utils
from maven_utils import MavenArtifact

git_version = None

scm_status_cache = {}

scm_info_path_cache = {}


def get_scm_status(config, read_modules=False, repo_url=None, mvn_repo_local=None, additional_params=None):
    """
    Gets the artifact status (MavenArtifact instance) from SCM defined by config. Only the top-level artifact is read by
    default, although it can be requested to read the whole available module structure.

    :param config: artifact config (ArtifactConfig instance)
    :param read_modules: if True all modules are read, otherwise only top-level artifact
    :param repo_url: the URL of the repository to use
    :param mvn_repo_local: local repository path
    :param additional_params: additional params to add on command-line when running maven
    """
    global scm_status_cache
    if config.artifact in scm_status_cache.keys():
        result = scm_status_cache[config.artifact]
    elif not read_modules and (("%s|False" % config.artifact) in scm_status_cache.keys()):
        result = scm_status_cache["%s|False" % config.artifact]
    else:
        result = _get_scm_status(config, read_modules, repo_url, mvn_repo_local, additional_params)
        if read_modules:
            scm_status_cache[config.artifact] = result
            if ("%s|False" % config.artifact) in scm_status_cache.keys():
                del(scm_status_cache["%s|False" % config.artifact])
        else:
            scm_status_cache["%s|False" % config.artifact] = result
    return result


def _get_scm_status(config, read_modules, repo_url, mvn_repo_local, additional_params):
    scm = config.src_scm
    if not scm:
        return None
    work_dir = os.getcwd()
    src_dir = os.path.join(work_dir, "src_git_temp")
    patches_dir = os.path.join(work_dir, "patches_git_temp")

    if os.path.exists(src_dir):
        shutil.rmtree(src_dir, True)
    if os.path.exists(patches_dir):
        shutil.rmtree(patches_dir, True)

    pom_path = os.path.join(src_dir, "pom.xml")
    if scm.scheme == "git" or scm.scheme == "git+https":
        if read_modules or additional_params or scm.host_and_port != "git.app.eng.bos.redhat.com":
            git_clone(scm, src_dir, "sources")
        else:
            if not scm.path.endswith(".git"):
                scm.path = "%s.git" % scm.path
            if scm.repo_root:
                repo_path = "/%s" % scm.repo_root
            else:
                repo_path = ""
            if scm.commit_id:
                pom_url = "http://%s%s/plain%s/pom.xml?id=%s" % (scm.host_and_port, scm.path, repo_path, scm.commit_id)
            else:
                pom_url = "http://%s%s/plain%s/pom.xml" % (scm.host_and_port, scm.path, repo_path)
            download_result = web_utils.download_file(pom_url, pom_path, config.artifact)
            if not download_result:
                return None
    elif scm.scheme == "svn+http":
        if read_modules or additional_params or scm.host_and_port != "svn.devel.redhat.com":
            svn_checkout(scm, src_dir, "sources")
        else:
            if scm.repo_root:
                scm_path = "%s/%s" % (scm.path.replace('?', '/'), scm.repo_root)
            else:
                scm_path = scm.path.replace('?', '/')
            if scm.commit_id:
                pom_url = "http://%s%s/pom.xml?p=%s" % (scm.host_and_port, scm_path, scm.commit_id)
            else:
                pom_url = "http://%s%s/pom.xml" % (scm.host_and_port, scm_path)
            download_result = web_utils.download_file(pom_url, pom_path, config.artifact)
            if not download_result:
                return None
    elif scm.scheme == "file":
        shutil.copytree(scm.path, src_dir)
    else:
        logging.error("[%s] %s scheme is not supported ATM (%s).", config.artifact, scm.scheme, scm.host_and_port)
        return None

    if config.patches_scm:
        if config.patches_scm.scheme == "git":
            git_clone(config.patches_scm, patches_dir, "patches")
        elif config.patches_scm.scheme == "svn+http":
            svn_checkout(config.patches_scm, patches_dir, "patches")
        elif config.patches_scm.scheme == "file":
            shutil.copytree(config.patches_scm.path, patches_dir)
        else:
            logging.error("[%s] %s scheme is not supported ATM (%s).", config.artifact, config.patches_scm.scheme,
                          config.patches_scm.host_and_port)
            return None
        apply_patches(src_dir, patches_dir, not read_modules)
        #shutil.rmtree(patches_dir, True)

    todo_modules = ['']
    result = None

    if additional_params:
        maven_utils.alter_poms(src_dir, additional_params, repo_url, mvn_repo_local)

    while len(todo_modules):
        act_module = todo_modules.pop(0)
        act_module_path = os.path.join(src_dir, act_module)
        pom_path = os.path.join(act_module_path, "pom.xml")
        pom_file = None
        try:
            pom_file = open(pom_path)
            pom = pom_file.read()
        finally:
            if pom_file:
                pom_file.close()
        if config.profiles:
            artifact = MavenArtifact(pom, re.split("[, ]+", config.profiles))
        else:
            artifact = MavenArtifact(pom)
        if act_module == '':
            result = artifact
        else:
            (act_module_parent, act_module_name) = os.path.split(act_module)
            module_parent_path = act_module_parent.split(os.sep)
            parent_module = result
            rest = ""
            for path_element in module_parent_path:
                if rest:
                    module_name = "%s/%s" % (rest, path_element)
                else:
                    module_name = path_element
                if module_name:
                    if module_name in parent_module.modules.keys() and parent_module.modules[module_name].modules:
                        parent_module = parent_module.modules[module_name]
                        rest = ""
                    else:
                        rest = module_name
            if rest:
                act_module_name = "%s/%s" % (rest, act_module_name)
            parent_module.modules[act_module_name] = artifact

        if read_modules and artifact.modules:
            for module in artifact.modules:
                todo_modules.append(os.path.join(act_module, module))
            todo_modules.sort()

    #shutil.rmtree(src_dir, True)

    return result


def git_clone(scm_info, target_dir, desc, ssl_no_verify=False):
    logging.debug("Cloning from %s to '%s'", str(scm_info), target_dir)
    args_array = []
    if scm_info.commit_id:
        git_version = get_git_version()
        # if git version >= 1.9.x
        if git_version[0:2] != "1." or git_version[2] >= '9':
            args_array.append(["git", "clone", "--depth", "1", "--branch", scm_info.commit_id, scm_info.get_scm_url(), target_dir])
        args_array.append(["git", "clone", scm_info.get_scm_url(), target_dir])
    else:
        args_array.append(["git", "clone", "--depth", "1", scm_info.get_scm_url(), target_dir])
    cloned = False
    while not cloned and len(args_array):
        args = args_array.pop(0)
        logging.debug("Running %s", " ".join(args))
        if ssl_no_verify:
            # Copy existing enivronment vars
            env_vars = dict(os.environ)
            env_vars['GIT_SSL_NO_VERIFY'] = 'true'
            command = Popen(args, stdout=PIPE, stderr=STDOUT, env=env_vars)
        else:
            command = Popen(args, stdout=PIPE, stderr=STDOUT)
        stdout = command.communicate()[0]
        if command.returncode:
            if len(args_array) and ("fatal: Remote branch %s not found in upstream origin" % scm_info.commit_id) in stdout:
                logging.info("Git clone of %s ended up with an error. Output: %s\nTrying a full clone and then checkout." % (desc, stdout))
            else:
                raise ScmException("Git clone of %s ended up with an error. Output: %s" % (desc, stdout))
        else:
            cloned = True
            if len(args) == 4 and scm_info.commit_id:
                args = ["git", "checkout", scm_info.commit_id]

                work_dir = os.getcwd()
                _chdir(target_dir)
                logging.debug("Running %s", " ".join(args))
                command = Popen(args, stdout=PIPE, stderr=STDOUT)
                stdout = command.communicate()[0]
                _chdir(work_dir)

                if command.returncode:
                    raise ScmException("Git checkout in dir %s ended up with an error. Output: %s" % (target_dir, stdout))

    if scm_info.repo_root:
        intended_root = os.path.join(target_dir, scm_info.repo_root)
        temp_root = "%s-temp" % target_dir
        shutil.move(intended_root, temp_root)
        shutil.rmtree(target_dir)
        shutil.move(temp_root, target_dir)


def svn_checkout(scm_info, target_dir, desc=""):
    logging.debug("Checking out from %s to '%s'", str(scm_info), target_dir)

    args = ["svn", "co", scm_info.get_scm_url().replace('?', '/'), '-r', scm_info.commit_id, target_dir]
    command = Popen(args, stdout=PIPE, stderr=STDOUT)
    stdout = command.communicate()[0]
    if command.returncode:
        raise ScmException("SVN checkout of %s ended up with an error. Output: %s" % (desc, stdout))

    if scm_info.repo_root:
        intended_root = os.path.join(target_dir, scm_info.repo_root)
        temp_root = "%s-temp" % target_dir
        shutil.move(intended_root, temp_root)
        shutil.rmtree(target_dir)
        shutil.move(temp_root, target_dir)


def apply_patches(src_dir, patches_dir, shrink=True):
    patch_count = 0
    for root, dirs, files in os.walk(patches_dir):
        if root == patches_dir:
            for patch_file in sorted(files):
                if patch_file.endswith(".patch"):
                    patch_count += 1
                    patch_path = os.path.join(root, patch_file)
                    if shrink:
                        pom_path = os.path.join(src_dir, "pom.xml")
                        if shrink_patch(patch_path, "pom.xml"):
                            args = ["patch", pom_path, patch_path]
                            logging.debug("Running command: %s", " ".join(args))
                            command = Popen(args, stdout=PIPE, stderr=STDOUT)
                            stdout = command.communicate()[0]
                            if command.returncode:
                                logging.warning("Patching of pom.xml failed. Output:\n%s" % stdout)
                            else:
                                logging.debug("Patches applied OK")
                        else:
                            logging.debug("Skipping %s because it does not contain any changes for pom.xml.", patch_file)
                    else:
                        work_dir = os.getcwd()
                        _chdir(src_dir)
                        args = "patch -p1 <%s" % patch_path
                        logging.debug("Running command: %s", args)
                        command = Popen(args, stdout=PIPE, stderr=STDOUT, shell=True)
                        stdout = command.communicate()[0]
                        if command.returncode:
                            logging.warning("Patching of sources failed. Output:\n%s" % stdout)
                        else:
                            logging.debug("Patches applied OK")
                        _chdir(work_dir)
    if not patch_count:
        logging.debug("No patches found in patches repository.")


def shrink_patch(patch_path, target_file):
    """
    Shrinks a patch on patch_path to contain only changes for target_file.

    :param patch_path: path to the shrinked patch file
    :param target_file: filename of a file of which changes should be kept
    :return: True if the is a section containing changes for target_file, Flase otherwise
    """
    logging.debug("Shrinking patch file %s to keep only %s changes.", patch_path, target_file)
    shrinked_lines = []
    patch_file = None
    try:
        patch_file = open(patch_path)
        adding = False
        search_line = "diff --git a/%s b/%s" % (target_file, target_file)
        for line in patch_file.read().split("\n"):
            if adding and line.startswith("diff --git a/") and line != search_line:
                adding = False
            elif line == search_line:
                adding = True
            if adding:
                shrinked_lines.append(line)
    finally:
        if patch_file:
            patch_file.close()

    if len(shrinked_lines):
        patch_file = None
        try:
            patch_file = open(patch_path, "w")
            content = "\n".join(shrinked_lines)
            if not content.endswith("\n"):
                content = content + "\n"
            patch_file.write(content)
        finally:
            if patch_file:
                patch_file.close()
        return True
    else:
        return False


def _chdir(path):
    os.chdir(path)
    logging.debug("CWD changed to '%s'", os.getcwd())


def get_scm_info(directory, branch_id=False, read_only=False, filePath=None):
    """
    Reads SCM info from the given directory. It can fill real commit ID into commit_id field or branch name.

    @param directory: directory name
    @param branch_id: reads commit ID if False (default) or branch name if True
    @param read_only: if True it replaces the actual scheme to the read-only for known hosts, e.g. git+ssh to git for
                      git.app.eng.bos.redhat.com, otherwise it just reads it (default)
    @return: an ScmInfo instance
    """
    #TODO use a commit id instead of branch if in detached state

    if (directory, branch_id, read_only, filePath) in scm_info_path_cache:
        return copy.copy(scm_info_path_cache[(directory, branch_id, read_only, filePath)])

    if os.path.exists(os.path.join(directory, ".git")):
        logging.debug("Getting git info for %s", directory)
        if filePath != None:
            args = ["git", "--git-dir", directory + "/.git", "log", "-z", "-n", "2", "--pretty=format:* dummy-branch  %H  %s%n", "--", filePath]
        else:
            args = ["git", "--git-dir", directory + "/.git", "branch", "-v", "--no-abbrev"]

        command = Popen(args, stdout=PIPE, stderr=STDOUT)
        stdout = command.communicate()[0]
        if command.returncode:
            raise ScmException("Reading Git branch name and commit ID from %s failed. Output: %s" % (directory, stdout))

        branch_name = None
        commit_id = None

        for line in stdout.split("\n"):
            if line.startswith("* "):
                pattern = "\* +(.*) +([a-f0-9]{40}) .*"
                m = re.match(pattern, line)
                if m:
                    branch_name = m.group(1).strip()
                    commit_id = m.group(2).strip()
                    break
                else:
                    raise ScmException("Cannot parse commit ID and branch name from result line:\n%s" % line)

        logging.info ("Retrieved branch_name %s and commit_id %s", branch_name, commit_id)

        args = ["git", "--git-dir", directory + "/.git", "remote", "-v"]
        command = Popen(args, stdout=PIPE, stderr=STDOUT)
        stdout = command.communicate()[0]
        if command.returncode:
            raise ScmException("Reading Git remote from %s failed. Output: %s" % (directory, stdout))

        origin_url = None
        for line in stdout.split("\n"):
            if line.startswith("origin" + chr(9)) and line.endswith(" (fetch)"):
                parts = re.split("[\s]+", line, 3)
                origin_url = parts[1]
                break

        if branch_id:
            scminfo = ScmInfo("%s#%s" % (origin_url, branch_name))
        else:
            scminfo = ScmInfo("%s#%s" % (origin_url, commit_id))

        if read_only:
            if scminfo.get_scm_url().startswith("git+ssh://git.app.eng.bos.redhat.com/srv/git/"):
                scminfo.scheme = "git"
                scminfo.path = scminfo.path.replace("/srv/git/", "/")
            elif scminfo.get_scm_url().startswith("git+ssh://code.engineering.redhat.com/"):
                scminfo.scheme = "git+https"
                scminfo.path = ("%s%s" % ("/gerrit/", scminfo.path)).replace("gerrit//", "gerrit/")

        scm_info_path_cache[(directory, branch_id, read_only, filePath)] = scminfo
        return scminfo
    elif os.path.exists(directory):
        #Special case for the integration-platform-tests which test tooling
        #inplace and use the file:// in the test.cfg
        scminfo = ScmInfo("file://%s#%s" % (directory, "xx"))
        scm_info_path_cache[(directory, branch_id, read_only, filePath)] = scminfo
        return scminfo
    else:
        raise ScmException("Unknown SCM type while reading SCM info from %s" % directory)


def get_git_version():
    global git_version
    if not git_version:
        args = ["git", "--version"]
        command = Popen(args, stdout=PIPE, stderr=STDOUT)
        stdout = command.communicate()[0]
        if command.returncode:
            raise ScmException("Reading Git version failed. Output: %s" % (stdout))
        git_version = stdout.strip()
        if git_version.startswith("git version "):
            git_version = git_version[12:]
    return git_version


class ScmInfo:

    def __init__(self, url):
        m = re.search("(.+)://([^/]*)(/[^?]*)(?:\?(.*)|)#(.*)", url)
        if m:
            self.scheme = m.group(1)
            self.host_and_port = re.sub(".*@", "", m.group(2))
            login_match = re.search("^(.*)@.*", m.group(2))
            if login_match:
                self.login = login_match.group(1)
            else:
                self.login = None
            self.path = m.group(3)
            self.repo_root = m.group(4)
            self.commit_id = m.group(5)
        else:
            if url.startswith("file://"):
                self.scheme = "file"
                self.path = url[7:]
            else:
                raise ScmException("Malformed SCM URL: %s" % url)

    def get_scm_url(self):
        if self.scheme.endswith("+http"):
            checkout_scheme = "http"
        elif self.scheme.endswith("+https"):
            checkout_scheme = "https"
        else:
            checkout_scheme = self.scheme
        return "%s://%s%s" % (checkout_scheme, self.host_and_port, self.path)

    def __str__(self):
        if self.repo_root:
            return "%s://%s%s?%s#%s" % (self.scheme, self.host_and_port, self.path, self.repo_root, self.commit_id)
        else:
            return "%s://%s%s#%s" % (self.scheme, self.host_and_port, self.path, self.commit_id)


class ScmException(BaseException):

    def __init__(self, message):
        super(ScmException, self).__init__(message)
