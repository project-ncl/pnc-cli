import pytest

__author__ = 'thauser'
from pnc_cli import utils
from pnc_cli.swagger_client.apis import BuildconfigsetrecordsApi

bcsr_api = BuildconfigsetrecordsApi(utils.get_api_client())


def test_get_all():
    bcrsets = bcsr_api.get_all().content
    assert bcrsets is not None


def test_get_specific():
    bcrset = bcsr_api.get_specific(id=1).content
    assert bcrset is not None


@pytest.mark.xfail(reason='none of the default record sets contain build records, and there is no api to add them.')
def test_get_build_records():
    records = bcsr_api.get_build_records(id=1).content
    assert records is None
