__author__ = 'thauser'
import pytest

from test import testutils
from pnc_cli import utils
from pnc_cli.swagger_client.apis import BuildtasksApi
import pnc_cli.user_config as uc

@pytest.fixture(scope='function', autouse=True)
def get_tasks_api():
    global tasks_api
    tasks_api = BuildtasksApi(uc.user.get_api_client())


def test_build_task_completed_no_task_id():
    testutils.assert_raises_valueerror(tasks_api, 'build_task_completed', task_id=None, build_result='NEW')


def test_build_task_completed_no_build_result():
    testutils.assert_raises_valueerror(tasks_api, 'build_task_completed', task_id=1, build_result=None)


def test_build_task_completed_invalid_param():
    testutils.assert_raises_typeerror(tasks_api, 'build_task_completed', task_id=1, build_result='NEW')


@pytest.mark.xfail(reason='unsure of how to test this correctly.')
def test_build_task_completed():
    response = tasks_api.build_task_completed(task_id=1, build_result='NEW')
    assert response

