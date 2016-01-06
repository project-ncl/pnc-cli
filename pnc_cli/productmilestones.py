from pprint import pprint

from argh import arg
from six import iteritems

import logging
from pnc_cli import utils
from pnc_cli.swagger_client import ProductMilestoneRest
from pnc_cli.swagger_client import ProductversionsApi
from pnc_cli.swagger_client import ProductmilestonesApi

productversions_api = ProductversionsApi(utils.get_api_client())
milestones_api = ProductmilestonesApi(utils.get_api_client())


def product_version_exists(search_id):
    return str(search_id) in [str(x.id) for x in productversions_api.get_all().content]


def create_milestone_object(**kwargs):
    created_milestone = ProductMilestoneRest()
    for key, value in iteritems(kwargs):
        setattr(created_milestone, key, value)
    return created_milestone


@arg("-p", "--page-size", help="Limit the amount of ProductReleases returned")
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_milestones(page_size=200, q="", sort=""):
    """
    List all ProductMilestones
    """
    response = utils.checked_api_call(milestones_api, 'get_all', page_size=page_size, q=q, sort=sort).content
    if response:
        return response


@arg("product_version_id", help="ID of the ProductVersion to create a ProductMilestone from.")
@arg("version", help="Version of the ProductMilestone. Will be appended to the version from product_version_id.")
@arg("starting_date", help="Planned starting date for the ProductMilestone.")
@arg("planned_release_date", help="Planned date for the ProductMilestone release.")
def create_milestone(**kwargs):
    """
    Create a new ProductMilestone
    """
    if not product_version_exists(kwargs.get('product_version_id')):
        logging.error("No ProductVersion exists with the ID {}.".format(
            kwargs.get('product_version_id')))
        return
    version = kwargs.get('version')

    if not utils.is_valid_version(version):
        logging.error("Version must start with a number, followed by a dot and then a qualifier (e.g ER1).")
        return
    base_version = str(productversions_api.get_specific(
        id=kwargs.get('product_version_id')).content.version)
    kwargs['version'] = base_version + "." + kwargs.get('version')
    created_milestone = create_milestone_object(**kwargs)
    response = utils.checked_api_call(
        milestones_api,
        'create_new',
        body=created_milestone)
    if response:
        return response.content


@arg("id", help="ProductVersion ID to retrieve milestones for.")
def list_milestones_for_version(id):
    """
    List ProductMilestones for a specific ProductVersion
    """
    response = utils.checked_api_call(
        milestones_api,
        'get_all_by_product_version_id',
        version_id=id).content
    if response:
        return response


@arg("id", help="ProductMilestone ID to retrieve.")
def get_milestone(id):
    response = utils.checked_api_call(milestones_api, 'get_specific', id=id).content
    if response:
        return response


@arg("id", help="ProductMilestone ID to update.")
@arg("version", help="New version for the ProductMilestone.")
@arg("start_date", help="New start date for the ProductMilestone.")
@arg("release_date", help="New release date for the ProductMilestone.")
def update_milestone(id, **kwargs):
    existing_milestone = milestones_api.get_specific(id=id).content
    for key, value in iteritems(kwargs):
        setattr(existing_milestone, key, value)
    response = utils.checked_api_call(
        milestones_api, 'update', id=id, body=existing_milestone).content
    if response:
        return response
