import argparse
import datetime
import logging
import time

from argh import arg
from six import iteritems

import pnc_cli.cli_types as types
import pnc_cli.utils as utils
from pnc_cli.swagger_client import ProductMilestoneRest
from pnc_cli.pnc_api import pnc_api


def create_milestone_object(**kwargs):
    created_milestone = ProductMilestoneRest()
    for key, value in iteritems(kwargs):
        setattr(created_milestone, key, value)
    return created_milestone 
def check_date_order(start_date, end_date):
    if not start_date <= end_date:
        raise argparse.ArgumentTypeError("Error: start date must be before end date")


def get_product_version_from_milestone(milestone_id):
    return get_milestone(milestone_id).product_version_id


def unique_version_value(parent_product_version_id, version):
    parent_product_version = utils.checked_api_call(pnc_api.product_versions, 'get_specific',
                                                    id=parent_product_version_id).content
    for milestone in parent_product_version.product_milestones:
        if milestone.version == version:
            raise argparse.ArgumentTypeError("Error: version already being used for another milestone")


@arg("-p", "--page-size", help="Limit the amount of ProductReleases returned", type=int)
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_milestones(page_size=200, page_index=0, q="", sort=""):
    """
    List all ProductMilestones
    """
    data = list_milestones_raw(page_size, page_index, sort, q)
    if data:
        return utils.format_json_list(data)

def list_milestones_raw(page_size=200, page_index=0, sort="", q=""):
    response = utils.checked_api_call(pnc_api.product_milestones, 'get_all', page_size=page_size, page_index=page_index, q=q, sort=sort)
    if response:
        return response.content


@arg("product_version_id", help="ID of the ProductVersion to create a ProductMilestone from.",
     type=types.existing_product_version)
@arg("version", help="Version of the ProductMilestone. Will be appended to the version from product_version_id.",
     type=types.valid_version_create)
@arg("starting_date", help="Planned starting date for the ProductMilestone.", type=types.valid_date)
@arg("planned_end_date", help="Planned date for the end of this ProductMilestone.", type=types.valid_date)
@arg("issue_tracker_url", help="Issue tracker URL for this ProductMilestone.", type=types.valid_url)
def create_milestone(**kwargs):
    """
    Create a new ProductMilestone
    """
    data = create_milestone_raw(**kwargs)
    if data:
        return utils.format_json(data)

def create_milestone_raw(**kwargs):
    check_date_order(kwargs.get('starting_date'), kwargs.get('planned_end_date'))

    base_version = str(pnc_api.product_versions.get_specific(
        id=kwargs.get('product_version_id')).content.version)
    kwargs['version'] = base_version + "." + kwargs.get('version')

    unique_version_value(kwargs.get('product_version_id'), kwargs['version'])

    created_milestone = create_milestone_object(**kwargs)
    response = utils.checked_api_call(
        pnc_api.product_milestones,
        'create_new',
        body=created_milestone)
    if response:
        return response.content


@arg("id", help="ProductVersion ID to retrieve milestones for.", type=types.existing_product_version)
def list_milestones_for_version(id):
    """
    List ProductMilestones for a specific ProductVersion
    """
    data = list_milestones_for_version_raw(id)
    if data:
        return utils.format_json_list(data)

def list_milestones_for_version_raw(id):
    response = utils.checked_api_call(
        pnc_api.product_milestones,
        'get_all_by_product_version_id',
        version_id=id)
    if response:
        return response.content


@arg("id", help="ProductMilestone ID to retrieve.", type=types.existing_product_milestone)
def get_milestone(id):
    data = get_milestone_raw(id)
    if data:
        return utils.format_json(data)

def get_milestone_raw(id):
    response = utils.checked_api_call(pnc_api.product_milestones, 'get_specific', id=id)
    return response.content


@arg("id", help="ProductMilestone ID to update.", type=types.existing_product_milestone)
@arg("-v", "--version", help="New version for the ProductMilestone.", type=types.valid_version_update)
@arg("-sd", "--starting-date", help="New start date for the ProductMilestone.", type=types.valid_date)
@arg("-ped", "--planned-end-date", help="New release date for the ProductMilestone.", type=types.valid_date)
def update_milestone(id, **kwargs):
    """
    Update a ProductMilestone
    """
    data = update_milestone_raw(id, **kwargs)
    if data:
        return utils.format_json(data)

def update_milestone_raw(id, **kwargs):
    existing_milestone = utils.checked_api_call(pnc_api.product_milestones, 'get_specific', id=id).content
    existing_start_date = existing_milestone.starting_date
    existing_end_date = existing_milestone.planned_end_date
    updated_start_date = kwargs.get('starting_date')
    updated_ending_date = kwargs.get('planned_end_date')

    if updated_start_date and updated_ending_date:
        check_date_order(updated_start_date, updated_ending_date)
    elif updated_start_date:
        check_date_order(updated_start_date, existing_end_date)
    elif updated_ending_date:
        check_date_order(existing_start_date, updated_ending_date)

    if kwargs.get('version'):
        unique_version_value(get_product_version_from_milestone(id), kwargs.get('version'))

    for key, value in iteritems(kwargs):
        setattr(existing_milestone, key, value)
    response = utils.checked_api_call(
        pnc_api.product_milestones, 'update', id=id, body=existing_milestone)
    if response:
        return response.content


@arg("id", help="ProductMilestone ID to update.", type=types.existing_product_milestone)
@arg("-w", "--wait", help="Wait for release process to finish", action='store_true')
def close_milestone(id, **kwargs):
    """
    Close a milestone. This triggers its release process.

    The user can optionally specify the release-date, otherwise today's date is
    used.

    If the wait parameter is specified and set to True, upon closing the milestone,
    we'll periodically check that the release being processed is done.

    Required:
    - id: int

    Optional:
    - wait key: bool
    """
    data = close_milestone_raw(id, **kwargs)
    if data:
        return utils.format_json(data)

def close_milestone_raw(id, **kwargs):
    existing_milestone = utils.checked_api_call(pnc_api.product_milestones, 'get_specific', id=id).content

    response = utils.checked_api_call(
        pnc_api.product_milestones, 'close_milestone', id=id, body=existing_milestone)

    latest_release = utils.checked_api_call(pnc_api.product_milestones, 'get_latest_release', id=id).content

    if kwargs.get('wait') == True:
        while latest_release.status == 'IN_PROGRESS':
            logging.info("Latest release for milestone is in progress, waiting till it finishes...")
            time.sleep(60)
            latest_release = utils.checked_api_call(pnc_api.product_milestones, 'get_latest_release', id=id).content

        logging.error("Status of release for milestone: " + latest_release.status)

    if response:
        return response.content


@arg("id", help="ID of the ProductMilestone to list distributed artifacts for.", type=types.existing_product_milestone)
@arg("-p", "--page-size", help="Limit the amount of distributed artifacts returned", type=int)
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_distributed_artifacts(id, page_size=200, page_index=0, sort="", q=""):
    data = list_distributed_artifacts_raw(id, page_size, page_index, sort, q)
    if data:
        return utils.format_json_list(data)

def list_distributed_artifacts_raw(id, page_size=200, page_index=0, sort="", q=""):
    response = utils.checked_api_call(pnc_api.product_milestones, 'get_distributed_artifacts', id=id, page_size=page_size, page_index=page_index, sort=sort, q=q)
    if response:
        return response.content


@arg('id', help="ID of the ProductMilestone to add a distributed artifact to.", type=types.existing_product_milestone)
#TODO: come up with a way to check that a given artifact ID exists. Currently the REST API doesn't have a method available like
# get_specific for the artifacts
@arg('artifact_id', help='ID of the Artifact to add.', type=types.existing_built_artifact)
def add_distributed_artifact():
    pass


@arg('id', help="ID of the ProductMilestone to remove the distributed artifact from.", type=types.existing_product_milestone)
@arg('artifact_id', help='ID of the distributed artifact to remove.', type=types.existing_built_artifact)
def remove_distributed_artifact():
    pass


@arg("id", help="ID of the ProductMilestone to list distributed builds for.", type=types.existing_product_milestone)
@arg("-p", "--page-size", help="Limit the amount of distributed builds returned", type=int)
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_distributed_builds(id, page_size=200, page_index=0, sort='', q=''):
    data = list_distributed_builds_raw(id, page_size, page_index, sort, q)
    if data:
        return utils.format_json_list(data)

def list_distributed_builds_raw(id, page_size=200, page_index=0, sort="", q=""):
    response = utils.checked_api_call(pnc_api.product_milestones, 'get_distributed_builds', id=id, page_size=page_size, page_index=page_index, sort=sort, q=q)
    if response:
        return response.content
