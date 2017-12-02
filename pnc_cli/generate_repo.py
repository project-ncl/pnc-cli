import logging
import sys

from argh import arg

from pnc_cli.swagger_client import ProductversionsApi
from pnc_cli.swagger_client import ProductmilestonesApi
from pnc_cli.swagger_client import BuildrecordsApi
import pnc_cli.user_config as uc

productversions_api = ProductversionsApi(uc.user.get_api_client())
productmilestones_api = ProductmilestonesApi(uc.user.get_api_client())
buildrecords_api = BuildrecordsApi(uc.user.get_api_client())

@arg('-p', '--product_name', help='Product name')
@arg('-v', '--product_version', help='Product version')
@arg('-m', '--product_milestone', help='Product milestone')
def generate_repo_list(product_name=None, product_version=None, product_milestone=None):
    """
    Generates list of artifacts for offline repository.
    """
    if not validate_input_parameters(product_name, product_version, product_milestone):
        sys.exit(1)
    product_version = productversions_api.get_all(q="version=='"+ product_version + "';product.name=='"+product_name+"'")
    if not product_version.content:
        logging.error('Specified product version not found.')
        sys.exit(1)
    product_version_id = product_version.content[0].id
    milestone = productmilestones_api.get_all(q="version=='"+ product_milestone + "';productVersion.id=='"+str(product_version_id)+"'")
    if not milestone.content:
        logging.error('Specified milestone not found.')
        sys.exit(1)
    milestone_id = milestone.content[0].id
    builds = get_all_successful_builds(milestone_id)
    if not builds:
        logging.warning('No builds performed in the milestone.')
        return
    for build in builds:
        built_artifacts = get_all_artifacts(build.id)
        for artifact in built_artifacts:
            print(artifact.identifier)

def get_all_artifacts(build_id):
    artifacts = []
    page = 0
    ba = buildrecords_api.get_built_artifacts(build_id, page_index=page, page_size=50)
    if not ba.content:
        return []
    pages = ba.total_pages
    artifacts.extend(ba.content)
    for page in range(1,pages):
        ba = buildrecords_api.get_built_artifacts(build_id, page_index=page, page_size=50)
        artifacts.extend(ba.content)
    return artifacts

def get_all_successful_builds(milestone_id):
    builds = []
    page = 0
    pb = productmilestones_api.get_performed_builds(milestone_id, page_index=page, page_size=2, q="status=='SUCCESS'")
    if not pb.content:
        return []
    pages = pb.total_pages
    builds.extend(pb.content)
    for page in range(1,pages):
        pb = productmilestones_api.get_performed_builds(milestone_id, page_index=page, page_size=2, q="status=='SUCCESS'")
        builds.extend(pb.content)
    return builds

def validate_input_parameters(product_name, product_version, product_milestone):
    valid = True
    if product_name is None:
        logging.error('Product Name --product-name is not specified.')
        valid = False

    if product_version is None:
        logging.error('Product Version --product-version is not specified.')
        valid = False

    if product_milestone is None:
        logging.error('Product Milestone --product-milestone is not specified.')
        valid = False

    return valid
