import pytest

__author__ = 'thauser'
from pnc_cli.swagger_client.apis import ProductmilestonesApi
from pnc_cli import utils
from pnc_cli import productmilestones
from test import testutils

milestone_api = ProductmilestonesApi(utils.get_api_client())

@pytest.fixture(scope='function')
def new_milestone():
    milestone = milestone_api.create_new(body=productmilestones.create_milestone_object(
        product_version_id=1, version=testutils.gen_random_version()+".1.GA", start_date="2015-01-01", planned_release_date="2015-01-02"
    )).content
    return milestone

def test_get_all(new_milestone):
    assert milestone_api.get_all().content is not None

def test_create_new(new_milestone):
    milestones = [m.id for m in milestone_api.get_all().content]
    assert new_milestone.id in milestones

def test_get_all_by_product_version_id():
    milestones = milestone_api.get_all_by_product_version_id(version_id=1).content
    assert milestones is not None

def test_get_specific(new_milestone):
    retrieved = milestone_api.get_specific(new_milestone.id).content
    assert new_milestone.to_dict() == retrieved.to_dict()


def test_update(new_milestone):
    new_milestone.download_url = "updatedUrlHere"
    milestone_api.update(id=new_milestone.id, body=new_milestone)
    updated = milestone_api.get_specific(new_milestone.id).content
    assert updated.to_dict() == new_milestone.to_dict()


