import pytest

__author__ = 'thauser'
from pnc_cli import utils
from pnc_cli.swagger_client.apis import BuildconfigsetrecordsApi
from test import testutils

bcsr_api = None


@pytest.fixture(scope='function', autouse=True)
def init_api():
    global bcsr_api
    bcsr_api = BuildconfigsetrecordsApi(utils.get_api_client())


def test_get_all_invalid_param():
    testutils.assert_raises_typeerror(bcsr_api, 'get_all')


def test_get_all():
    bcrsets = bcsr_api.get_all(page_index=0, page_size=1000000, sort='', q='').content
    assert bcrsets is not None


def test_get_specific_no_id():
    testutils.assert_raises_valueerror(bcsr_api, 'get_specific', id=None)


def test_get_specific_invalid_param():
    testutils.assert_raises_typeerror(bcsr_api, 'get_specific', id=1)


def test_get_specific():
    bcrset = bcsr_api.get_specific(id=1).content
    assert bcrset is not None


def test_get_build_records_no_id():
    testutils.assert_raises_valueerror(bcsr_api, 'get_build_records', id=None)


def test_get_build_records_invalid_param():
    testutils.assert_raises_typeerror(bcsr_api, 'get_build_records', id=1)


@pytest.mark.xpass(reason='none of the default record sets contain build records, and there is no api to add them.')
def test_get_build_records():
    records = bcsr_api.get_build_records(id=1, page_index=0, page_size=1000000, sort='', q='').content
    assert records is None
