from argh import arg
from argh import named

import pnc_cli.common as common
import pnc_cli.cli_types as types
import pnc_cli.utils as utils
from pnc_cli import swagger_client
from pnc_cli.pnc_api import pnc_api

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
    response = utils.checked_api_call(pnc_api.build_push, 'push', body=req)
    if response:
        return utils.format_json_list(response)


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
    response = utils.checked_api_call(pnc_api.build_push, 'push_record_set', body=req)
    if response:
        return utils.format_json_list(response)


@named("status")
@arg("id", help="Build record ID to get the Brew push status.", type=types.existing_build_record)
def push_build_status(id):
    """
    Get status of Brew push.
    """
    response = utils.checked_api_call(pnc_api.build_push, 'status', build_record_id=id)
    if response:
        return utils.format_json(response)

