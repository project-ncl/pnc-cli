import sys

from argh import arg

import swagger_client
from swagger_client.apis.productmilestones_api import ProductmilestonesApi
import utils


def create_milestone_object(**kwargs):
    created_milestone = swagger_client.models.product_milestone.ProductMilestone()
    for key, value in kwargs.iteritems():
        setattr(created_milestone, key, value)
    return created_milestone

@arg("-a", "--attributes", help="Comma separated list of attributes to print.")
def list_product_milestones(attributes=None):
    response = get_all()
    utils.print_json_result(sys._getframe().f_code.co_name,
                            response,
                            attributes,
                            swagger_client.models.product_milestone.ProductMilestone().attribute_map)

@arg("id", help="ID of the milestone to retrieve.")
@arg("-a", "--attributes", help="Comma separated list of attributes to print.")
def get_product_milestone(id, attributes=None):
    response = get_specific(id)
    utils.print_json_result(sys._getframe().f_code.co_name,
                            response,
                            attributes,
                            swagger_client.models.product_milestone.ProductMilestone().attribute_map)

def create_product_milestone(version, start_date, planned_release_date):
    created_milestone = create_milestone_object(version=version, startingDate=start_date, plannedReleaseDate=planned_release_date)
    response = create(created_milestone)
    utils.print_json_result(sys._getframe().f_code.co_name,response)

@arg("id", help="Product version ID to retrieve milestones for.")
def list_milestones_for_version(id):
    response = get_all_by_product_version_id(id)
    utils.print_json_result(sys._getframe().f_code.co_name, response)

@arg("id", help="Product milestone ID to retrieve.")
def get_milestone(id):
    response = get_specific(id)
    utils.print_json_result(sys._getframe().f_code.co_name, response)

@arg("id", help="Product milestone ID to update.")
def update_milestone(id, version=None, start_date=None,release_date=None):
    existing = get_specific(id)
    if not existing.ok:
        print("No milestone with ID {0} exists.").format(id)
        return

    existing_milestone = existing.json()

    if version: existing_milestone['version'] = version
    if version: existing_milestone['startingDate'] = start_date
    if version: existing_milestone['plannedReleaseDate'] = release_date

    milestone_obj = create_milestone_object(existing_milestone)
    response = update(id, milestone_obj)
    if not response.ok:
        utils.print_error(sys._getframe().f_code.co_name, response)
        return
    print("Successfully updated milestone with ID {0}.").format(id)

def get_all():
    return ProductmilestonesApi(utils.get_api_client()).getAll()

def create(milestone):
    return ProductmilestonesApi(utils.get_api_client()).createNew(body=milestone)

def get_all_by_product_version_id(version_id):
    return ProductmilestonesApi(utils.get_api_client()).getAllByProductVersionId(versionId=version_id)

def get_specific(milestone_id):
    return ProductmilestonesApi(utils.get_api_client()).getSpecific(id=milestone_id)

def update(milestone_id, milestone):
    return ProductmilestonesApi(utils.get_api_client()).update(id=milestone_id, body=milestone)


