from argh import arg
from six import iteritems

import logging
from pnc_cli import utils
from pnc_cli.swagger_client import ProductReleaseRest
from pnc_cli.swagger_client import ProductversionsApi
from pnc_cli.swagger_client import ProductreleasesApi


productversions_api = ProductversionsApi(utils.get_api_client())
releases_api = ProductreleasesApi(utils.get_api_client())


def create_product_release_object(**kwargs):
    created_release = ProductReleaseRest()
    for key, value in iteritems(kwargs):
        setattr(created_release, key, value)
    return created_release


@arg("-p", "--page-size", help="Limit the amount of ProductReleases returned")
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_product_releases(page_size=200, sort="", q=""):
    """
    List all ProductReleases
    """
    response = utils.checked_api_call(releases_api, 'get_all', page_size=page_size, sort=sort, q=q)
    if response:
        return response.content


# no more than one release per milestone
# need ProductVersion id (version is not enough)
# version is created by appending product_version.<new info>


@arg("version", help="Version of the release. Appended to the ProductVersion's version.")
@arg("release_date", help="Date of the release. Format: yyyy-mm-dd")
@arg("download_url", help="URL where deliverable(s) are located.")
@arg("product_version_id",
     help="ID of the ProductVersion this release is associated with.")
@arg("product_milestone_id", help="ProductMilestone which is the basis of this release")
@arg("issue_tracker_url", help="Link to the Issue tracker for this ProductRelease")
@arg("support_level",
     help="Level of support committed to for this release. Possible values: 'UNRELEASED', 'EARLYACCESS', 'SUPPORTED', 'EXTENDED_SUPPORT', 'EOL'")
def create_release(**kwargs):
    """
    Create a new ProductRelease.
    A ProductRelease represents a build / set of builds that is ready for release to the public.
    Each ProductRelease is associated with exactly one ProductMilestone and exactly one ProductVersion.

    Example:
    ProductVersion: 1.0
    ProductMilestone: 1.0.0.CR2
    ProductRelease: 1.0.0.GA
    """
    version = kwargs.get('version')
    if not utils.is_valid_version(version):
        logging.error("Version must start with a number, followed by a dot and then a qualifier (e.g ER1).")
        return
    base_version = productversions_api.get_specific(
        id=kwargs.get('product_version_id')).content.version
    kwargs['version'] = base_version + '.' + kwargs.get('version')
    created_release = create_product_release_object(**kwargs)
    response = utils.checked_api_call(
        releases_api, 'create_new', body=created_release)
    if response:
        return response.content


@arg("id", help="ProductVersion ID to retrieve releases for.")
def list_releases_for_version(id):
    """
    List all ProductReleases for a ProductVersion
    """
    response = utils.checked_api_call(
        releases_api, 'get_all_by_product_version_id', version_id=id)
    if response:
        return response.content


@arg("id", help="ID of the ProductVersion to retrieve.")
def get_release(id):
    """
    Retrieve a specific ProductRelease
    """
    response = utils.checked_api_call(releases_api, 'get_specific', id=id)
    if response:
        return response.content


def _product_release_exists(search_id):
    """
    Check if a Product release with the given id exists
    """
    response = utils.checked_api_call(releases_api, 'get_specific', id=search_id)
    return response is not None


@arg("id", help="ID of the release to update.")
@arg("-v", "--version", help="Version of the release. Appended to the ProductVersion.")
@arg("-rd", "--release-date", help="Date of the release.")
@arg("-du", "--download-url", help="URL where deliverable(s) are located.")
@arg("-pvid", "--product-version-id",
     help="ID of the ProductVersion     this release is associated with.")
@arg("-msid", "--product-milestone-id",
     help="ProductMilestone which is the basis of this release")
@arg("-sl", "--support-level", help="Level of support committed to for this release.")
def update_release(id, **kwargs):
    """
    Update an existing ProductRelease with new information
    """
    if not _product_release_exists(id):
        logging.error("No ProductRelease with ID {} exists.".format(id))
        return

    to_update = releases_api.get_specific(id=id).content
    for key, value in iteritems(kwargs):
        setattr(to_update, key, value)

    response = utils.checked_api_call(
        releases_api, 'update', id=id, body=to_update)
    if response:
        return response.content
