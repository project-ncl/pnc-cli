__author__ = 'thauser'
from pnc_cli.swagger_client.apis import ProductmilestonesApi
from pnc_cli.swagger_client.apis import ProductversionsApi
from pnc_cli import utils
from pnc_cli import productmilestones
from pnc_cli import productversions
from test import testutils

milestone_api = ProductmilestonesApi(utils.get_api_client())

def create_product_milestone():
    return milestone_api.create_new(body=productmilestones.create_milestone_object(
        product_version_id=1, version=testutils.gen_random_version()+".1.GA", start_date="2015-01-01", planned_release_date="2015-01-02"
    )).content

def test_get_all():
    create_product_milestone()
    assert milestone_api.get_all().content is not None

def test_create_new():
    created = create_product_milestone()
    milestones = [m.id for m in milestone_api.get_all().content]
    assert created.id in milestones

def test_get_all_by_product_version_id():
    milestones = milestone_api.get_all_by_product_version_id(version_id=1).content
    assert milestones is not None

def test_get_specific():
    created = create_product_milestone()
    retrieved = milestone_api.get_specific(created.id).content
    assert created.to_dict() == retrieved.to_dict()


def test_update():
    created = create_product_milestone()
    created.download_url = "updatedUrlHere"
    milestone_api.update(id=created.id, body=created)
    updated = milestone_api.get_specific(created.id).content
    assert updated.to_dict() == created.to_dict()


