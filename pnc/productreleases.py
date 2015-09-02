import sys

from argh import arg

from client.ProductreleasesApi import ProductreleasesApi
import utils
import client


def create_product_release_object(**kwargs):
    created_release = client.models.ProductRelease.ProductRelease()
    for key, value in kwargs.iteritems():
        setattr(created_release, key ,value)
    return created_release

@arg("-a", "--attributes", help="Comma separated list of attributes to print.")
def list_product_releases(attributes=None):
    response = get_all()
    utils.print_json_result(sys._getframe().f_code.co_name,
                            response,
                            attributes,
                            client.models.ProductRelease.ProductRelease().attributeMap)

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
    created_release = create_product_release_object(version,
                                                    release_date,
                                                    download_url,
                                                    product_version_id,
                                                    product_milestone_id,
                                                    support_level)
    response = create(created_release)
    utils.print_json_result(sys._getframe().f_code.co_name,
                            response)

@arg("id", help="Product version ID to retrieve releases for.")
def list_releases_for_version(id):
    response = get_all_by_product_version_id(id)
    utils.print_json_result(sys._getframe().f_code.co_name, response)

def list_release_support_levels():
    response = get_all_support_level()
    utils.print_json_result(sys._getframe().f_code.co_name, response)

@arg("id", help="Product version to retrieve.")
def get_release(id):
    response = get_specific(id)
    utils.print_json_result(sys._getframe().f_code.co_name, response)

@arg("id", help="ID of the release to update.")
@arg("-v", "--version", help="Version of the release. Appended to the Product Version.")
@arg("-rd", "--release-date", help="Date of the release.")
@arg("-du", "--download-url", help="URL where deliverables are located.")
@arg("-pvid", "--product-version-id", help="ID of the product version this release is associated with.")
@arg("-msid","--product-milestone-id", help="Milestone which is the basis of this release")
@arg("-sl", "--support-level", help="Level of support comitted to for this release.")
def update_release(id, version=None, release_date=None, download_url=None, product_version_id=None, product_milestone_id=None, support_level=None):
    #get the existing product_release
    existing = get_specific(id)
    if not existing.ok:
        print("No release with ID {0} exists.").format(id)
        return

    existing_release = existing.json()
    if version: existing_release['version'] = version
    if release_date: existing_release['releaseDate'] = release_date
    if download_url: existing_release['downloadUrl'] = download_url
    if product_version_id: existing_release['productVersionId'] = product_version_id
    if product_milestone_id: existing_release['productMilestoneId'] = product_milestone_id
    if support_level: existing_release['supportLevel'] = support_level

    # create the new product_release from the modified dict
    release_obj = create_product_release_object(existing_release)
    response = update(id, release_obj)
    if not response.ok:
        utils.print_error(sys._getframe().f_code.co_name, response)
        return
    print("Successfully updated release with ID {0}.").format(id)


def get_all():
    return ProductreleasesApi(utils.get_api_client()).getAll()

def create(product_release):
    return ProductreleasesApi(utils.get_api_client()).createNew(body=product_release)

def get_all_by_product_version_id(version_id):
    return ProductreleasesApi(utils.get_api_client()).getAllByProductVersionId(versionId=version_id)

def get_all_support_level():
    return ProductreleasesApi(utils.get_api_client()).getAllSupportLevel()

def get_specific(release_id):
    return ProductreleasesApi(utils.get_api_client()).getSpecific(id=release_id)

def update(release_id, updated_release):
    return ProductreleasesApi(utils.get_api_client()).update(id=release_id, body=updated_release)


