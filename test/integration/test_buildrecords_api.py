
import pytest

from pnc_cli.swagger_client.apis.buildrecords_api import BuildrecordsApi
from test import testutils
import pnc_cli.user_config as uc


@pytest.fixture(scope='function', autouse=True)
def get_builds_api():
    global builds_api
    builds_api = BuildrecordsApi(uc.user.get_api_client())

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
    records = builds_api.get_all().content
    record = builds_api.get_specific(id=records[1].id).content
    assert record is not None


def test_get_all_for_build_configuration_no_configuration_id():
    testutils.assert_raises_valueerror(builds_api, 'get_all_for_build_configuration', configuration_id=None)


def test_get_all_for_build_configuration_invalid_param():
    testutils.assert_raises_typeerror(builds_api, 'get_all_for_build_configuration', configuration_id=1)


def test_get_all_for_build_configuration():
    build_config = builds_api.get_all().content[1]
    records = builds_api.get_all_for_build_configuration(configuration_id=build_config.id).content
    assert records is not None


def test_get_all_for_project_no_project_id():
    testutils.assert_raises_valueerror(builds_api, 'get_all_for_project', project_id=None)


def test_get_all_for_project_invalid_param():
    testutils.assert_raises_typeerror(builds_api, 'get_all_for_project', project_id=1)


def test_get_all_for_project():
    records = builds_api.get_all_for_project(project_id=1).content
    assert records is not None


def test_get_built_artifacts_no_id():
    testutils.assert_raises_valueerror(builds_api, 'get_built_artifacts', id=None)


def test_get_built_artifacts_invalid_param():
    testutils.assert_raises_typeerror(builds_api, 'get_built_artifacts', id=1)


def test_get_built_artifacts():
    record = builds_api.get_all().content[1]
    artifacts = builds_api.get_built_artifacts(id=record.id).content
    assert artifacts is not None


def test_get_dependency_artifacts_no_id():
    testutils.assert_raises_valueerror(builds_api, 'get_dependency_artifacts', id=None)


def test_get_dependency_artifacts_invalid_param():
    testutils.assert_raises_typeerror(builds_api, 'get_dependency_artifacts', id=1)


def test_get_dependency_artifacts():
    record = builds_api.get_all().content[1]
    artifacts = builds_api.get_dependency_artifacts(id=record.id).content
    assert artifacts is not None


def test_get_logs_no_id():
    testutils.assert_raises_valueerror(builds_api, 'get_logs', id=None)


def test_get_logs_invalid_param():
    testutils.assert_raises_typeerror(builds_api, 'get_logs', id=1)


def test_get_logs():
    record = builds_api.get_all().content[1]
    log = builds_api.get_logs(id=record.id)
    assert log is not None


def test_get_build_configuration_audited_no_id():
    testutils.assert_raises_valueerror(builds_api, 'get_build_configuration_audited', id=None)


def test_get_build_configuration_audited_invalid_param():
    testutils.assert_raises_typeerror(builds_api, 'get_build_configuration_audited', id=1)


def test_get_build_configuration_audited():
    record = builds_api.get_all().content[1]
    audited = builds_api.get_build_configuration_audited(id=record.id).content
    assert audited is not None


def test_get_artifacts_no_id():
    testutils.assert_raises_valueerror(builds_api, 'get_artifacts', id=None)


def test_get_artifacts_invalid_param():
    testutils.assert_raises_typeerror(builds_api, 'get_artifacts', id=1)


def test_get_artifacts():
    record = builds_api.get_all().content[1]
    result = builds_api.get_artifacts(id=record.id)
    assert result is not None


def test_get_attributes_no_id():
    testutils.assert_raises_valueerror(builds_api, 'get_attributes', id=None)


def test_get_attributes_invalid_param():
    testutils.assert_raises_typeerror(builds_api, 'get_attributes', id=1)


def test_get_attributes():
    record = builds_api.get_all().content[1]
    builds_api.put_attribute(id=record.id, key='test_get_attributes', value='hi')
    result = builds_api.get_attributes(id=record.id).content
    assert result is not None
    builds_api.remove_attribute(id=record.id, key='test_get_attributes')


def test_put_attribute_no_id():
    testutils.assert_raises_valueerror(builds_api, 'put_attribute', id=None, key='key', value='value')


def test_put_attribute_no_key():
    testutils.assert_raises_valueerror(builds_api, 'put_attribute', id=1, key=None, value='value')


def test_put_attribute_no_value():
    testutils.assert_raises_valueerror(builds_api, 'put_attribute', id=1, key='key', value=None)


def test_put_attribute_invalid_param():
    testutils.assert_raises_typeerror(builds_api, 'put_attribute', id=1, key='key', value='value')


def test_put_attribute():
    record = builds_api.get_all().content[1]
    builds_api.put_attribute(id=record.id, key='test_put_attribute', value='value')
    result = builds_api.get_specific(id=record.id).content
    assert 'test_put_attribute' in result.attributes


def test_query_by_attribute_no_key():
    testutils.assert_raises_valueerror(builds_api, 'query_by_attribute', key=None, value='value')


def test_query_by_attribute_no_value():
    testutils.assert_raises_valueerror(builds_api, 'query_by_attribute', key='key', value=None)


def test_query_by_attribute_invalid_param():
    testutils.assert_raises_typeerror(builds_api, 'query_by_attribute', key='key', value='value')


def test_query_by_attribute():
    record = builds_api.get_all().content[1]
    builds_api.put_attribute(id=record.id, key='test_query_by_attribute', value='value')
    result = builds_api.query_by_attribute(key='test_query_by_attribute', value='value')
    assert result == record
    builds_api.remove_attribute(id=record.id, key='test_query_by_attribute')


def test_remove_attribute_no_id():
    testutils.assert_raises_valueerror(builds_api, 'remove_attribute', id=None, key='key')


def test_remove_attribute_no_key():
    testutils.assert_raises_valueerror(builds_api, 'remove_attribute', id=1, key=None)


def test_remove_attribute_invalid_param():
    testutils.assert_raises_typeerror(builds_api, 'remove_attribute', id=1, key='key')


def test_remove_attribute():
    record = builds_api.get_all().content[1]
    builds_api.put_attribute(id=record.id, key='test_remove_attribute', value='value')
    assert 'test_remove_attribute' in builds_api.get_specific(id=record.id).content.attributes
    builds_api.remove_attribute(id=record.id, key='test_remove_attribute')
    assert 'test_remove_attribute' not in builds_api.get_specific(id=record.id).content.attributes
