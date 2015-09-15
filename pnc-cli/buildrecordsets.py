from pprint import pprint

__author__ = 'thauser'
import utils
from swagger_client.apis import BuildrecordsetsApi

brs_api = BuildrecordsetsApi(utils.get_api_client())

def list_build_record_sets():
    brs_api.get_all(callback=callback_function)

def get_build_record_set(id):
    brs_api.get_specific(id=id, callback=callback_function)

def create_build_record_set():
    brs_api.create_new(callback=callback_function)

def list_sets_for_build_record(id):
    brs_api.get_all_for_build_record(record_id=id,callback=callback_function)

def list_build_record_sets_for_milestone(id):
    brs_api.get_all_for_product_milestone(version_id=id, callback=callback_function)

def delete_build_record_set(id):
    brs_api.delete_specific(id=id, callback=callback_function)

def update_build_record_set(id):
    brs_api.update(id=id, callback=callback_function)

def callback_function(response):
    if response:
        pprint(response.content)