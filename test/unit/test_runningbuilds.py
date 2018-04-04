from mock import patch, MagicMock
from pnc_cli import runningbuilds

__author__ = 'thauser'


@patch('pnc_cli.runningbuilds.pnc_api.running_builds.get_all', return_value=MagicMock(content=[1, 2, 3]))
def test_list_running_builds(mock):
    result = runningbuilds.list_running_builds_raw()
    mock.assert_called_once_with(page_index=0, page_size=200, sort="")
    assert result == [1, 2, 3]


@patch('pnc_cli.runningbuilds.pnc_api.running_builds.get_specific', return_value=MagicMock(content='running-build'))
def test_get_running_build(mock):
    result = runningbuilds.get_running_build_raw(1)
    mock.assert_called_once_with(id=1)
    assert result == 'running-build'