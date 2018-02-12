from argh import arg
from argh import named

import pnc_cli.common as common
import pnc_cli.cli_types as types
import pnc_cli.utils as utils
from pnc_cli import swagger_client
from pnc_cli.swagger_client import BuildrecordpushApi
from pnc_cli.swagger_client import BuildrecordsApi
from pnc_cli.swagger_client import BuildconfigurationsApi
from pnc_cli.swagger_client import ProjectsApi
import pnc_cli.user_config as uc

push_api = BuildrecordpushApi(uc.user.get_api_client())
records_api = BuildrecordsApi(uc.user.get_api_client())
configs_api = BuildconfigurationsApi(uc.user.get_api_client())
projects_api = ProjectsApi(uc.user.get_api_client())

namespace_kwargs = {'title': 'Brew push commands',
                    'description': 'Commands related to pushing to Brew'}

@named("build")
@arg("id", help="Build record ID to push to Brew.", type=types.existing_build_record)
@arg("tag_prefix", help="Brew tag to which push the build. It will have -candidate suffix.", type=str)
def push_build(id, tag_prefix):
    """
    Push build to Brew
    """
    req = swagger_client.BuildRecordPushRequestRest()
    req.tag_prefix = tag_prefix
    req.build_record_id = id
    response = utils.checked_api_call(push_api, 'push', body=req)
    if response:
        return utils.format_dict(response)


@named("build-set")
@arg("id", help="Build set record ID to push to Brew.", type=types.existing_build_record)
@arg("tag_prefix", help="Brew tag to which push the builds. It will have -candidate suffix.", type=str)
def push_build_set(id, tag_prefix):
    """
    Push build set to Brew
    """
    req = swagger_client.BuildConfigSetRecordPushRequestRest()
    req.tag_prefix = tag_prefix
    req.build_config_set_record_id = id
    response = utils.checked_api_call(push_api, 'push_record_set', body=req)
    if response:
        return utils.format_dict(response)


@named("status")
@arg("id", help="Build record ID to get the Brew push status.", type=types.existing_build_record)
def push_build_status(id):
    """
    Get status of Brew push.
    """
    response = utils.checked_api_call(push_api, 'status', build_record_id=id)
    if response:
        return utils.format_json(response)

