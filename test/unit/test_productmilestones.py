from mock import patch, MagicMock
from pnc_cli import productmilestones
from test import testutils
from pnc_cli.swagger_client.models import ProductMilestoneRest

def test_create_milestone_object():
    compare = ProductMilestoneRest()
    compare.version = '1.0.1.GA'
    compare.starting_date = '2015-01-01'
    result = productmilestones.create_milestone_object(version='1.0.1.GA', starting_date='2015-01-01')
    assert result.to_dict() == compare.to_dict()

@patch('pnc_cli.productmilestones.milestones_api.get_all', return_value=MagicMock(content=[1, 2, 3]))
def test_list_milestones(mock):
    result = productmilestones.list_milestones()
    mock.assert_called_once_with(page_size=200, q="", sort="")
    assert result == [1, 2, 3]

@patch('pnc_cli.productmilestones.create_milestone_object', return_value='created milestone')
@patch('pnc_cli.productmilestones.milestones_api.create_new', return_value=MagicMock(content='created milestone'))
@patch('pnc_cli.productmilestones.productversions_api.get_all',
       return_value=MagicMock(content=[MagicMock(id=1), MagicMock(id=2)]))
@patch('pnc_cli.productmilestones.productversions_api.get_specific', return_value=MagicMock(content=MagicMock(version=1.0)))
def test_create_milestone(mock_get_specific, mock_get_all, mock_create_new, mock_create_milestone_object):
    result = productmilestones.create_milestone(product_version_id=1, version='1.GA', start_date='2015-01-01',
                                                planned_release_date='2015-01-02')
    mock_get_all.assert_called_once_with()
    mock_create_milestone_object.assert_called_once_with(product_version_id=1, version='1.0.1.GA', start_date='2015-01-01',
                                                planned_release_date='2015-01-02')
    mock_get_specific.assert_called_once_with(id=1)
    mock_create_new.assert_called_once_with(body='created milestone')
    assert result == 'created milestone'

@patch('pnc_cli.productmilestones.create_milestone_object')
@patch('pnc_cli.productmilestones.milestones_api.create_new')
@patch('pnc_cli.productmilestones.productversions_api.get_all',
       return_value=MagicMock(content=[MagicMock(id=1), MagicMock(id=2)]))
@patch('pnc_cli.productmilestones.productversions_api.get_specific')
def test_create_milestone_noversion(mock_get_specific, mock_get_all, mock_create_new, mock_create_milestone_object):
    result = productmilestones.create_milestone(product_version_id=2000, version='1.GA', start_date='2015-01-01',
                                                planned_release_date='2015-01-02')
    mock_get_all.assert_called_once_with()
    assert not mock_create_milestone_object.called
    assert not mock_get_specific.called
    assert not mock_create_new.called
    assert not result

@patch('pnc_cli.productmilestones.create_milestone_object')
@patch('pnc_cli.productmilestones.milestones_api.create_new')
@patch('pnc_cli.productmilestones.productversions_api.get_all',
       return_value=MagicMock(content=[MagicMock(id=1), MagicMock(id=2)]))
@patch('pnc_cli.productmilestones.productversions_api.get_specific')
def test_create_milestone_badversion(mock_get_specific, mock_get_all, mock_create_new, mock_create_milestone_object):
    result = productmilestones.create_milestone(product_version_id=1, version='gaga1.GA', start_date='2015-01-01',
                                                planned_release_date='2015-01-02')
    mock_get_all.assert_called_once_with()
    assert not mock_create_milestone_object.called
    assert not mock_get_specific.called
    assert not mock_create_new.called
    assert not result

@patch('pnc_cli.productmilestones.milestones_api.get_all_by_product_version_id', return_value=MagicMock(content=[MagicMock(version_id=1, ver_name='mock1'), MagicMock(version_id=1, ver_name='mock2')]))
def test_list_milestones_for_version(mock):
    result = [x.ver_name for x in productmilestones.list_milestones_for_version(1)]
    mock.assert_called_once_with(version_id=1)
    assert result == ['mock1', 'mock2']

@patch('pnc_cli.productmilestones.milestones_api.get_specific', return_value=MagicMock(content='target milestone'))
def test_get_milestone(mock):
    result = productmilestones.get_milestone(1)
    mock.assert_called_once_with(id=1)
    assert result == 'target milestone'

@patch('pnc_cli.productmilestones.milestones_api.get_specific')
@patch('pnc_cli.productmilestones.milestones_api.update', return_value=MagicMock(content='updated milestone'))
def test_update_milestone(mock_update, mock_get_specific):
    mock = MagicMock()
    mockcontent = MagicMock(content=mock)
    mock_get_specific.return_value = mockcontent
    result = productmilestones.update_milestone(id=1, version='1.0.1.GA', start_date='2015-01-01')
    mock_get_specific.assert_called_once_with(id=1)
    assert getattr(mock, 'version') == '1.0.1.GA'
    assert getattr(mock, 'start_date') == '2015-01-01'
    mock_update.assert_called_once_with(id=1, body=mock)
    assert result == 'updated milestone'









