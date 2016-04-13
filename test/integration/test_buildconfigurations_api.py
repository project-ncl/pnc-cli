import pytest
from pnc_cli import projects
from pnc_cli import environments
from pnc_cli import buildconfigurations
from pnc_cli.swagger_client.apis.buildconfigurations_api import BuildconfigurationsApi
from pnc_cli.swagger_client.apis.runningbuildrecords_api import RunningbuildrecordsApi
from pnc_cli import utils
from test import testutils

import time

current_time_millis = lambda: int(round(time.time() * 1000))


@pytest.fixture(scope='function', autouse=True)
def get_configs_api():
    global configs_api
    configs_api = BuildconfigurationsApi(utils.get_api_client())

@pytest.fixture(scope='function')
def new_project(request):
    project = projects.create_project(name=testutils.gen_random_name()+'-project')
    return project

@pytest.fixture(scope='function')
def new_environment(request):
    randname = testutils.gen_random_name()
    env = environments.create_environment(name=randname + '-environment', build_type='JAVA', image_id=randname)
    return env

@pytest.fixture(scope='function')
def new_config(request, new_project, new_environment):
    created_bc = configs_api.create_new(
        body=buildconfigurations.create_build_conf_object(name=testutils.gen_random_name(),
                                                          project=new_project,
                                                          environment=new_environment,
                                                          build_status="SUCCESS",
                                                          build_script='mvn clean install',
                                                          product_version_ids=[1],
                                                          scm_repo_url='https://github.com/thauser/simple-maven-build-pnc.git',
                                                          )).content

    return created_bc


def test_get_all_invalid_params():
    testutils.assert_raises_typeerror(configs_api, 'get_all')


def test_get_all():
    build_configurations = configs_api.get_all(page_index=0, page_size=10000000, sort="", q="").content
    assert build_configurations is not None


def test_create_build_configuration_invalid_params():
    testutils.assert_raises_typeerror(configs_api, 'create_new')


def test_create_build_configuration(new_config):
    bc_names = [bc.name for bc in configs_api.get_all(page_size=1000000).content]
    assert new_config.name in bc_names


def test_get_specific_no_id():
    testutils.assert_raises_valueerror(configs_api, 'get_specific', id=None)


def test_get_specific_invalid_param():
    testutils.assert_raises_typeerror(configs_api, 'get_specific', id=1)


def test_get_specific(new_config):
    assert configs_api.get_specific(id=new_config.id).content.to_dict() == new_config.to_dict()


def test_trigger_no_id():
    testutils.assert_raises_valueerror(configs_api, 'trigger', id=None)


def test_trigger_invalid_params():
    testutils.assert_raises_typeerror(configs_api, 'trigger', id=1)


def test_trigger(new_config):
    running_api = RunningbuildrecordsApi(utils.get_api_client())
    triggered_build = configs_api.trigger(id=new_config.id, rebuild_all=False).content
    assert triggered_build is not None
    build_record = running_api.get_specific(id=triggered_build.id)
    assert build_record is not None


def test_get_build_configuration_id_by_name(new_config):
    find_by_name = buildconfigurations.get_build_configuration_id_by_name(name=new_config.name)
    assert configs_api.get_specific(id=find_by_name).content.id == configs_api.get_specific(id=new_config.id).content.id


def test_get_all_by_product_id_no_id():
    testutils.assert_raises_valueerror(configs_api, 'get_all_by_product_id', product_id=None)


def test_get_all_by_product_id_invalid_param():
    testutils.assert_raises_typeerror(configs_api, 'get_all_by_product_id', product_id=1)


def test_get_all_by_product_id(new_config):
    # need to add bcs to some product

    response = configs_api.get_all_by_product_id(product_id=1, page_index=0, page_size=1000000, sort="", q="").content
    assert response is not None


def test_get_all_by_product_version_id_no_product_id():
    testutils.assert_raises_valueerror(configs_api, 'get_all_by_product_version_id', product_id=None, version_id=1)


def test_get_all_by_product_version_id_no_version_id():
    testutils.assert_raises_valueerror(configs_api, 'get_all_by_product_version_id', product_id=1, version_id=None)


def test_get_all_by_product_version_id_invalid_param():
    testutils.assert_raises_typeerror(configs_api, 'get_all_by_product_version_id', product_id=1, version_id=1)


def test_get_all_by_product_version_id(new_config):
    # need to add bcs to some product version

    response = configs_api.get_all_by_product_version_id(product_id=1, version_id=1, page_index=0, page_size=1000000,
                                                         sort="", q="").content
    assert response is not None


def test_get_all_by_project_id_no_id():
    testutils.assert_raises_valueerror(configs_api, 'get_all_by_project_id', project_id=None)


def test_get_all_by_project_id_invalid_param():
    testutils.assert_raises_typeerror(configs_api, 'get_all_by_project_id', project_id=1)


def test_get_all_by_project_id():
    response = configs_api.get_all_by_project_id(project_id=1, page_index=0, page_size=1000000, sort="", q="").content
    assert response is not None


def test_update_no_id():
    testutils.assert_raises_valueerror(configs_api, 'update', id=None)


def test_update_invalid_param():
    testutils.assert_raises_typeerror(configs_api, 'update', id=1)


def test_update(new_config):
    ignored_keys = ('last_modification_time')
    new_config.description = "This is a new description for testing update functionality"
    new_config.name = "pnc-cli-test-updated-" + new_config.name
    configs_api.update(id=new_config.id, body=new_config)
    updated = configs_api.get_specific(id=new_config.id).content
    keys_updated = set(updated.attribute_map).difference(ignored_keys)
    keys_new_config = set(new_config.attribute_map).difference(ignored_keys)
    assert keys_updated == keys_new_config and (getattr(updated, key) == getattr(new_config, key) for key in keys_updated)


def test_delete_specific_no_id():
    testutils.assert_raises_valueerror(configs_api, 'delete_specific', id=None)


def test_delete_specific_invalid_param():
    testutils.assert_raises_typeerror(configs_api, 'delete_specific', id=1)


def test_delete_specific(new_config):
    existing_ids = [bc.id for bc in configs_api.get_all(page_size=1000000).content]
    assert new_config.id in existing_ids
    configs_api.delete_specific(id=new_config.id)
    existing_ids = [bc.id for bc in configs_api.get_all(page_size=1000000).content]
    assert new_config.id not in existing_ids


def test_get_build_records_no_id():
    testutils.assert_raises_valueerror(configs_api, 'get_build_records', id=None)


def test_get_build_records_invalid_param():
    testutils.assert_raises_typeerror(configs_api, 'get_build_records', id=1)


def test_get_build_records():
    response = configs_api.get_build_records(id=1, page_index=0, page_size=1000000, sort='', q='').content
    assert response is not None


def test_get_latest_build_record_no_id():
    testutils.assert_raises_valueerror(configs_api, 'get_latest_build_record', id=None)


def test_get_latest_build_record_invalid_param():
    testutils.assert_raises_typeerror(configs_api, 'get_latest_build_record', id=1)


def test_get_latest_build_record():
    response = configs_api.get_latest_build_record(id=1).content
    assert response is not None


def test_clone_no_id():
    testutils.assert_raises_valueerror(configs_api, 'clone', id=None)


def test_clone_invalid_param():
    testutils.assert_raises_typeerror(configs_api, 'clone', id=1)


def test_clone(new_config):
    cloned_bc = configs_api.clone(id=new_config.id).content
    expected_unchanged_fields = ['description',
                                 'build_script',
                                 'scm_repo_url',
                                 'scm_revision',
                                 'scm_mirror_repo_url',
                                 'scm_mirror_revision',
                                 'build_status',
                                 'repositories',
                                 'environment',
                                 'dependency_ids',
                                 'internal_scm',
                                 'internal_scm_revison']
    for x in expected_unchanged_fields:
        print('Testing {}'.format(x))
        assert cloned_bc.to_dict().get(x) == new_config.to_dict().get(x)
    # cleanup
    configs_api.delete_specific(id=cloned_bc.id)


def test_get_dependencies_no_id():
    testutils.assert_raises_valueerror(configs_api, 'get_dependencies', id=None)


def test_get_dependencies_invalid_param():
    testutils.assert_raises_typeerror(configs_api, 'get_dependencies', id=1)


def test_add_dependency_no_id():
    testutils.assert_raises_valueerror(configs_api, 'add_dependency', id=None)


def test_add_dependency_invalid_param():
    testutils.assert_raises_typeerror(configs_api, 'add_dependency', id=1)


def test_remove_dependency_no_bc_id():
    testutils.assert_raises_valueerror(configs_api, 'remove_dependency', id=None, dependency_id=1)


def test_remove_dependency_no_dep_id():
    testutils.assert_raises_valueerror(configs_api, 'remove_dependency', id=1, dependency_id=None)


def test_remove_dependency_invalid_param():
    testutils.assert_raises_typeerror(configs_api, 'remove_dependency', id=1, dependency_id=1)


# add_dependency
# get_dependencies
# remove_dependency
def test_dependency_operations(new_config):
    dep = configs_api.get_specific(id=1).content
    configs_api.add_dependency(id=new_config.id, body=dep)
    dependency_ids = [dep.id for dep in
                      configs_api.get_dependencies(id=new_config.id, page_index=0, page_size=1000000, sort='',
                                                   q='').content]
    assert dep.id in dependency_ids
    configs_api.remove_dependency(id=new_config.id, dependency_id=dep.id)
    assert not configs_api.get_dependencies(id=new_config.id).content


def test_get_product_versions_no_id():
    testutils.assert_raises_valueerror(configs_api, 'get_product_versions', id=None)


def test_get_product_versions_invalid_param():
    testutils.assert_raises_typeerror(configs_api, 'get_product_versions', id=1)


def test_remove_product_version_no_bc_id():
    testutils.assert_raises_valueerror(configs_api, 'remove_product_version', id=None, product_version_id=1)


def test_remove_product_version_no_version_id():
    testutils.assert_raises_valueerror(configs_api, 'remove_product_version', id=1, product_version_id=None)


def test_remove_product_version_invalid_param():
    testutils.assert_raises_typeerror(configs_api, 'remove_product_version', id=1, product_version_id=1)


def test_add_product_version_no_id():
    testutils.assert_raises_valueerror(configs_api, 'add_product_version', id=None)


def test_add_product_version_invalid_param():
    testutils.assert_raises_typeerror(configs_api, 'add_product_version', id=1)


# add_product_version
# get_product_versions
# remove_product_version
# TODO: cannot test due to test_productversions_api incomplete
def test_product_version_operations(new_config):
    pass


def test_get_revisions_no_id():
    testutils.assert_raises_valueerror(configs_api, 'get_revisions', id=None)


def test_get_revisions_invalid_param():
    testutils.assert_raises_typeerror(configs_api, 'get_revisions', id=1)


def test_get_revision_no_bc_id():
    testutils.assert_raises_valueerror(configs_api, 'get_revision', id=None, rev=1)


def test_get_revision_no_rev_id():
    testutils.assert_raises_valueerror(configs_api, 'get_revision', id=1, rev=None)


def test_get_revision_invalid_param():
    testutils.assert_raises_typeerror(configs_api, 'get_revision', id=1, rev=1)


# get_revisions
# get_revision
@pytest.mark.xfail(reason='get_revisions is currently non-functional.')
def test_revision_operations(new_config):
    revisions = configs_api.get_revisions(id=new_config.id).content
    assert revisions is not None
    revision = configs_api.get_revision(id=new_config.id, rev=revisions[0].id)
    assert revision is not None


def test_get_build_configuration_sets_no_id():
    testutils.assert_raises_typeerror(configs_api, 'get_build_configuration_sets')


def test_get_build_configuration_sets_invalid_param():
    testutils.assert_raises_valueerror(configs_api, 'get_build_configuration_sets', id=None)


def test_get_build_configuration_sets():
    build_configuration_sets = configs_api.get_build_configuration_sets(id=1).content
    assert build_configuration_sets is not None


