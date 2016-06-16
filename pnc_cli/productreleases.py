import argparse

from argh import arg
from six import iteritems

from pnc_cli import utils
from pnc_cli.swagger_client import ProductReleaseRest
from pnc_cli.swagger_client import ProductversionsApi
from pnc_cli.swagger_client import ProductreleasesApi
from pnc_cli import productmilestones
from pnc_cli import productversions

productversions_api = ProductversionsApi(utils.get_api_client())
releases_api = ProductreleasesApi(utils.get_api_client())


def existing_product_release(id_input):
    utils.valid_id(id_input)
    if not _product_release_exists(id_input):
        raise argparse.ArgumentTypeError("no ProductRelease with ID {} exists.".format(id_input))
    return id_input

def _product_release_exists(search_id):
    """
    Check if a Product release with the given id exists
    """
    response = utils.checked_api_call(releases_api, 'get_specific', id=search_id)
    return response is not None


def _valid_support_type(supportTypeInput):
    VALID_TYPES=["UNRELEASED", "EARLYACCESS", "SUPPORTED", "EXTENDED_SUPPORT", "EOL"]
    supportCaps = supportTypeInput.upper()
    if supportCaps not in VALID_TYPES:
        raise argparse.ArgumentTypeError("Invalid support level type")
    return supportCaps


def _valid_version_for_update(version):
    if not utils.is_valid_version(version, '^\d+\.\d+\.\d+\.\w+$'):
        raise argparse.ArgumentTypeError("The version should consist of three numeric parts and one alphanumeric qualifier each separated by a dot.")
    return version


def _valid_version_for_create(version):
    if not utils.is_valid_version(version, '^\d+\.\w+$'):
        raise argparse.ArgumentTypeError("Version must start with a number, followed by a dot and then a qualifier (e.g ER1).")
    return version


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


@arg("version", help="Version of the release. Appended to the ProductVersion's version.", type=_valid_version_for_create)
@arg("release_date", help="Date of the release. Format: yyyy-mm-dd", type=utils.valid_date)
@arg("download_url", help="URL where deliverable(s) are located.", type=utils.valid_url)
@arg("product_milestone_id", help="ProductMilestone which is the basis of this release", type=productmilestones.existing_product_milestone)
@arg("issue_tracker_url", help="Link to the Issue tracker for this ProductRelease", type=utils.valid_url)
@arg("support_level",
     help="Level of support committed to for this release. Possible values: 'UNRELEASED', 'EARLYACCESS', 'SUPPORTED', 'EXTENDED_SUPPORT', 'EOL'",
     type=_valid_support_type)
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
    product_version = str(productmilestones.get_product_version_from_milestone(kwargs.get('product_milestone_id')))
    base_version = productversions_api.get_specific(
        id=product_version).content.version
    kwargs['version'] = base_version + '.' + kwargs.get('version')
    created_release = create_product_release_object(**kwargs)
    response = utils.checked_api_call(
        releases_api, 'create_new', body=created_release)
    if response:
        return response.content


@arg("id", help="ProductVersion ID to retrieve releases for.", type=productversions.existing_product_version)
def list_releases_for_version(id):
    """
    List all ProductReleases for a ProductVersion
    """
    response = utils.checked_api_call(
        releases_api, 'get_all_by_product_version_id', version_id=id)
    if response:
        return response.content


@arg("id", help="ID of the ProductRelease to retrieve.", type=existing_product_release)
def get_release(id):
    """
    Retrieve a specific ProductRelease
    """
    response = utils.checked_api_call(releases_api, 'get_specific', id=id)
    if response:
        return response.content


@arg("id", help="ID of the release to update.", type=existing_product_release)
@arg("-v", "--version", help="Version of the release. Appended to the ProductVersion.", type=_valid_version_for_update)
@arg("-rd", "--release-date", help="Date of the release.", type=utils.valid_date)
@arg("-du", "--download-url", help="URL where deliverable(s) are located.", type=utils.valid_url)
@arg("-msid", "--product-milestone-id",
     help="ProductMilestone which is the basis of this release", type=productmilestones.existing_product_milestone)
@arg("-sl", "--support-level", help="Level of support committed to for this release.", type=_valid_support_type)
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
        return response.content
