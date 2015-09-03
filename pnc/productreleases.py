import utils
import swagger_client
from argh import arg
from swagger_client.apis.productreleases_api import ProductreleasesApi
from pprint import pprint

releases_api = ProductreleasesApi(utils.get_api_client())

def create_product_release_object(**kwargs):
    created_release = swagger_client.models.product_release.ProductRelease()
    for key, value in kwargs.iteritems():
        setattr(created_release, key ,value)
    return created_release


def list_product_releases(attributes=None):
    """
    List all product releases
    :param attributes:
    :return:
    """
    releases_api.get_all(callback=callback_function)

# no more than one release per milestone
# need product version id (version is not enough)
# version is created by appending product_version.<new info>

@arg("version", help="Version of the release. Appended to the Product Version.")
@arg("release-date", help="Date of the release.")
@arg("download-url", help="URL where deliverables are located.")
@arg("product-version-id", help="ID of the product version this release is associated with.")
@arg("product-milestone-id", help="Milestone which is the basis of this release")
@arg("support-level", help="Level of support comitted to for this release.")
def create_release(version, release_date, download_url, product_version_id, product_milestone_id, support_level):
    """
    Create a new product release
    :param version: version for the release (appended to associated product version)
    :param release_date: release date for the release (duh!)
    :param download_url: URL where built artifacts will be available
    :param product_version_id: associated product version id
    :param product_milestone_id: associated milestone id
    :param support_level: support level for this release
    :return: Resulting release
    """
    # TODO: better way to use dicts here maybe?
    created_release = create_product_release_object(version=version,
                                                    release_date=release_date,
                                                    download_url=download_url,
                                                    product_version_id=product_version_id,
                                                    product_milestone_id=product_milestone_id,
                                                    support_level=support_level)
    releases_api.create(body=created_release, callback=callback_function)


@arg("id", help="Product version ID to retrieve releases for.")
def list_releases_for_version(id):
    """
    List all releases for a product version
    :param id: id of the product version
    :return: list of associated releases
    """
    releases_api.get_all_by_product_version_id(id=id,callback=callback_function)


def list_release_support_levels():
    """
    List all possible support levels.
    :return:
    """
    releases_api.get_all_support_level(callback=callback_function)

@arg("id", help="Product version to retrieve.")
def get_release(id):
    """
    Get a specific product release.
    :param id: id of the product release
    :return:
    """
    releases_api.get_specific(id=id, callback=callback_function)

@arg("id", help="ID of the release to update.")
@arg("-v", "--version", help="Version of the release. Appended to the Product Version.")
@arg("-rd", "--release-date", help="Date of the release.")
@arg("-du", "--download-url", help="URL where deliverables are located.")
@arg("-pvid", "--product-version-id", help="ID of the product version this release is associated with.")
@arg("-msid","--product-milestone-id", help="Milestone which is the basis of this release")
@arg("-sl", "--support-level", help="Level of support comitted to for this release.")
def update_release(id, **kwargs):
    """
    Replace the product release with ID id with new information
    :param id: id of the release to update
    :param version: new version for release
    :param release_date: new release date
    :param download_url: new download url
    :param product_version_id: new product version id for the release
    :param product_milestone_id: new milestone id for the release
    :param support_level: new support level for the release
    :return: errors upon failure
    """
    #get the existing product_release
    to_update = releases_api.get_specific(id=id)
    for key, value in kwargs.iteritems():
        setattr(to_update, key, value)
    releases_api.update(id=id, body=to_update, callback=callback_function)

def callback_function(response):
    if response:
        pprint(response)
