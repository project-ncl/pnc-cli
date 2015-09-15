from pprint import pprint

__author__ = 'thauser'
from argh import arg
import utils
from swagger_client.apis import BuildconfigurationsetsApi
from swagger_client.apis import BuildconfigsetrecordsApi

sets_api = BuildconfigurationsetsApi(utils.get_api_client())
bcsr_api = BuildconfigsetrecordsApi(utils.get_api_client())

def callback_function(response):
    if response:
        pprint(response.content)

def _config_set_record_exists(id):
    return id in [str(x.id) for x in bcsr_api.get_all().content]

def list_build_config_set_records():
    bcsr_api.get_all(callback=callback_function)

@arg("id", help="ID of build configuration set record to retrieve.")
def get_build_config_set_record(id):
    if not _config_set_record_exists(id):
        print("A build configuration set record with ID {} does not exist.").format(id)
        return
    bcsr_api.get_specific(id=id, callback=callback_function)

@arg("id", help="ID of build configuration set record to retrieve build records from.")
def get_records_for_build_config_set(id):
    if not id in [str(x.id) for x in sets_api.get_all().content]:
        print("A build configuration set with ID {} does not exist.").format(id)
        return
    bcsr_api.get_build_records(id=id, callback=callback_function)