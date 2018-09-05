from mock import MagicMock, patch
from pnc_cli import builds


@patch('pnc_cli.builds.pnc_api.builds_running.cancel', return_value=MagicMock(content=None))
def test_cancel_build(mock_cancel):
    result = builds.cancel_running_build_raw(1)
    mock_cancel.assert_called_once_with(id=1)
    assert result == None