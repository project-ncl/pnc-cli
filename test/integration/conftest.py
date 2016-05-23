import datetime

__author__ = 'thauser'

import pytest
from test import testutils
from pnc_cli import utils
from pnc_cli import buildconfigurations
from pnc_cli import buildconfigurationsets
from pnc_cli import environments
from pnc_cli import products
from pnc_cli import productversions
from pnc_cli import productmilestones
from pnc_cli import productreleases
from pnc_cli import projects


@pytest.fixture(scope='module')
def new_product():
    product = products.create_product(name=testutils.gen_random_name() + "-product",
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


@pytest.fixture(scope='module')
def new_environment(request):
    randname = testutils.gen_random_name()
    env = environments.create_environment(name=randname,
                                          image_id=randname,
                                          system_image_type="DOCKER_IMAGE")

    def teardown():
        environments.delete_environment(id=env.id)

    request.addfinalizer(teardown)
    return env


@pytest.fixture(scope='function')
def new_set(request):
    set = buildconfigurationsets.create_build_configuration_set(name=testutils.gen_random_name() + "-set",
                                                                product_version_id=1)

    def teardown():
        buildconfigurationsets.delete_build_configuration_set(id=set.id)

    request.addfinalizer(teardown)
    return set


@pytest.fixture(scope='function')
def new_config(request, new_project, new_environment):
    created_bc = buildconfigurations.create_build_configuration(
        name=testutils.gen_random_name() + '-config',
        project=new_project.id,
        environment=new_environment.id,
        build_script='mvn javadoc:jar install',
        product_version_ids=[1],
        scm_repo_url='https://github.com/project-ncl/pnc-simple-test-project.git',
        scm_revision='1.0')

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
    starting = utils.unix_time_millis(datetime.datetime(2016, 1, 2, 12, 0, 0))
    ending = utils.unix_time_millis(datetime.datetime(2017, 1, 2, 12, 0, 0))
    milestone = productmilestones.create_milestone(
        version='1.build3',
        starting_date=starting,
        planned_end_date=ending,
        download_url='localhost:8080/build3',
        product_version_id=new_version.id)
    return milestone


@pytest.fixture(scope='module')
def new_release(new_milestone):
    release_time = utils.unix_time_millis(datetime.datetime(2016, 1, 2, 12, 0, 0))
    release = productreleases.create_release(
        version="1.DR1",
        release_date=release_time,
        download_url="pnc-cli-test-url",
        product_version_id=new_milestone.product_version_id,
        product_milestone_id=new_milestone.id,
        support_level='EOL'
    )
    return release