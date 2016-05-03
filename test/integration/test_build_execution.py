
import logging
import os
import re
import shutil
import tempfile
import time

import pytest

from git import Repo

from pnc_cli import buildconfigurationsets
from pnc_cli import buildconfigurations
from pnc_cli import buildrecords
from pnc_cli import projects
from pnc_cli import environments
from pnc_cli import utils
from test import testutils
from pnc_cli.swagger_client.apis.buildconfigurations_api import BuildconfigurationsApi
from pnc_cli.swagger_client.apis.runningbuildrecords_api import RunningbuildrecordsApi
from pnc_cli.swagger_client.apis.buildconfigurationsets_api import BuildconfigurationsetsApi
from pnc_cli.swagger_client.apis.buildrecords_api import BuildrecordsApi

# setup logging to print timestamps
logging.basicConfig(format='[%(asctime)s %(levelname)s] %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

POM_VERSION_UPDATE_REGEX_STR = r'^-\s*<version>([\w\.-]+)</version>\s*^\+\s*<version>(\d[\w\.-]*redhat-\d+)</version>'
POM_VERSION_UPDATE_REGEX = re.compile(POM_VERSION_UPDATE_REGEX_STR, re.MULTILINE)

BUILD_STATUS_DONE = 'DONE'

@pytest.fixture(scope='function', autouse=True)
def get_running_api():
    global running_api
    running_api = RunningbuildrecordsApi(utils.get_api_client())


@pytest.fixture(scope='function', autouse=True)
def get_configs_api():
    global configs_api
    configs_api = BuildconfigurationsApi(utils.get_api_client())


@pytest.fixture(scope='function', autouse=True)
def get_sets_api():
    global sets_api
    sets_api = BuildconfigurationsetsApi(utils.get_api_client())

@pytest.fixture(scope='function', autouse=True)
def get_records_api():
    global records_api
    records_api = BuildrecordsApi(utils.get_api_client())


@pytest.fixture(scope='function')
def new_project(request):
    project = projects.create_project(name=testutils.gen_random_name() + '-project')
    return project


@pytest.fixture(scope='function')
def new_environment(request):
    randname = testutils.gen_random_name()
    env = environments.create_environment(name=randname + '-environment', build_type='JAVA', image_id=randname)
    return env


@pytest.fixture(scope='function')
def new_config(request, new_environment, new_project):
    created_bc = configs_api.create_new(
        body=buildconfigurations.create_build_conf_object(
            name=testutils.gen_random_name() + '-config-build-exec-test',
            project=new_project,
            environment=new_environment,
            build_script='mvn javadoc:jar install',
            product_version_ids=[1],
            scm_repo_url='https://github.com/project-ncl/pnc-simple-test-project.git',
            scm_revision='1.0')).content

    return created_bc


def test_run_single_build(new_config):
    """ Run a single build configuration defined by the 'new_config' method
    and verify the build output """
    assert(new_config is not None, 'Unable to create build configuration')

    triggered_build = configs_api.trigger(id=new_config.id).content
    assert(triggered_build is not None, 'Unable to start build')

    logger.info("Build %s is running...", triggered_build.id)
    while True:
        if not running_api.get_all_for_bc(id=new_config.id).content:
            break
        time.sleep(5)
    logger.info("Build %s is done!", triggered_build.id)

    build_record = records_api.get_specific(triggered_build.id).content
    logger.info(str(build_record))
    assert(build_record is not None)
    assert(build_record.status == BUILD_STATUS_DONE)
    assert(build_record.scm_repo_url is not None)
    assert(build_record.scm_revision is not None)

    git_repo = checkout_git_sources(build_record.scm_repo_url, build_record.scm_revision)
    logger.info("Checked out sources of build " + str(build_record.id) + " to: " + git_repo.working_dir)
    diff = get_source_changes_in_last_commit(git_repo)
    assert(check_pom_for_redhat_version_update(diff))

    # Cleanup the local git repo
    shutil.rmtree(git_repo.working_dir)

    artifacts = records_api.get_built_artifacts(build_record.id).content
    assert(artifacts is not None)
    assert(len(artifacts) > 0)

def checkout_git_sources(repo_url, revision):
    repo_dir = os.path.join(tempfile.gettempdir(), revision)
    if (os.path.isdir(repo_dir)):
        logger.warn("Found existing git checkout directory: " + str(repo_dir))
        git_repo = Repo(repo_dir)
    else:
        git_repo = Repo.clone_from(repo_url, repo_dir)
    git_repo.head.reference = git_repo.commit(revision)
    git_repo.head.reset(index=True, working_tree=True)
    return git_repo

def get_source_changes_in_last_commit(repo):
    """ Get the changes made in the most recent commit"""
    return repo.git.diff('HEAD~1')

def check_pom_for_redhat_version_update(diff):
    """Check the POM file diff for the redhat version update"""
    search = POM_VERSION_UPDATE_REGEX.search(diff)
    return (search is not None)



