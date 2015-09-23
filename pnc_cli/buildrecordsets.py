__author__ = 'thauser'
from pnc_cli import utils
from pnc_cli.swagger_client.apis import BuildrecordsetsApi

brs_api = BuildrecordsetsApi(utils.get_api_client())


def list_build_record_sets():
    """
    List all BuildRecordSets
    """
    response = utils.checked_api_call(brs_api, 'get_all')
    if response:
        return response.content


def get_build_record_set(id):
    """
    Get a specific BuildRecordSet by ID
    """
    response = utils.checked_api_call(brs_api, 'get_specific', id=id)
    if response:
        return response.content


def create_build_record_set():
    """
    Create a new BuildRecordSet (incomplete)
    """
    response = utils.checked_api_call(brs_api, 'create_new')
    if response:
        return response.content


def list_sets_for_build_record(id):
    """
    List all BuildRecordSets of a given BuildRecord
    """
    response = utils.checked_api_call(
        brs_api, 'get_all_for_build_record', record_id=id)
    if response:
        return response.content


def list_build_record_sets_for_milestone(id):
    """
    List all BuildRecordSets for a given ProductMilestone
    """
    response = utils.checked_api_call(
        brs_api, 'get_all_for_product_milestone', version_id=id)
    if response:
        return response.content


def delete_build_record_set(id):
    """
    Delete a specific BuildRecordSet by ID
    """
    response = utils.checked_api_call(brs_api, 'delete_specific', id=id)
    if response:
        return response.content


def update_build_record_set(id):
    """
    Replace a specific BuildRecordSet with a new one.
    """
    response = utils.checked_api_call(brs_api, 'update', id=id)
    if response:
        return response.content
