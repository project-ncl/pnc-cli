__author__ = 'thauser'
from argh import arg
from six import iteritems

import logging
from pnc_cli import swagger_client
from pnc_cli import utils

from pnc_cli.swagger_client import BuildsApi

builds_api = BuildsApi()

@arg("-p", "--page-size", help="Limit the amount of builds returned")
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_builds(page_size=200, page_index=0, sort="", q=""):
    """
    List all builds
    :param page_size: number of builds returned per query
    :param sort: RSQL sorting query
    :param q: RSQL query
    :return:
    """
    response = utils.checked_api_call(builds_api, 'get_all', page_size=page_size, page_index=page_index, sort=sort, q=q)
    if response:
        return response.content
