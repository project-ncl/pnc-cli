from pprint import pprint

from argh import arg
from six import iteritems

from pnc_cli import utils
from pnc_cli.swagger_client import ProductMilestoneRest
from pnc_cli.swagger_client import ProductversionsApi
from pnc_cli.swagger_client import ProductmilestonesApi

productversions_api = ProductversionsApi(utils.get_api_client())
milestones_api = ProductmilestonesApi(utils.get_api_client())


def create_milestone_object(**kwargs):
    created_milestone = ProductMilestoneRest()
    for key, value in iteritems(kwargs):
        setattr(created_milestone, key, value)
    return created_milestone


@arg("-p", "--page-size", help="Limit the amount of product releases returned")
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_milestones(page_size=200, q="", sort=""):
    """
    List all ProductMilestones
    """
    response = utils.checked_api_call(milestones_api, 'get_all', page_size=page_size, q=q, sort=sort)
    if response:
        pprint(response.content)


@arg("product_version_id", help="ID of the product version to create a milestone from.")
@arg("version", help="Version of the milestone. Will be appended to the version from product_version_id.")
@arg("start_date", help="Planned starting date for the milestone.")
@arg("planned_release_date", help="Planned date for the milestone release.")
def create_milestone(**kwargs):
    """
    Create a new ProductMilestone
    """
    if kwargs.get('product_version_id') not in [
            str(x.id) for x in productversions_api.get_all().content]:
        print("No product version exists with the ID {}.").format(
            kwargs.get('product_version_id'))
        return
    version = kwargs.get('version')

    if not utils.is_valid_version(version):
        print("Version must start with a number, followed by a dot and then a qualifier (e.g ER1).")
        return
    base_version = productversions_api.get_specific(
        id=kwargs.get('product_version_id')).content.version
    kwargs['version'] = base_version + "." + kwargs.get('version')
    created_milestone = create_milestone_object(**kwargs)
    response = utils.checked_api_call(
        milestones_api,
        'create_new',
        body=created_milestone)
    if response:
        pprint(response.content)


@arg("id", help="Product version ID to retrieve milestones for.")
def list_milestones_for_version(id):
    """
    List ProductMilestones for a specific ProductVersion
    """
    response = utils.checked_api_call(
        milestones_api,
        'get_all_by_product_version_id',
        version_id=id)
    if response:
        pprint(response.content)


@arg("id", help="Product milestone ID to retrieve.")
def get_milestone(id):
    response = utils.checked_api_call(milestones_api, 'get_specific', id=id)
    if response:
        pprint(response.content)


@arg("id", help="Product milestone ID to update.")
@arg("version", help="New version for the milestone.")
@arg("start_date", help="New start date for the milestone.")
@arg("release_date", help="New release date for the milestone.")
def update_milestone(id, **kwargs):
    existing_milestone = milestones_api.get_specific(id)
    for key, value in iteritems(kwargs):
        setattr(existing_milestone, key, value)
    response = utils.checked_api_call(
        milestones_api, 'update', id=id, body=existing_milestone)
    if response:
        pprint(response)
