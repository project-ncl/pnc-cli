import random
import string
import pytest
from pnc import projects

def _create_project():
    randname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    new_project = projects.create_project(randname)
    return new_project

def test_list_projects():
    projs = projects.list_projects()
    assert projs is not None

def test_list_projects_attributes():
    projs = projects.list_projects(attributes='name,description')
    assert projs is not None

def test_create_project():
    new_proj = _create_project()
    proj_ids = [x['id'] for x in projects.list_projects()]
    assert new_proj['id'] in proj_ids

def test_get_project():
    new_proj = _create_project()
    assert projects.get_project(new_proj['id']) is not None

@pytest.mark.xfail(reason='currently server gives 409 error upon executing projects.update_project')
def test_update_project():
    new_proj = _create_project()
    projects.update_project(new_proj['id'], "updated project", "updated description")
    updated_proj = projects.get_project(new_proj['id'])
    assert updated_proj['name'] == 'updated project' and updated_proj['description'] == 'updated description'

def test_delete_project():
    new_proj = _create_project()
    proj_ids = [x['id'] for x in projects.list_projects()]
    # new project exists in the projects list
    assert new_proj['id'] in proj_ids
    projects.delete_project(id=new_proj['id'])
    proj_ids = [x['id'] for x in projects.list_projects()]
    # new project is missing from the projects list
    assert new_proj['id'] not in proj_ids

def test_project_exists():
    new_proj = _create_project()
    assert projects._project_exists(new_proj['id'])

def test_get_project_id_by_name():
    new_proj = _create_project()
    assert projects._project_exists(projects._get_project_id_by_name(new_proj['name']))


