import argparse

from pprint import pprint

from argh import arg
from six import iteritems

import logging
import datetime
from pnc_cli import utils
from pnc_cli.swagger_client import ProductMilestoneRest
from pnc_cli.swagger_client import ProductversionsApi
from pnc_cli.swagger_client import ProductmilestonesApi
from pnc_cli import productversions

productversions_api = ProductversionsApi(utils.get_api_client())
milestones_api = ProductmilestonesApi(utils.get_api_client())

def existing_product_milestone(id_input):
    utils.valid_id(id_input)
    if not product_milestone_exists(id_input):
        raise argparse.ArgumentTypeError("no ProductMilestone with ID {} exists.".format(id_input))
    return id_input


def product_milestone_exists(search_id):
    response = utils.checked_api_call(milestones_api, 'get_specific', id=search_id)
    return response is not None


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


def _valid_version_create(version):
    if not utils.is_valid_version(version, '^\d+\.\w+$'):
        raise argparse.ArgumentTypeError("Version must start with a number, followed by a dot and then a qualifier (e.g ER1).")
    return version


def _valid_version_update(version):
    if not utils.is_valid_version(version, '^\d+\.\d+\.\d+\.\w+$'):
        raise argparse.ArgumentTypeError(
            "The version should consist of three numeric parts and one alphanumeric qualifier each separated by a dot.")
    return version


def check_date_order(start_arg, end_arg):
    start_date = datetime.datetime.strptime(start_arg, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_arg, '%Y-%m-%d')
    if not start_date <= end_date:
        raise argparse.ArgumentTypeError("Error: start date must be before end date")


def get_product_version_from_milestone(milestone_id):
    return get_milestone(milestone_id).product_version_id


def unique_version_value(parent_product_version_id, version):
    parent_product_version = utils.checked_api_call(productversions_api, 'get_specific',
                                                    id=parent_product_version_id).content
    for milestone in parent_product_version.product_milestones:
        if milestone.version == version:
            raise argparse.ArgumentTypeError("Error: version already being used for another milestone")


@arg("product_version_id", help="ID of the ProductVersion to create a ProductMilestone from.",
     type=productversions.existing_product_version)
@arg("version", help="Version of the ProductMilestone. Will be appended to the version from product_version_id.",
     type=_valid_version_create)
@arg("starting_date", help="Planned starting date for the ProductMilestone.", type=utils.valid_date)
@arg("planned_end_date", help="Planned date for the end of this ProductMilestone.", type=utils.valid_date)
@arg("issue_tracker_url", help="Issue tracker URL for this ProductMilestone.", type=utils.valid_url)
def create_milestone(**kwargs):
    """
    Create a new ProductMilestone
    """
    check_date_order(kwargs.get('starting_date'), kwargs.get('planned_end_date'))

    base_version = str(productversions_api.get_specific(
        id=kwargs.get('product_version_id')).content.version)
    kwargs['version'] = base_version + "." + kwargs.get('version')

    unique_version_value(kwargs.get('product_version_id'), kwargs['version'])

    created_milestone = create_milestone_object(**kwargs)
    response = utils.checked_api_call(
        milestones_api,
        'create_new',
        body=created_milestone)
    if response:
        return response.content


@arg("id", help="ProductVersion ID to retrieve milestones for.", type=productversions.existing_product_version)
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


@arg("id", help="ProductMilestone ID to retrieve.", type=existing_product_milestone)
def get_milestone(id):
    response = utils.checked_api_call(milestones_api, 'get_specific', id=id)
    return response.content

#TODO: problem setting end date.
#TODO: incorrect date parsing.
#TODO: update_milestone does not work.
@arg("id", help="ProductMilestone ID to update.", type=existing_product_milestone)
@arg("version", help="New version for the ProductMilestone.", type=_valid_version_update)
@arg("starting_date", help="New start date for the ProductMilestone.", type=utils.valid_date)
@arg("end_date", help="New release date for the ProductMilestone.", type=utils.valid_date)
def update_milestone(id, **kwargs):
    """
    Update a ProductMilestone
    """
    check_date_order(kwargs.get('starting_date'), kwargs.get('end_date'))

    unique_version_value(get_product_version_from_milestone(id), kwargs.get('version'))

    existing_milestone = utils.checked_api_call(milestones_api, 'get_specific', id=id).content
    for key, value in iteritems(kwargs):
        setattr(existing_milestone, key, value)
    response = utils.checked_api_call(
        milestones_api, 'update', id=id, body=existing_milestone)
    if response:
        return response.content