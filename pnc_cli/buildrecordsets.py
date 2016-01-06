from argh import arg
from six import iteritems

import logging

__author__ = 'thauser'
from pnc_cli import utils
from pnc_cli.swagger_client import BuildrecordsetsApi
from pnc_cli.swagger_client import BuildRecordSetRest

brs_api = BuildrecordsetsApi(utils.get_api_client())


def create_buildrecordset_object(**kwargs):
    created = BuildRecordSetRest()
    for key, value in iteritems(kwargs):
        setattr(created, key, value)
    return created


def get_brs_id(id):
    if not str(id) in [str(x.id) for x in brs_api.get_all().content]:
        logging.error("No BuildRecordSet with ID {} exists.".format(id))
        return
    return id


@arg("-p", "--page-size", help="Limit the amount of BuildRecordSets returned")
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_build_record_sets(page_size=200, sort="", q=""):
    """
    List all BuildRecordSets
    """
    response = utils.checked_api_call(brs_api, 'get_all', page_size=page_size, sort=sort, q=q)
    if response:
        return response.content


def get_build_record_set(id):
    """
    Get a specific BuildRecordSet by ID
    """
    if not get_brs_id(id):
        return

    response = utils.checked_api_call(brs_api, 'get_specific', id=id)
    if response:
        return response.content


@arg('-di', '--distributed-in-product-milestone-id',
     help='ID of the ProductMilestone this BuildRecordSet was distributed in.')
@arg('-pi', '--performed-in-product-milestone-id',
     help='ID of the ProductMilestone this BuildRecordSet was performed in.')
@arg('-bri', '--build-record-ids', type=int, nargs='+', help='BuildRecords in this BuildRecordSet.')
# TODO check for existence of BuildRecords in -bri array
def create_build_record_set(**kwargs):
    """
    Create a new BuildRecordSet (incomplete). Cannot add ProductMilestone references
    """
    response = utils.checked_api_call(brs_api, 'create_new', body=create_buildrecordset_object(**kwargs))
    if response:
        return response.content


@arg('id', help='ID of the BuildRecord.')
@arg("-p", "--page-size", help="Limit the amount of BuildRecordSets returned")
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_sets_containing_build_record(id, page_size=200, sort="", q=""):
    """
    List all BuildRecordSets containing the given BuildRecord
    """
    response = utils.checked_api_call(
        brs_api, 'get_all_for_build_record', record_id=id, page_size=page_size, sort=sort, q=q)
    if response:
        return response.content


@arg("-p", "--page-size", help="Limit the amount of BuildRecordSets returned")
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
@arg('id', help='ID of the BuildRecord.')
def list_build_record_sets_for_milestone(id, page_size=200, sort="", q=""):
    """
    List all BuildRecordSets containing the given ProductMilestone
    """
    # TODO: check id for existence in productversions
    response = utils.checked_api_call(
        brs_api, 'get_all_for_product_milestone', version_id=id, page_size=page_size, sort=sort, q=q)
    if response:
        return response.content


@arg('id', help='ID of the BuildRecordSet.')
def delete_build_record_set(id):
    """
    Delete a specific BuildRecordSet by ID
    """
    if not get_brs_id(id):
        return
    response = utils.checked_api_call(brs_api, 'delete_specific', id=id)
    if response:
        return response.content


@arg('id', help='ID of the BuildRecordSet to update.')
@arg('-di', '--distributed-in-product-milestone-id',
     help='ID of the ProductMilestone this BuildRecordSet was distributed in.')
@arg('-pi', '--performed-in-product-milestone-id',
     help='ID of the ProductMilestone this BuildRecordSet was performed in.')
@arg('-bri', '--build-record-ids', type=int, nargs='+', help='BuildRecords in this BuildRecordSet.')
# TODO check for existence of BuildRecords in -bri array
def update_build_record_set(id, **kwargs):
    """
    Update a BuildRecordSet with new information.
    """
    if not get_brs_id(id):
        return

    to_update = brs_api.get_specific(id=id).content
    for key, value in iteritems(kwargs):
        setattr(to_update, key, value)

    response = utils.checked_api_call(brs_api, 'update', id=id, body=to_update)
    if response:
        return response.content
