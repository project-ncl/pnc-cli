from argh import arg
from six import iteritems

import pnc_cli.cli_types as types
import pnc_cli.utils as utils
from pnc_cli import productmilestones
from pnc_cli.swagger_client import ProductReleaseRest
from pnc_cli.swagger_client import ProductreleasesApi
from pnc_cli.swagger_client import ProductversionsApi
import pnc_cli.user_config as uc

productversions_api = ProductversionsApi(uc.user.get_api_client())
releases_api = ProductreleasesApi(uc.user.get_api_client())


def create_product_release_object(**kwargs):
    created_release = ProductReleaseRest()
    for key, value in iteritems(kwargs):
        setattr(created_release, key, value)
    return created_release


@arg("-p", "--page-size", help="Limit the amount of ProductReleases returned", type=int)
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_product_releases(page_size=200, page_index=0, sort="", q=""):
    """
    List all ProductReleases
    """
    response = utils.checked_api_call(releases_api, 'get_all', page_size=page_size, page_index=page_index, sort=sort, q=q)
    if response:
        return utils.format_json_list(response.content)


# no more than one release per milestone
# need ProductVersion id (version is not enough)
# version is created by appending product_version.<new info>


@arg("version", help="Version of the release. Appended to the ProductVersion's version.",
     type=types.valid_version_create)
@arg("release_date", help="Date of the release. Format: yyyy-mm-dd", type=types.valid_date)
@arg("download_url", help="URL where deliverable(s) are located.", type=types.valid_url)
@arg("product_milestone_id", help="ProductMilestone which is the basis of this release",
     type=types.existing_product_milestone)
@arg("issue_tracker_url", help="Link to the Issue tracker for this ProductRelease", type=types.valid_url)
@arg("support_level",
     help="Level of support committed to for this release. Possible values: 'UNRELEASED', 'EARLYACCESS', 'SUPPORTED', 'EXTENDED_SUPPORT', 'EOL'",
     choices=['UNRELEASED', 'EARLYACCESS', 'SUPPORTED', 'EXTENDED_SUPPORT', 'EOL'])
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
    # gotta find a way to avoid this situation
    product_version = str(productmilestones.get_product_version_from_milestone(kwargs.get('product_milestone_id')))
    base_version = productversions_api.get_specific(
        id=product_version).content.version
    kwargs['version'] = base_version + '.' + kwargs.get('version')
    created_release = create_product_release_object(**kwargs)
    response = utils.checked_api_call(
        releases_api, 'create_new', body=created_release)
    if response:
        return utils.format_json(response.content)


@arg("id", help="ProductVersion ID to retrieve releases for.", type=types.existing_product_version)
def list_releases_for_version(id):
    """
    List all ProductReleases for a ProductVersion
    """
    response = utils.checked_api_call(
        releases_api, 'get_all_by_product_version_id', version_id=id)
    if response:
        return utils.format_json_list(response.content)


@arg("id", help="ID of the ProductRelease to retrieve.", type=types.existing_product_release)
def get_release(id):
    """
    Retrieve a specific ProductRelease
    """
    response = utils.checked_api_call(releases_api, 'get_specific', id=id)
    if response:
        return utils.format_json(response.content)


@arg("id", help="ID of the release to update.", type=types.existing_product_release)
@arg("-v", "--version", help="Version of the release. Appended to the ProductVersion.", type=types.valid_version_update)
@arg("-rd", "--release-date", help="Date of the release.", type=types.valid_date)
@arg("-du", "--download-url", help="URL where deliverable(s) are located.", type=types.valid_url)
@arg("-msid", "--product-milestone-id",
     help="ProductMilestone which is the basis of this release", type=types.existing_product_milestone)
@arg("-sl", "--support-level", help="Level of support committed to for this release.",
     choices=['UNRELEASED', 'EARLYACCESS', 'SUPPORTED', 'EXTENDED_SUPPORT', 'EOL'])
def update_release(id, **kwargs):
    """
    Update an existing ProductRelease with new information
    """
    to_update = utils.checked_api_call(releases_api, 'get_specific', id=id).content
    for key, value in iteritems(kwargs):
        if value is not None:
            setattr(to_update, key, value)

    response = utils.checked_api_call(
        releases_api, 'update', id=id, body=to_update)
    if response:
        return utils.format_json(response.content)
