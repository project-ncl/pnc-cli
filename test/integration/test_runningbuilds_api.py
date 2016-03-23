import time

import pytest

from pnc_cli import buildconfigurations
from pnc_cli import projects
from pnc_cli import environments
from pnc_cli import utils
from test import testutils
from pnc_cli.swagger_client.apis.buildconfigurations_api import BuildconfigurationsApi
from pnc_cli.swagger_client.apis.runningbuildrecords_api import RunningbuildrecordsApi


@pytest.fixture(scope='function', autouse=True)
def get_running_api():
    global running_api
    running_api = RunningbuildrecordsApi(utils.get_api_client())

@pytest.fixture(scope='function', autouse=True)
def get_configs_api():
    global configs_api
    configs_api = BuildconfigurationsApi(utils.get_api_client())

@pytest.fixture(scope='function')
def new_project(request):
    project = projects.create_project(name=testutils.gen_random_name()+'_project')
    return project

@pytest.fixture(scope='function')
def new_environment(request):
    env = environments.create_environment(name=testutils.gen_random_name()+'_environment')
    return env

@pytest.fixture(scope='function')
def new_config(request, new_project, new_environment):
    created_bc = configs_api.create_new(
        body=buildconfigurations.create_build_conf_object(name=testutils.gen_random_name(),
                                                          project=new_project,
                                                          environment=new_environment,
                                                          build_status="UNKNOWN",
                                                          build_script='mvn clean install',
                                                          product_version_ids=[1],
                                                          scm_repo_url='https://github.com/thauser/simple-maven-build-pnc.git')).content

    return created_bc


def test_get_all(new_config):
    # start a build so that a build is running
    # need to run a legitimate build, create a buildconfiguration that will start running
    configs_api.trigger(id=new_config.id, rebuild_all=False)
    running_builds = running_api.get_all(page_size=1000).content
    assert running_builds is not None


def test_get_specific(new_config):
    # same as above
    triggered_build = configs_api.trigger(id=new_config.id).content
    running_build = running_api.get_specific(id=triggered_build.id)
    assert running_build is not None
