from mock import patch, MagicMock, call
from pnc_cli import productmilestones
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
@patch('pnc_cli.productmilestones.productversions_api.get_specific', return_value=MagicMock(content=MagicMock(version=1.0)))
def test_create_milestone(mock_get_specific, mock_create_new, mock_create_milestone_object):
    result = productmilestones.create_milestone(product_version_id=1, version='1.GA', starting_date='2015-01-01',
                                                planned_end_date='2015-01-02')


    mock_create_milestone_object.assert_called_once_with(product_version_id=1, version='1.0.1.GA', starting_date='2015-01-01',
                                                planned_end_date='2015-01-02')
    get_specific_calls = [call(id=1), call(id=1)]
    mock_get_specific.assert_has_calls(get_specific_calls)
    mock_create_new.assert_called_once_with(body='created milestone')
    assert result == 'created milestone'


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
@patch('pnc_cli.productmilestones.unique_version_value')
@patch('pnc_cli.productmilestones.get_product_version_from_milestone', return_value=1)
def test_update_milestone(mock_get_version, mock_unique, mock_update, mock_get_specific):
    mock = ProductMilestoneRest()
    mock.id = '1'
    mock.version = '0.0.1.GA'
    mock.starting_date = '2015-01-01'
    mock.planned_end_date = '2016-01-01'
    mockcontent = MagicMock(content=mock)
    mock_get_specific.return_value = mockcontent
    result = productmilestones.update_milestone(id=1, version='1.0.1.GA', starting_date='2015-01-01')
    mock_get_specific.assert_called_once_with(id=1)
    mock_get_version.assert_called_once_with(1)
    mock_unique.assert_called_once_with(1, '1.0.1.GA')
    assert getattr(mock, 'version') == '1.0.1.GA'
    assert getattr(mock, 'starting_date') == '2015-01-01'
    mock_update.assert_called_once_with(id=1, body=mock)
    assert result == 'updated milestone'


#TODO: test new functions in this module