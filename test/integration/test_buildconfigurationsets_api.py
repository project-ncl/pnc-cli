import pytest

__author__ = 'thauser'

from pnc_cli import buildconfigurationsets
from pnc_cli import buildconfigurations
from pnc_cli import projects
from pnc_cli import environments
from pnc_cli import utils
from test import testutils
from pnc_cli.swagger_client.apis.buildconfigurationsets_api import BuildconfigurationsetsApi


@pytest.fixture(scope='function', autouse=True)
def get_sets_api():
    global sets_api
    sets_api = BuildconfigurationsetsApi(utils.get_api_client())


@pytest.fixture(scope='function')
def new_set():
    set = sets_api.create_new(
        body=buildconfigurationsets._create_build_config_set_object(name=testutils.gen_random_name(),
                                                                    productVersionId=1)).content
    return set


@pytest.fixture(scope='function')
def new_project():
    project = projects.create_project(name=testutils.gen_random_name() + '_project')
    return project


@pytest.fixture(scope='function')
def new_environment():
    randname = testutils.gen_random_name()
    env = environments.create_environment(name=randname + '_environment', build_type='JAVA', image_id=randname)
    return env


@pytest.fixture(scope='function')
def new_config(new_project, new_environment):
    created_bc = buildconfigurations.create_build_configuration(name=testutils.gen_random_name(),
                                                                project=new_project.id,
                                                                environment=new_environment.id,
                                                                build_status="UNKNOWN",
                                                                build_script='mvn clean install',
                                                                product_version_ids=[1],
                                                                scm_repo_url='https://github.com/thauser/simple-maven-build-pnc.git')

    return created_bc


def test_get_all():
    sets = sets_api.get_all().content
    assert sets is not None


def test_create(new_set):
    set_names = [set.name for set in sets_api.get_all(page_size=1000000).content]
    assert new_set.name in set_names


def test_get_specific(new_set):
    set = sets_api.get_specific(id=new_set.id)
    assert set is not None


def test_update(new_set):
    newname = "newname" + testutils.gen_random_name()
    updated_set = buildconfigurationsets._create_build_config_set_object(name=newname)
    sets_api.update(id=new_set.id, body=updated_set)
    retrieved_set = sets_api.get_specific(id=new_set.id).content
    assert retrieved_set.name == newname


def test_delete(new_set):
    sets_api.delete_specific(id=new_set.id)
    response = utils.checked_api_call(sets_api, 'get_specific', id=new_set.id)
    assert response is None


@pytest.mark.xfail(reason="doesn't reliably return valid json.")
def test_trigger(new_set):
    running_set = sets_api.trigger(id=new_set.id)
    assert running_set.ok


def test_get_configurations(new_config, new_set):
    sets_api.add_configuration(id=new_set.id, body=new_config)
    set_configs = sets_api.get_configurations(id=new_set.id)
    assert set_configs is not None


def test_add_configuration(new_config, new_set):
    sets_api.add_configuration(id=new_set.id, body=new_config)
    set_config_ids = [x.id for x in sets_api.get_configurations(id=new_set.id).content]
    assert new_config.id in set_config_ids


def test_get_build_records(new_set):
    response = sets_api.get_build_records(id=new_set.id)
    assert response
