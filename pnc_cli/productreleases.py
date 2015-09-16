import utils
import swagger_client
from argh import arg
from swagger_client.apis.productversions_api import ProductversionsApi
from swagger_client.apis.productreleases_api import ProductreleasesApi
from pprint import pprint

productversions_api = ProductversionsApi(utils.get_api_client())
releases_api = ProductreleasesApi(utils.get_api_client())

def create_product_release_object(**kwargs):
    created_release = swagger_client.ProductReleaseRest()
    for key, value in kwargs.iteritems():
        setattr(created_release, key ,value)
    return created_release


def list_product_releases():
    releases_api.get_all(callback=callback_function)

# no more than one release per milestone
# need product version id (version is not enough)
# version is created by appending product_version.<new info>
@arg("version", help="Version of the release. Appended to the Product Version.")
@arg("release_date", help="Date of the release. Format: yyyy-mm-dd")
@arg("download_url", help="URL where deliverables are located.")
@arg("product_version_id", help="ID of the product version this release is associated with.")
@arg("product_milestone_id", help="Milestone which is the basis of this release")
@arg("support_level", help="Level of support committed to for this release. Possible values: 'UNRELEASED', 'EARLYACCESS', 'SUPPORTED', 'EXTENDED_SUPPORT', 'EOL'")
def create_release(**kwargs):
    version = kwargs.get('version')
    if not utils.is_valid_version(version):
        print("Version must start with a number, followed by a dot and then a qualifier (e.g ER1).")
        return
    base_version = productversions_api.get_specific(id=kwargs.get('product_version_id')).content.version
    kwargs['version'] = base_version + '.' + kwargs.get('version')
    created_release = create_product_release_object(**kwargs)
    releases_api.create_new(body=created_release, callback=callback_function)


@arg("id", help="Product version ID to retrieve releases for.")
def list_releases_for_version(id):
    """
    List all releases for a product version
    :param id: id of the product version
    :return: list of associated releases
    """
    releases_api.get_all_by_product_version_id(id=id,callback=callback_function)

@arg("id", help="ID of the product version to retrieve.")
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
    #get the existing product_release
    to_update = releases_api.get_specific(id=id)
    for key, value in kwargs.iteritems():
        setattr(to_update, key, value)
    releases_api.update(id=id, body=to_update, callback=callback_function)

def callback_function(response):
    if response:
        pprint(response.content)
