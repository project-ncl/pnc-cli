__author__ = 'Tom'
from mock import MagicMock, patch
from pnc_cli import buildrecords

@patch('pnc_cli.buildrecords.records_api')
def test_list_build_records(mock_records_api):
    mock_records_api.get_all = MagicMock(name='get_all_mock', return_value=MagicMock(name='mock_response', content=[1, 2, 3]))
    result = buildrecords.list_build_records()
    mock_records_api.get_all.assert_called_once_with()
    assert result == [1, 2, 3]

@patch('pnc_cli.buildconfigurations.get_config_id', autospec=True, return_value='1')
@patch('pnc_cli.buildrecords.records_api.get_all_for_build_configuration', return_value=MagicMock(content=[2,3,4]))
def test_list_records_for_build_configuration_id(mock_records_api, mock_get_config_id):
    mock_get_config_id.return_value = '1'
    result = buildrecords.list_records_for_build_configuration(id='1')
    mock_get_config_id.assert_called_once_with('1', None)
    mock_records_api.assert_called_once_with(configuration_id='1')
    assert result == [2,3,4]

@patch('pnc_cli.buildconfigurations.get_config_id', autospec=True, return_value='2')
@patch('pnc_cli.buildrecords.records_api.get_all_for_build_configuration', return_value=MagicMock(content=[1,2,3]))
def test_list_records_for_build_configuration_name(mock_records_api, mock_get_config_id):
    result = buildrecords.list_records_for_build_configuration(name='test configuration')
    mock_get_config_id.assert_called_once_with(None, 'test configuration')
    mock_records_api.assert_called_once_with(configuration_id='2')
    assert result == [1,2,3]

@patch('pnc_cli.buildconfigurations.get_config_id', autospec=True, return_value=None)
def test_list_records_for_build_configuration_notexist(mock_get_config_id):
    result = buildrecords.list_records_for_build_configuration(id='10')
    mock_get_config_id.assert_called_once_with('10', None)
    assert not result

@patch('pnc_cli.projects.get_project_id', autospec=True, return_value='1')
@patch('pnc_cli.buildrecords.records_api.get_all_for_project', return_value=MagicMock(content=[1]))
def test_list_records_for_project_id(mock_records_api, mock_get_project_id):
    result = buildrecords.list_records_for_project(id='1')
    mock_get_project_id.assert_called_once_with('1', None)
    mock_records_api.assert_called_once_with(project_id='1')
    assert result == [1]

@patch('pnc_cli.projects.get_project_id', autospec=True, return_value='2')
@patch('pnc_cli.buildrecords.records_api.get_all_for_project', return_value=MagicMock(content=[2]))
def test_list_records_for_project_name(mock_records_api, mock_get_project_id):
    result = buildrecords.list_records_for_project(name='Tom')
    mock_get_project_id.assert_called_once_with(None, 'Tom')
    mock_records_api.assert_called_once_with(project_id='2')
    assert result == [2]

@patch('pnc_cli.projects.get_project_id', autospec=True, return_value=None)
def test_list_records_for_project_notexist(mock_get_project_id):
    result = buildrecords.list_records_for_project(name="Doesn't exist")
    mock_get_project_id.assert_called_once_with(None,"Doesn't exist")
    assert not result

@patch('pnc_cli.buildrecords.records_api.get_specific', return_value=MagicMock(content='build record 2'))
def test_get_build_record_id(mock_get_specific):
    result = buildrecords.get_build_record('2')
    mock_get_specific.assert_called_once_with(id='2')
    assert result == 'build record 2'

@patch('pnc_cli.buildrecords.record_exists', return_value=False)
def test_get_build_record_notexist(mock):
    result = buildrecords.get_build_record(id='2')
    mock.assert_called_once_with('2')
    assert not result

@patch('pnc_cli.buildrecords.records_api.get_artifacts', return_value=MagicMock(content=['artifact1','artifact2']))
def test_list_build_artifacts(mock):
    result = buildrecords.list_build_artifacts('1')
    mock.assert_called_once_with(id='1')
    assert result == ['artifact1', 'artifact2']

@patch('pnc_cli.buildrecords.records_api.get_artifacts', return_value=None)
def test_list_build_artifacts_notexist(mock):
    result = buildrecords.list_build_artifacts('100')
    mock.assert_called_once_with(id='100')
    assert not result

@patch('pnc_cli.buildrecords.records_api.get_build_configuration_audited', return_value=MagicMock(content='audited bc'))
def test_get_audited_configuration_for_record(mock):
    result = buildrecords.get_audited_configuration_for_record(id=100)
    mock.assert_called_once_with(id=100)
    assert result == 'audited bc'

@patch('pnc_cli.buildrecords.records_api.get_build_configuration_audited', return_value=None)
def test_get_audited_configuration_for_record_notexist(mock):
    result = buildrecords.get_audited_configuration_for_record(id=100)
    mock.assert_called_once_with(id=100)
    assert not result

@patch('pnc_cli.buildrecords.records_api.get_logs', return_value='log here.')
def test_get_log_for_record(mock):
    result = buildrecords.get_log_for_record(id=100)
    mock.assert_called_once_with(id=100)
    assert result == 'log here.'

@patch('pnc_cli.buildrecords.records_api.get_logs', return_value=None)
def test_get_log_for_record_notexist(mock):
    result = buildrecords.get_log_for_record(id=100)
    mock.assert_called_once_with(id=100)
    assert not result