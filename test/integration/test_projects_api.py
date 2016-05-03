import pytest
from pnc_cli import projects
from pnc_cli.swagger_client.apis.projects_api import ProjectsApi
from pnc_cli import utils
from test import testutils

@pytest.fixture(scope='function', autouse=True)
def get_projects_api():
    global projects_api
    projects_api = ProjectsApi(utils.get_api_client())


@pytest.fixture(scope='module')
def new_project(request):
    project = projects_api.create_new(body=projects._create_project_object(name=testutils.gen_random_name())).content
    def teardown():
        projects.delete_project(id=project.id)
    request.addfinalizer(teardown)
    return project


def test_get_all_invalid_param():
    testutils.assert_raises_typeerror(projects_api, 'get_all')


def test_get_all():
    projs = projects_api.get_all(page_index=0, page_size=1000000, sort='', q='').content
    assert projs is not None


def test_create_new_invalid_param():
    testutils.assert_raises_typeerror(projects_api, 'create_new')


def test_create_new(new_project):
    proj_ids = [x.id for x in projects_api.get_all(page_size=1000000).content]
    assert new_project.id in proj_ids


def test_get_specific_no_id():
    testutils.assert_raises_valueerror(projects_api, 'get_specific', id=None)


def test_get_specific_invalid_param():
    testutils.assert_raises_typeerror(projects_api, 'get_specific', id=1)


def test_get_specific(new_project):
    assert projects_api.get_specific(new_project.id) is not None


def test_update_no_id():
    testutils.assert_raises_valueerror(projects_api, 'update', id=None)


def test_update_invalid_param():
    testutils.assert_raises_typeerror(projects_api, 'update', id=1)


def test_update(new_project):
    newname = 'newname' + testutils.gen_random_name()
    updated_project = projects._create_project_object(name=newname, description="pnc-cli test updated description")
    projects_api.update(id=new_project.id, body=updated_project)
    retrieved_project = projects_api.get_specific(new_project.id).content
    assert retrieved_project.name == newname and retrieved_project.description == 'pnc-cli test updated description'


def test_delete_specific_no_id():
    testutils.assert_raises_valueerror(projects_api, 'delete_specific', id=None)


def test_delete_specific_invalid_param():
    testutils.assert_raises_typeerror(projects_api, 'delete_specific', id=1)


def test_delete_specific(new_project):
    proj_ids = [x.id for x in projects_api.get_all(page_size=1000000).content]
    assert new_project.id in proj_ids
    projects_api.delete_specific(new_project.id)
    proj_ids = [x.id for x in projects_api.get_all(page_size=1000000).content]
    assert new_project.id not in proj_ids
