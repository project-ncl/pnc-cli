from argh import arg
from six import iteritems

import utils
import swagger_client
from swagger_client.apis.productversions_api import ProductversionsApi
from swagger_client.apis.productreleases_api import ProductreleasesApi


productversions_api = ProductversionsApi(utils.get_api_client())
releases_api = ProductreleasesApi(utils.get_api_client())


def create_product_release_object(**kwargs):
    created_release = swagger_client.ProductReleaseRest()
    for key, value in iteritems(kwargs):
        setattr(created_release, key, value)
    return created_release


def list_product_releases():
    """
    List all ProductReleases
    """
    response = utils.checked_api_call(releases_api, 'get_all')
    if response:
        return response.content

# no more than one release per milestone
# need product version id (version is not enough)
# version is created by appending product_version.<new info>


@arg("version", help="Version of the release. Appended to the Product Version.")
@arg("release_date", help="Date of the release. Format: yyyy-mm-dd")
@arg("download_url", help="URL where deliverables are located.")
@arg("product_version_id",
     help="ID of the product version this release is associated with.")
@arg("product_milestone_id", help="Milestone which is the basis of this release")
@arg("support_level", help="Level of support committed to for this release. Possible values: 'UNRELEASED', 'EARLYACCESS', 'SUPPORTED', 'EXTENDED_SUPPORT', 'EOL'")
def create_release(**kwargs):
    version = kwargs.get('version')
    if not utils.is_valid_version(version):
        print("Version must start with a number, followed by a dot and then a qualifier (e.g ER1).")
        return
    base_version = productversions_api.get_specific(
        id=kwargs.get('product_version_id')).content.version
    kwargs['version'] = base_version + '.' + kwargs.get('version')
    created_release = create_product_release_object(**kwargs)
    response = utils.checked_api_call(
        releases_api, 'create_new', body=created_release)
    if response:
        return response.content


@arg("id", help="Product version ID to retrieve releases for.")
def list_releases_for_version(id):
    """
    List all ProductReleases for a ProductVersion
    """
    response = utils.checked_api_call(
        releases_api, 'get_all_by_product_version_id', id=id)
    if response:
        return response.content


@arg("id", help="ID of the product version to retrieve.")
def get_release(id):
    """
    Get a specific ProductRelease
    """
    response = utils.checked_api_call(releases_api, 'get_specific', id=id)
    if response:
        return response.content


def _product_release_exists(search_id):
    """
    Check if a ProductVersion ID exists
    """
    existing_release_ids = [str(x.id) for x in releases_api.get_all().content]
    return str(search_id) in existing_release_ids


@arg("id", help="ID of the release to update.")
@arg("-v", "--version", help="Version of the release. Appended to the Product Version.")
@arg("-rd", "--release-date", help="Date of the release.")
@arg("-du", "--download-url", help="URL where deliverables are located.")
@arg("-pvid", "--product-version-id",
     help="ID of the product version this release is associated with.")
@arg("-msid", "--product-milestone-id",
     help="Milestone which is the basis of this release")
@arg("-sl", "--support-level", help="Level of support comitted to for this release.")
def update_release(id, **kwargs):
    """
    Update an existing ProductRelease with new information
    """
    if not _product_release_exists(id):
        print("No ProductRelease with ID {} exists.").format(id)
        return

    to_update = releases_api.get_specific(id=id).content
    for key, value in iteritems(kwargs):
        setattr(to_update, key, value)

    response = utils.checked_api_call(
        releases_api, 'update', id=id, body=to_update)
    if response:
        return response.content
