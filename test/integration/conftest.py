__author__ = 'thauser'

import pytest

import pnc_cli.user_config as uc
from pnc_cli import buildconfigurations
from pnc_cli import buildconfigurationsets
from pnc_cli import productmilestones
from pnc_cli import productreleases
from pnc_cli import products
from pnc_cli import productversions
from pnc_cli import projects
from test import testutils


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


# helper function for checking BC creation
def contains_event_type(events, types):
    for event in events:
        if (event.event_type in types):
            return True
    return False

@pytest.fixture(scope='function')
def new_config(request, new_project, new_version):
    created_bc = create_config(request, new_project, new_version, 1)
    return created_bc


def create_config(request, new_project, new_version, project_number):
    if (project_number == 2):
        ending = '-2'
    elif (project_number == 3):
        ending = '-3'
    else:
        ending = ''

    # detect our environment.
    if "stage" in uc.user.pnc_config.url:
        repo_url = 'git+ssh://pnc-gerrit-stage@code-stage.eng.nay.redhat.com:29418/productization/github.com/pnc-simple-test-project'+ending+'.git'
        env = 2
    elif "devel" in uc.user.pnc_config.url:
        repo_url = 'git+ssh://user-pnc-gerrit@pnc-gerrit.pnc.dev.eng.bos.redhat.com:29418/productization/github.com/pnc-simple-test-project'+ending+'.git'
        env = 3

    bc_name = testutils.gen_random_name() + '-config'
    created_bc = buildconfigurations.create_build_configuration(
        name=bc_name,
        project=new_project.id,
        environment=env,
        build_script='mvn deploy',
        product_version_id=new_version.id,
        scm_repo_url=repo_url,
        scm_revision='master')

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
