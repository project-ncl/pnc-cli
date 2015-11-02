import pytest
from pnc_cli import projects
from pnc_cli.swagger_client.apis.projects_api import ProjectsApi
from pnc_cli import utils
from test import testutils

projects_api = ProjectsApi(utils.get_api_client())

@pytest.fixture(scope='function')
def new_project(request):
    project = projects_api.create_new(body=projects._create_project_object(name=testutils.gen_random_name())).content
    def teardown():
        existing = projects_api.get_all().content
        if existing and project.id in [x.id for x in existing]:
            projects_api.delete_specific(id=project.id)
    request.addfinalizer(teardown)
    return project

def test_get_project_list():
    projs = projects_api.get_all().content
    assert projs is not None


def test_create(new_project):
    proj_ids = [x.id for x in projects_api.get_all().content]
    assert new_project.id in proj_ids


def test_get_specific(new_project):
    assert projects_api.get_specific(new_project.id) is not None


def test_update(new_project):
    newname = 'newname' + testutils.gen_random_name()
    updated_project = projects._create_project_object(name=newname, description="pnc-cli test updated description")
    projects_api.update(id=new_project.id, body=updated_project)
    retrieved_project = projects_api.get_specific(new_project.id).content
    assert retrieved_project.name == newname and retrieved_project.description == 'pnc-cli test updated description'


def test_delete(new_project):
    proj_ids = [x.id for x in projects_api.get_all().content]
    assert new_project.id in proj_ids
    projects_api.delete_specific(new_project.id)
    proj_ids = [x.id for x in projects_api.get_all().content]
    assert new_project.id not in proj_ids


def test_project_exists(new_project):
    assert projects._project_exists(new_project.id)


def test_get_project_id_by_name(new_project):
    assert projects._project_exists(projects._get_project_id_by_name(new_project.name))
