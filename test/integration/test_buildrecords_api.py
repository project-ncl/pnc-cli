from pnc_cli import utils
from pnc_cli.swagger_client.apis.buildrecords_api import BuildrecordsApi
builds_api = BuildrecordsApi(utils.get_api_client())

def test_get_all():
    records = builds_api.get_all().content
    assert records is not None

def test_get_specific():
    record = builds_api.get_specific(id=1).content
    assert record is not None

def test_get_all_for_build_configuration():
    records = builds_api.get_all_for_build_configuration(configuration_id=1).content
    assert records is not None

def test_get_all_for_product():
    records = builds_api.get_all_for_project(project_id=1).content
    assert records is not None

def test_get_build_artifacts():
    artifacts = builds_api.get_artifacts(id=1).content
    assert artifacts is not None

def test_get_logs():
    log = builds_api.get_logs(id=1)
    assert log is not None

def test_get_audited_build_configuration():
    audited = builds_api.get_build_configuration_audited(id=1).content
    assert audited is not None
