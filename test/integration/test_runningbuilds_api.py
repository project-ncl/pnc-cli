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


def test_get_all(new_config):
    # start a build so that a build is running
    # need to run a legitimate build, create a buildconfiguration that will start running
    configs_api.trigger(id=new_config.id)
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


def test_get_all_for_bc_no_id():
    testutils.assert_raises_valueerror(running_api, 'get_all_for_bc', id=None)


def test_get_all_for_bc_invalid_param():
    testutils.assert_raises_typeerror(running_api, 'get_all_for_bc', id=1)


def test_get_all_for_bc(new_config):
    configs_api.trigger(id=new_config.id)
    response = running_api.get_all_for_bc(id=new_config.id)
    assert response is not None

