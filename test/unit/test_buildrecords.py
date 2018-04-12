__author__ = 'Tom'
from mock import MagicMock, patch

from pnc_cli import buildrecords
from pnc_cli.swagger_client import BuildconfigurationsApi
from pnc_cli.swagger_client import ProjectsApi


@patch('pnc_cli.buildrecords.records_api')
def test_list_build_records(mock_records_api):
    mock_records_api.get_all = MagicMock(name='get_all_mock',
                                         return_value=MagicMock(name='mock_response', content=[1, 2, 3]))
    result = buildrecords.list_build_records_raw()
    mock_records_api.get_all.assert_called_once_with(page_index=0, page_size=200, q="", sort="")
    assert result == [1, 2, 3]


@patch('pnc_cli.common.set_id', autospec=True, return_value='1')
@patch('pnc_cli.buildrecords.records_api.get_all_for_build_configuration', return_value=MagicMock(content=[2, 3, 4]))
@patch('pnc_cli.buildrecords.configs_api', autospec=BuildconfigurationsApi)
def test_list_records_for_build_configuration_id(mock_configs_api, mock_records_api, mock_set_id):
    result = buildrecords.list_records_for_build_configuration_raw(id='1')
    mock_set_id.assert_called_once_with(mock_configs_api, '1', None)
    mock_records_api.assert_called_once_with(configuration_id='1', page_index=0, page_size=200, q="", sort="")
    assert result == [2, 3, 4]


@patch('pnc_cli.common.set_id', return_value=2)
@patch('pnc_cli.buildrecords.records_api.get_all_for_build_configuration', return_value=MagicMock(content=[1, 2, 3]))
@patch('pnc_cli.buildrecords.configs_api', autospec=BuildconfigurationsApi)
def test_list_records_for_build_configuration_name(mock_configs_api, mock_records_api, mock_set_id):
    result = buildrecords.list_records_for_build_configuration_raw(name='test configuration')
    mock_set_id.assert_called_once_with(mock_configs_api, None, 'test configuration')
    mock_records_api.assert_called_once_with(configuration_id=2, page_index=0, page_size=200, q="", sort="")
    assert result == [1, 2, 3]


@patch('pnc_cli.common.set_id', autospec=True, return_value='1')
@patch('pnc_cli.buildrecords.records_api.get_all_for_project_1', return_value=MagicMock(content=[1]))
@patch('pnc_cli.buildrecords.projects_api', autospec=ProjectsApi)
def test_list_records_for_project_id(mock_projects_api, mock_records_api, mock_set_id):
    result = buildrecords.list_records_for_project_raw(id='1')
    mock_set_id.assert_called_once_with(mock_projects_api, '1', None)
    mock_records_api.assert_called_once_with(project_id='1', page_index=0, page_size=200, q="", sort="")
    assert result == [1]


@patch('pnc_cli.common.set_id', autospec=True, return_value='2')
@patch('pnc_cli.buildrecords.records_api.get_all_for_project_1', return_value=MagicMock(content=[2]))
@patch('pnc_cli.buildrecords.projects_api', autospec=ProjectsApi)
def test_list_records_for_project_name(mock_projects_api, mock_records_api, mock_set_id):
    result = buildrecords.list_records_for_project_raw(name='Tom')
    mock_set_id.assert_called_once_with(mock_projects_api, None, 'Tom')
    mock_records_api.assert_called_once_with(project_id='2', page_index=0, page_size=200, q="", sort="")
    assert result == [2]


@patch('pnc_cli.buildrecords.records_api.get_specific', return_value=MagicMock(content='build record 2'))
def test_get_build_record_id(mock_get_specific):
    result = buildrecords.get_build_record_raw('2')
    mock_get_specific.assert_called_once_with(id='2')
    assert result == 'build record 2'


@patch('pnc_cli.buildrecords.records_api.get_built_artifacts',
       return_value=MagicMock(content=['artifact1', 'artifact2']))
def test_list_build_artifacts(mock):
    result = buildrecords.list_built_artifacts_raw('1')
    mock.assert_called_once_with(id='1', page_index=0, page_size=200, q="", sort="")
    assert result == ['artifact1', 'artifact2']


@patch('pnc_cli.buildrecords.records_api.get_dependency_artifacts',
       return_value=MagicMock(content=['artifact1', 'artifact2']))
def test_list_dependency_artifacts(mock):
    result = buildrecords.list_dependency_artifacts_raw('1')
    mock.assert_called_once_with(id='1', page_index=0, page_size=200, q="", sort="")
    assert result == ['artifact1', 'artifact2']


@patch('pnc_cli.buildrecords.records_api.get_build_configuration_audited', return_value=MagicMock(content='audited bc'))
def test_get_audited_configuration_for_record(mock):
    result = buildrecords.get_audited_configuration_for_record_raw(id=100)
    mock.assert_called_once_with(id=100)
    assert result == 'audited bc'


@patch('pnc_cli.buildrecords.records_api.get_logs', return_value='log here.')
def test_get_log_for_record(mock):
    result = buildrecords.get_log_for_record_raw(id=100)
    mock.assert_called_once_with(id=100)
    assert result == 'log here.'


@patch('pnc_cli.buildrecords.records_api.get_artifacts', return_value=MagicMock(content="list of artifacts"))
def test_get_artifacts(mock):
    result = buildrecords.list_artifacts_raw(id=100)
    mock.assert_called_once_with(id=100, page_index=0, page_size=200, sort="", q="")
    assert result == "list of artifacts"

@patch('pnc_cli.buildrecords.records_api.put_attribute')
def test_put_attribute(mock):
    result = buildrecords.put_attribute(1,'key','value')
    assert not result
    mock.assert_called_once_with(id=1, key='key', value='value')


@patch('pnc_cli.buildrecords.records_api.remove_attribute')
def test_remove_attribute(mock):
    result = buildrecords.remove_attribute(1, 'key')
    assert not result
    mock.assert_called_once_with(id=1, key='key')


@patch('pnc_cli.buildrecords.records_api.query_by_attribute', return_value=MagicMock(content=MagicMock(attributes={"key":"value"})))
def test_query_by_attribute(mock):
    result = buildrecords.query_by_attribute_raw('key', 'value')
    assert 'key' in result.attributes
    mock.assert_called_once_with(key='key', value='value')


@patch('pnc_cli.buildrecords.records_api.get_attributes', return_value=MagicMock(content=MagicMock(attributes={'key1':'value1','key2':'value2'})))
def test_list_attributes(mock):
    result = buildrecords.list_attributes_raw(1)
    assert result.attributes == {'key1':'value1','key2':'value2'}
    mock.assert_called_once_with(id=1)