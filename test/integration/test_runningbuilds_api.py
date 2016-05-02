import time

import pytest

from pnc_cli import buildconfigurationsets
from pnc_cli import buildconfigurations
from pnc_cli import projects
from pnc_cli import environments
from pnc_cli import utils
from test import testutils
from pnc_cli.swagger_client.apis.buildconfigurations_api import BuildconfigurationsApi
from pnc_cli.swagger_client.apis.runningbuildrecords_api import RunningbuildrecordsApi
from pnc_cli.swagger_client.apis.buildconfigurationsets_api import BuildconfigurationsetsApi


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
def new_config(request, new_project, new_environment):
    created_bc = configs_api.create_new(
        body=buildconfigurations.create_build_conf_object(
            name=testutils.gen_random_name() + '-config-running-builds-test',
            project=new_project,
            environment=new_environment,
            build_status="UNKNOWN",
            build_script='mvn clean install',
            product_version_ids=[1],
            scm_repo_url='https://github.com/project-ncl/pnc-simple-test-project.git',
            scm_revision='master')).content

    return created_bc


@pytest.fixture(scope='function')
def new_set(request, new_config):
    created_set = buildconfigurationsets.create_build_configuration_set(
        name=testutils.gen_random_name() + '-set-running-builds-test',
        build_configuration_ids=[new_config.id])
    return created_set


def test_get_all(new_config):
    # start a build so that a build is running
    # need to run a legitimate build, create a buildconfiguration that will start running
    configs_api.trigger(id=new_config.id, rebuild_all=False)
    running_builds = running_api.get_all(page_size=1000).content
    assert running_builds is not None


def test_get_specific_no_id():
    testutils.assert_raises_valueerror(running_api, 'get_specific', id=None)


def test_get_specific_invalid_param():
    testutils.assert_raises_typeerror(running_api, 'get_specific', id=1)


def test_get_specific(new_config):
    # same as above
    triggered_build = configs_api.trigger(id=new_config.id).content
    running_build = running_api.get_specific(id=triggered_build.id)
    assert running_build is not None


def test_get_all_for_bc_set_no_id():
    testutils.assert_raises_valueerror(running_api, 'get_all_for_bc_set', id=None)


def test_get_all_for_bc_set_invalid_param():
    testutils.assert_raises_typeerror(running_api, 'get_all_for_bc_set', id=1)


def test_get_all_for_bc_set(new_set):
    sets_api.build(id=new_set.id)
    response = running_api.get_all_for_bc_set(id=new_set.id)
    assert response is not None


def test_get_all_for_bc_no_id():
    testutils.assert_raises_valueerror(running_api, 'get_all_for_bc', id=None)


def test_get_all_for_bc_invalid_param():
    testutils.assert_raises_typeerror(running_api, 'get_all_for_bc', id=1)


def test_get_all_for_bc(new_config):
    configs_api.trigger(id=new_config.id)
    response = running_api.get_all_for_bc(id=new_config.id)
    assert response is not None

