__author__ = 'thauser'
from test import testutils
from pnc_cli import utils
from pnc_cli.swagger_client.apis import BuildtasksApi

tasks_api = BuildtasksApi(utils.get_api_client())


def test_build_task_completed_no_task_id():
    testutils.assert_raises_valueerror(tasks_api, 'build_task_completed', task_id=None, build_status='NEW')


def test_build_task_completed_no_build_status():
    testutils.assert_raises_valueerror(tasks_api, 'build_task_completed', task_id=1, build_status=None)


def test_build_task_completed_invalid_param():
    testutils.assert_raises_typeerror(tasks_api, 'build_task_completed', task_id=1, build_status='NEW')


def test_build_task_completed():
    response = tasks_api.build_task_completed(task_id=1, build_status='NEW')
    assert response

