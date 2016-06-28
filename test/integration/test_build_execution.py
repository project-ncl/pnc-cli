import httplib
import logging
import os
import re
import shutil
import tempfile
import time
from urlparse import urlparse

import pytest
from git import Repo

from pnc_cli import utils
from pnc_cli.swagger_client.apis.buildconfigurations_api import BuildconfigurationsApi
from pnc_cli.swagger_client.apis.buildconfigurationsets_api import BuildconfigurationsetsApi
from pnc_cli.swagger_client.apis.buildrecords_api import BuildrecordsApi
from pnc_cli.swagger_client.apis.runningbuildrecords_api import RunningbuildrecordsApi

# setup logging to print timestamps
from test.integration.conftest import new_config

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


def test_run_single_build(new_config):
    """ Run a single build configuration defined by the 'new_config' method
    and verify the build output """
    assert (new_config is not None, 'Unable to create build configuration')

    triggered_build = configs_api.trigger(id=new_config.id).content
    assert (triggered_build is not None, 'Unable to start build')

    logger.info("Build %s is running...", triggered_build.id)
    while True:
        if not running_api.get_all_for_bc(id=new_config.id).content:
            break
        time.sleep(5)
    logger.info("Build %s is done!", triggered_build.id)

    build_record = records_api.get_specific(triggered_build.id).content
    build_record_checks(build_record)


@pytest.mark.skip(reason="Blocked by issue with repour (NCL-2195)")
def test_run_group_build(request, new_set, new_environment, new_project):
    assert (new_set is not None, 'Unable to create Build Configuration Group')
    config_one = new_config(request, new_project, new_environment)
    config_two = new_config(request, new_project, new_environment)
    config_three = new_config(request, new_project, new_environment)
    sets_api.add_configuration(id=new_set.id, body=config_one)
    sets_api.add_configuration(id=new_set.id, body=config_two)
    sets_api.add_configuration(id=new_set.id, body=config_three)

    # this returns a list of build_records, one for each build configuration in the set
    triggered_build = sets_api.build(id=new_set.id).content
    assert (triggered_build is not None, 'Unable to start build')

    triggered_build_ids = [x.id for x in triggered_build]
    for id in triggered_build_ids:
        logger.info("Group Build: Build %s is running...", id)

    config_set_records = sets_api.get_all_build_config_set_records(id=new_set.id).content
    assert (config_set_records is not None, 'Unable to get running config set')
    assert (len(config_set_records) > 0, 'No running config sets found')

    while True:
        # TODO: this is not 100% reliable because the array we want might not be the first one (although it's very unlikely)
        # we have to do this for now because the id of the build config set record is only available in the header
        # location field of the triggered_build, and the header is not directly available from the swagger api response
        if not running_api.get_all_for_bc_set(id=config_set_records[0].id).content:
            break
        time.sleep(5)
    for id in triggered_build_ids:
        logger.info("Build %s is done!", id)

    for id in triggered_build_ids:
        build_record = records_api.get_specific(id=id).content
        build_record_checks(build_record)


def build_record_checks(build_record):
    logger.info(str(build_record))
    assert (build_record is not None)
    assert (build_record.status == BUILD_STATUS_DONE)
    assert (build_record.scm_repo_url is not None)
    assert (build_record.scm_revision is not None)

    git_repo = checkout_git_sources(build_record.scm_repo_url, build_record.scm_revision)
    logger.info("Checked out sources of build " + str(build_record.id) + " to: " + git_repo.working_dir)
    diff = get_source_changes_in_last_commit(git_repo)
    assert (check_pom_for_redhat_version_update(diff))

    # Cleanup the local git repo
    shutil.rmtree(git_repo.working_dir)

    build_record_artifact_checks(build_record.id)


def build_record_artifact_checks(build_record_id):
    ''' Check the the artifacts exist in the repository and have valid checksums'''
    artifacts = records_api.get_built_artifacts(build_record_id).content
    assert (artifacts is not None)
    assert (len(artifacts) > 0)

    # Check that each artifact URL points to a valid file and the checksums match
    for artifact in artifacts:
        parsed_url = urlparse(artifact.deploy_url)
        conn = httplib.HTTPConnection(parsed_url.netloc)
        conn.request('HEAD', parsed_url.path)
        response = conn.getresponse()
        assert (response.status == httplib.OK)

        conn = httplib.HTTPConnection(parsed_url.netloc)
        conn.request('GET', parsed_url.path + str('.md5'))
        response_body = conn.getresponse().read()
        assert (response_body == artifact.checksum)


def checkout_git_sources(repo_url, revision):
    repo_dir = os.path.join(tempfile.gettempdir(), revision)
    if (os.path.isdir(repo_dir)):
        logger.warn("Found existing git checkout directory: " + str(repo_dir))
        git_repo = Repo(repo_dir)
        origin = git_repo.remote("origin")
        origin.fetch()
    else:
        kwargs = {"config":"http.sslVerify=false"}
        git_repo = Repo.clone_from(repo_url, repo_dir, **kwargs)
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



