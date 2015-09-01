import pytest

from pnc import buildconfigurations
from pnc import runningbuilds


def test_get_all():
    # start a build so that a build is running
    buildconfigurations.trigger(1)
    running_builds = runningbuilds.get_all().json()
    assert running_builds is not None

@pytest.mark.xfail(reason='buildconfigurations.trigger(id) does not always return valid json (?)')
def test_get_specific():
    build = buildconfigurations.trigger(1).json()
    running_build = runningbuilds.get_specific(build['id'])
    assert running_build is not None

