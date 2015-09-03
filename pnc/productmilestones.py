import utils
import swagger_client
from swagger_client.apis.productmilestones_api import ProductmilestonesApi
from argh import arg
from pprint import pprint

milestones_api = ProductmilestonesApi(utils.get_api_client())

def create_milestone_object(**kwargs):
    created_milestone = swagger_client.models.product_milestone.ProductMilestone()
    for key, value in kwargs.iteritems():
        setattr(created_milestone, key, value)
    return created_milestone

def list_product_milestones():
    """
    List all product milestones
    :param attributes:
    :return:
    """
    milestones_api.get_all(callback=callback_function)

@arg("id", help="ID of the milestone to retrieve.")
def get_product_milestone(id):
     milestones_api.get_specific(id=id, callback=callback_function)

@arg("version", help="Version of the milestone.")
@arg("start_date", help="Planned starting date for the milestone.")
@arg("planned_release_date", help="Planned date for the milestone release.")
def create_product_milestone(version, start_date, planned_release_date):
    """
    Create a new product milestone.
    :param version: version for the milestone
    :param start_date: start date for the milestone
    :param planned_release_date: planned release date
    :return: Errors upon failure.
    """
    created_milestone = create_milestone_object(version=version, starting_date=start_date, planned_release_date=planned_release_date)
    milestones_api.create_new(body=created_milestone, callback=callback_function)

@arg("id", help="Product version ID to retrieve milestones for.")
def list_milestones_for_version(id):
    """
    List milestones for a specific product version
    :param id: ID of the product
    :return: List of product milestones associated with the given product
    """
    milestones_api.get_all_by_product_version_id(id=id,callback=callback_function)

@arg("id", help="Product milestone ID to retrieve.")
def get_milestone(id):
    milestones_api.get_specific(id=id, callback=callback_function)


@arg("id", help="Product milestone ID to update.")
@arg("version", help="New version for the milestone.")
@arg("start_date", help="New start date for the milestone.")
@arg("release_date", help="New release date for the milestone.")
def update_milestone(id, **kwargs):
    existing_milestone = milestones_api.get_specific(id)
    for key,value in kwargs.iteritems():
        setattr(existing_milestone, key, value)
    milestones_api.update(id=id, body=existing_milestone, callback=callback_function)


def callback_function(response):
    if response:
        pprint(response)


