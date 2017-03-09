__author__ = 'thauser'

import pytest
import time
from test import testutils
from pnc_cli import buildconfigurations
from pnc_cli import buildconfigurationsets
from pnc_cli import bpmbuildconfigurations
from pnc_cli import products
from pnc_cli import productversions
from pnc_cli import productmilestones
from pnc_cli import productreleases
from pnc_cli import projects


@pytest.fixture(scope='module')
def new_product():
    randname = testutils.gen_random_name()
    product = products.create_product(randname + "-product",
                                      randname,
                                      description="PNC CLI: test product")
    return product


@pytest.fixture(scope='module')
def new_project(request):
    project = projects.create_project(name=testutils.gen_random_name() + '-project',
                                      description="PNC CLI: test project")

    def teardown():
        projects.delete_project(id=project.id)

    request.addfinalizer(teardown)
    return project


@pytest.fixture(scope='function')
def new_set(request):
    set = buildconfigurationsets.create_build_configuration_set(name=testutils.gen_random_name() + "-set",
                                                                product_version_id=1)

    def teardown():
        buildconfigurationsets.delete_build_configuration_set(id=set.id)

    request.addfinalizer(teardown)
    return set

#helper function for checking BC creation
def contains_event_type(events, types):
    for event in events:
        if (event.event_type in types):
            return True

    return False

@pytest.fixture(scope='function')
#def new_config(request, new_project, new_environment):
def new_config(request, new_project):
    bc_name = testutils.gen_random_name() + '-config'
    task_id = bpmbuildconfigurations.create_build_configuration(
        name=bc_name,
        project=new_project.id,
        build_environment=1,
        build_script='mvn javadoc:jar deploy',
        product_version_id=1,
        scm_external_repo_url='https://github.com/project-ncl/pnc-simple-test-project.git',
        scm_external_revision='master')

    error_event_types = (
    "BCC_CONFIG_SET_ADDITION_ERROR", "BCC_CREATION_ERROR", "BCC_REPO_CLONE_ERROR", "BCC_REPO_CREATION_ERROR")
    # wait for BC creation to complete.
    time.sleep(2)
    while True:
        bpm_task = bpmbuildconfigurations.get_bpm_task_by_id(task_id)

        if contains_event_type(bpm_task.content.events, ("BCC_CREATION_SUCCESS",)):
            break

        if contains_event_type(bpm_task.content.events, error_event_types):
            return None

        time.sleep(10)

    created_bc = buildconfigurations.get_build_configuration_by_name(bc_name)

    def teardown():
        buildconfigurations.delete_build_configuration(id=created_bc.id)

    request.addfinalizer(teardown)
    return created_bc


@pytest.fixture(scope='module')
def new_version(new_product):
    version = productversions.create_product_version(
        product_id=new_product.id,
        version=get_unique_version(new_product.id))
    return version


def get_unique_version(product_id):
    rand_version = testutils.gen_random_version()
    existing = products.list_versions_for_product(id=product_id, page_size=100000)
    while existing is not None and rand_version in [x.version for x in existing]:
        rand_version = testutils.gen_random_version()
    return rand_version


@pytest.fixture(scope='module')
def new_milestone(new_version):
    starting = '2015-01-01'
    ending = '2016-01-01'
    milestone = productmilestones.create_milestone(
        version='1.build3',
        starting_date=starting,
        planned_end_date=ending,
        download_url='localhost:8080/build3',
        product_version_id=new_version.id)
    return milestone


@pytest.fixture(scope='module')
def new_release(new_milestone):
    release_time = '2016-01-01'
    release = productreleases.create_release(
        version="1.DR1",
        release_date=release_time,
        download_url="pnc-cli-test-url",
        product_version_id=new_milestone.product_version_id,
        product_milestone_id=new_milestone.id,
        support_level='EOL'
    )
    return release