from pnc_cli import utils
from pnc_cli.swagger_client.apis.buildrecords_api import BuildrecordsApi
from test import testutils

builds_api = BuildrecordsApi(utils.get_api_client())


def test_get_all_invalid_param():
    testutils.assert_raises_typeerror(builds_api, 'get_all')


def test_get_all():
    records = builds_api.get_all().content
    assert records is not None


def test_get_specific_no_id():
    testutils.assert_raises_valueerror(builds_api, 'get_specific', id=None)


def test_get_specific_invalid_param():
    testutils.assert_raises_typeerror(builds_api, 'get_specific', id=1)


def test_get_specific():
    record = builds_api.get_specific(id=1).content
    assert record is not None


def test_get_all_for_build_configuration_no_configuration_id():
    testutils.assert_raises_valueerror(builds_api, 'get_all_for_build_configuration', configuration_id=None)


def test_get_all_for_build_configuration_invalid_param():
    testutils.assert_raises_typeerror(builds_api, 'get_all_for_build_configuration', configuration_id=1)


def test_get_all_for_build_configuration():
    records = builds_api.get_all_for_build_configuration(configuration_id=1).content
    assert records is not None


def test_get_all_for_project_no_project_id():
    testutils.assert_raises_valueerror(builds_api, 'get_all_for_project', project_id=None)


def test_get_all_for_project_invalid_param():
    testutils.assert_raises_typeerror(builds_api, 'get_all_for_project', project_id=1)


def test_get_all_for_project():
    records = builds_api.get_all_for_project(project_id=1).content
    assert records is not None


def test_get_artifacts_no_id():
    testutils.assert_raises_valueerror(builds_api, 'get_artifacts', id=None)


def test_get_artifacts_invalid_param():
    testutils.assert_raises_typeerror(builds_api, 'get_artifacts', id=1)


def test_get_artifacts():
    artifacts = builds_api.get_artifacts(id=1).content
    assert artifacts is not None


def test_get_logs_no_id():
    testutils.assert_raises_valueerror(builds_api, 'get_logs', id=None)


def test_get_logs_invalid_param():
    testutils.assert_raises_typeerror(builds_api, 'get_logs', id=1)


def test_get_logs():
    log = builds_api.get_logs(id=1)
    assert log is not None


def test_get_build_configuration_audited():
    testutils.assert_raises_valueerror(builds_api, 'get_build_configuration_audited', id=None)


def test_get_build_configuration_audited_invalid_param():
    testutils.assert_raises_typeerror(builds_api, 'get_build_configuration_audited', id=1)


def test_get_build_configuration_audited():
    audited = builds_api.get_build_configuration_audited(id=1).content
    assert audited is not None


def test_get_completed_or_runnning_no_id():
    testutils.assert_raises_valueerror(builds_api, 'get_completed_or_runnning', id=None)


def test_get_completed_or_runnning_invalid_param():
    testutils.assert_raises_typeerror(builds_api, 'get_completed_or_runnning', id=1)


def test_get_completed_or_runnning():
    response = builds_api.get_completed_or_runnning(id=1)
    assert response is not None

