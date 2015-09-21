import random
import string
import pytest
from pnc_cli import projects
from pnc_cli.swagger_client.apis.projects_api import ProjectsApi
from pnc_cli import utils

projects_api = ProjectsApi(utils.get_api_client())

def _create_project():
    randname = utils.gen_random_name()
    return projects_api.create_new(body=projects._create_project_object(name=randname)).content

def test_get_project_list():
    projs = projects_api.get_all().content
    assert projs is not None

def test_create():
    new_proj = _create_project()
    proj_ids = [x.id for x in projects_api.get_all().content]
    assert new_proj.id in proj_ids

def test_get_specific():
    new_proj = _create_project()
    assert projects_api.get_specific(new_proj.id) is not None

def test_update():
    new_proj = _create_project()
    newname = 'newname' + utils.gen_random_name()
    updated_project = projects._create_project_object(name=newname, description="updated description")
    projects_api.update(id=new_proj.id, body=updated_project)
    retrieved_project = projects_api.get_specific(new_proj.id).content
    assert retrieved_project.name == newname and retrieved_project.description == 'updated description'

def test_delete():
    new_proj = _create_project()
    proj_ids = [x.id for x in projects_api.get_all().content]
    assert new_proj.id in proj_ids
    projects_api.delete_specific(new_proj.id)
    proj_ids = [x.id for x in projects_api.get_all().content]
    assert new_proj.id not in proj_ids

def test_project_exists():
    new_proj = _create_project()
    assert projects._project_exists(new_proj.id)

def test_get_project_id_by_name():
    new_proj = _create_project()
    assert projects._project_exists(projects._get_project_id_by_name(new_proj.name))


