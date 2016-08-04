import argparse

import pytest
from mock import patch

import pnc_cli.cli_types as cli_types
# create_autospec dud import
from pnc_cli.swagger_client import EnvironmentsApi
from pnc_cli.swagger_client import ProductmilestonesApi
from pnc_cli.swagger_client import ProductversionsApi
from pnc_cli.swagger_client import ProductsApi
from pnc_cli.swagger_client import ProductreleasesApi
from pnc_cli.swagger_client import ProjectsApi
from pnc_cli.swagger_client import BuildconfigurationsApi
from pnc_cli.swagger_client import BuildrecordsApi
from pnc_cli.swagger_client import LicensesApi
from pnc_cli.swagger_client import BuildconfigsetrecordsApi
from pnc_cli.swagger_client import RunningbuildrecordsApi

__author__ = 'thauser'


# Common validation tests
def test_valid_id():
    result = cli_types.valid_id('1')
    assert result == '1'


def test_valid_id_exception():
    with pytest.raises(argparse.ArgumentTypeError):
        cli_types.valid_id('-1000')


def test_valid_date():
    result = cli_types.valid_date('2015-06-01')
    assert result == '2015-06-01'


def test_valid_date_exception():
    with pytest.raises(argparse.ArgumentTypeError):
        cli_types.valid_date('06-01-1989')


def test_valid_url():
    result = cli_types.valid_url("http://www.tomhauser.com")
    assert result == 'http://www.tomhauser.com'


def test_valid_url_exception():
    with pytest.raises(argparse.ArgumentTypeError):
        cli_types.valid_url('httpzzz://localhost:8080')


# BuildConfiguration tests

def test_valid_bc_name():
    result = cli_types.valid_bc_name('test')
    assert result == 'test'


def test_valid_bc_name_exception():
    with pytest.raises(argparse.ArgumentTypeError):
        cli_types.valid_bc_name("invalid #@)H*! name")


@patch('pnc_cli.common.get_id_by_name', return_value=None)
@patch('pnc_cli.cli_types.configs_api', autospec=BuildconfigurationsApi)
def test_unique_bc_name(mock_configs_api, mock_get_id_by_name):
    result = cli_types.unique_bc_name('test')
    mock_get_id_by_name.assert_called_once_with(mock_configs_api, 'test')
    assert result == 'test'


@patch('pnc_cli.common.get_id_by_name', return_value=1)
@patch('pnc_cli.cli_types.configs_api', autospec=BuildconfigurationsApi)
def test_unique_bc_name_exception(mock_configs_api, mock_get_id_by_name):
    with pytest.raises(argparse.ArgumentTypeError):
        cli_types.unique_bc_name('non-unique')
    mock_get_id_by_name.assert_called_once_with(mock_configs_api, 'non-unique')


@patch('pnc_cli.cli_types.unique_bc_name', return_value='test')
@patch('pnc_cli.cli_types.valid_bc_name', return_value='test')
def test_valid_unique_bc_name(mock_valid_bc_name, mock_unique_bc_name):
    result = cli_types.valid_unique_bc_name('test')
    mock_unique_bc_name.assert_called_once_with('test')
    mock_valid_bc_name.assert_called_once_with('test')
    assert result == 'test'


def test_valid_unique_bc_name_exception():
    with pytest.raises(argparse.ArgumentTypeError):
        cli_types.valid_unique_bc_name("invalid #@)H*! name")


@patch('pnc_cli.cli_types.valid_bc_name')
@patch('pnc_cli.common.get_id_by_name', return_value=1)
@patch('pnc_cli.cli_types.configs_api', autospec=BuildconfigurationsApi)
def test_existing_bc_name(mock_configs_api, mock_get_id_by_name, mock_valid_bc_name):
    result = cli_types.existing_bc_name('test')
    mock_valid_bc_name.assert_called_once_with('test')
    mock_get_id_by_name.assert_called_once_with(mock_configs_api, 'test')
    assert result == 'test'


@patch('pnc_cli.cli_types.valid_bc_name')
@patch('pnc_cli.common.get_id_by_name', return_value=None)
@patch('pnc_cli.cli_types.configs_api', autospec=BuildconfigurationsApi)
def test_existing_bc_name_exception(mock_configs_api, mock_get_id_by_name, mock_valid_bc_name):
    with pytest.raises(argparse.ArgumentTypeError):
        cli_types.existing_bc_name('test')
    mock_valid_bc_name.assert_called_once_with('test')
    mock_get_id_by_name.assert_called_once_with(mock_configs_api, 'test')


@patch('pnc_cli.cli_types.valid_id')
@patch('pnc_cli.common.id_exists', return_value=True)
@patch('pnc_cli.cli_types.configs_api', autospec=BuildconfigurationsApi)
def test_existing_bc_id(mock_configs_api, mock_id_exists, mock_valid_id):
    result = cli_types.existing_bc_id('1')
    mock_valid_id.assert_called_once_with('1')
    mock_id_exists.assert_called_once_with(mock_configs_api, '1')
    assert result == '1'


@patch('pnc_cli.cli_types.valid_id')
@patch('pnc_cli.common.id_exists', return_value=False)
@patch('pnc_cli.cli_types.configs_api', autospec=BuildconfigurationsApi)
def test_existing_bc_id_exception(mock_configs_api, mock_id_exists, mock_valid_id):
    with pytest.raises(argparse.ArgumentTypeError):
        cli_types.existing_bc_id('1')
    mock_valid_id.assert_called_once_with('1')
    mock_id_exists.assert_called_once_with(mock_configs_api, '1')


# Buildconfiguration set tests
@patch('pnc_cli.common.get_id_by_name', return_value=None)
@patch('pnc_cli.cli_types.sets_api', autospec=BuildconfigurationsApi)
def test_unique_bc_set_name(mock_sets_api, mock_get_id_by_name):
    result = cli_types.unique_bc_set_name('test')
    mock_get_id_by_name.assert_called_once_with(mock_sets_api, 'test')
    assert result == 'test'


@patch('pnc_cli.common.get_id_by_name', return_value=1)
@patch('pnc_cli.cli_types.sets_api', autospec=BuildconfigurationsApi)
def test_unique_bc_set_name_exception(mock_sets_api, mock_get_id_by_name):
    with pytest.raises(argparse.ArgumentTypeError):
        cli_types.unique_bc_set_name('test')
    assert mock_get_id_by_name.assert_called_once_with(mock_sets_api, 'test')


@patch('pnc_cli.common.get_id_by_name', return_value=1)
@patch('pnc_cli.cli_types.sets_api', autospec=BuildconfigurationsApi)
def test_existing_bc_set_name(mock_sets_api, mock_get_id_by_name):
    result = cli_types.existing_bc_set_name('test')
    mock_get_id_by_name.assert_called_once_with(mock_sets_api, 'test')
    assert result == 'test'


@patch('pnc_cli.common.get_id_by_name', return_value=None)
@patch('pnc_cli.cli_types.sets_api', autospec=BuildconfigurationsApi)
def test_existing_bc_set_name_exception(mock_sets_api, mock_get_id_by_name):
    with pytest.raises(argparse.ArgumentTypeError):
        cli_types.existing_bc_set_name('test')
    mock_get_id_by_name.assert_called_once_with(mock_sets_api, 'test')


@patch('pnc_cli.common.id_exists', return_value=True)
@patch('pnc_cli.cli_types.valid_id', return_value=1)
@patch('pnc_cli.cli_types.sets_api', autospec=BuildconfigurationsApi)
def test_existing_bc_set_id(mock_sets_api, mock_valid_id, mock_id_exists):
    result = cli_types.existing_bc_set_id(1)
    mock_valid_id.assert_called_once_with(1)
    mock_id_exists.assert_called_once_with(mock_sets_api, 1)
    assert result == 1


@patch('pnc_cli.common.id_exists', return_value=False)
@patch('pnc_cli.cli_types.valid_id', return_value=1)
@patch('pnc_cli.cli_types.sets_api', autospec=BuildconfigurationsApi)
def test_existing_bc_set_id_exception(mock_sets_api, mock_valid_id, mock_id_exists):
    with pytest.raises(argparse.ArgumentTypeError):
        cli_types.existing_bc_set_id(1)
    mock_valid_id.assert_called_once_with(1)
    mock_id_exists.assert_called_once_with(mock_sets_api, 1)


# Product type tests
@patch('pnc_cli.cli_types.valid_id')
@patch('pnc_cli.common.id_exists', return_value=True)
@patch('pnc_cli.cli_types.products_api', autospec=ProductsApi)
def test_existing_product_id(mock_products_api, mock_id_exists, mock_valid_id):
    result = cli_types.existing_product_id('1')
    mock_valid_id.assert_called_once_with('1')
    mock_id_exists.assert_called_once_with(mock_products_api, '1')
    assert result == '1'


@patch('pnc_cli.cli_types.valid_id')
@patch('pnc_cli.common.id_exists', return_value=False)
@patch('pnc_cli.cli_types.products_api', autospec=ProductsApi)
def test_existing_product_id_exception(mock_products_api, mock_id_exists, mock_valid_id):
    with pytest.raises(argparse.ArgumentTypeError):
        cli_types.existing_product_id('1')
    mock_valid_id.assert_called_once_with('1')
    mock_id_exists.assert_called_once_with(mock_products_api, '1')


@patch('pnc_cli.common.get_id_by_name', return_value=1)
@patch('pnc_cli.cli_types.products_api', autospec=ProductsApi)
def test_existing_product_name(mock_products_api, mock_get_id_by_name):
    result = cli_types.existing_product_name('test')
    mock_get_id_by_name.assert_called_once_with(mock_products_api, 'test')
    assert result == 'test'


@patch('pnc_cli.common.get_id_by_name', return_value=None)
@patch('pnc_cli.cli_types.products_api', autospec=ProductsApi)
def test_existing_product_name_exception(mock_products_api, mock_get_id_by_name):
    with pytest.raises(argparse.ArgumentTypeError):
        cli_types.existing_product_name('test')
    mock_get_id_by_name.assert_called_once_with(mock_products_api, 'test')


@patch('pnc_cli.common.get_id_by_name', return_value=None)
@patch('pnc_cli.cli_types.products_api', autospec=ProductsApi)
def test_unique_product_name(mock_products_api, mock_get_id_by_name):
    result = cli_types.unique_product_name('test')
    mock_get_id_by_name.assert_called_once_with(mock_products_api, 'test')
    assert result == 'test'


@patch('pnc_cli.common.get_id_by_name', return_value='1')
@patch('pnc_cli.cli_types.products_api', autospec=ProductsApi)
def test_unique_product_name_exception(mock_products_api, mock_get_id_by_name):
    with pytest.raises(argparse.ArgumentTypeError):
        cli_types.unique_product_name('existing')
    mock_get_id_by_name.assert_called_once_with(mock_products_api, 'existing')


# ProductVersion type tests
@patch('pnc_cli.cli_types.valid_id')
@patch('pnc_cli.common.id_exists', return_value=True)
@patch('pnc_cli.cli_types.versions_api', autospec=ProductversionsApi)
def test_existing_product_version(mock_versions_api, mock_id_exists, mock_valid_id):
    result = cli_types.existing_product_version('1')
    mock_valid_id.assert_called_once_with('1')
    mock_id_exists.assert_called_once_with(mock_versions_api, '1')
    assert result == '1'


@patch('pnc_cli.cli_types.valid_id')
@patch('pnc_cli.common.id_exists', return_value=False)
@patch('pnc_cli.cli_types.versions_api', autospec=ProductversionsApi)
def test_existing_product_version_exception(mock_versions_api, mock_id_exists, mock_valid_id):
    with pytest.raises(argparse.ArgumentTypeError):
        cli_types.existing_product_version('1')
    mock_valid_id.assert_called_once_with('1')
    mock_id_exists.assert_called_once_with(mock_versions_api, '1')


@patch('pnc_cli.utils.is_valid_version', return_value=True)
def test_valid_version_two_digits(mock):
    result = cli_types.valid_version_two_digits('1.1')
    mock.assert_called_once_with('1.1', '^\d+\.\d+')
    assert result == '1.1'


@patch('pnc_cli.utils.is_valid_version', return_value=False)
def test_valid_version_two_digits_exception(mock):
    with pytest.raises(argparse.ArgumentTypeError):
        cli_types.valid_version_two_digits('1.1')
    mock.assert_called_once_with('1.1', '^\d+\.\d+')


# ProductMilestone type tests
@patch('pnc_cli.cli_types.valid_id', return_value=True)
@patch('pnc_cli.common.id_exists', return_value=True)
@patch('pnc_cli.cli_types.milestones_api', autospec=ProductmilestonesApi)
def test_existing_product_milestone(mock_milestones_api, mock_id_exists, mock_valid_id):
    result = cli_types.existing_product_milestone('1')
    mock_valid_id.assert_called_once_with('1')
    mock_id_exists.assert_called_once_with(mock_milestones_api, '1')
    assert result == '1'


@patch('pnc_cli.cli_types.valid_id', return_value=True)
@patch('pnc_cli.common.id_exists', return_value=False)
@patch('pnc_cli.cli_types.milestones_api', autospec=ProductmilestonesApi)
def test_existing_product_milestone_exception(mock_milestones_api, mock_id_exists, mock_valid_id):
    with pytest.raises(argparse.ArgumentTypeError):
        cli_types.existing_product_milestone('1')
    mock_valid_id.assert_called_once_with('1')
    mock_id_exists.assert_called_once_with(mock_milestones_api, '1')


@patch('pnc_cli.utils.is_valid_version', return_value=True)
def test_valid_version_create(mock):
    result = cli_types.valid_version_create('1.ER1')
    mock.assert_called_once_with('1.ER1', '^\d+\.\w+$')
    assert result == '1.ER1'


@patch('pnc_cli.utils.is_valid_version', return_value=False)
def test_valid_version_create_exception(mock):
    with pytest.raises(argparse.ArgumentTypeError):
        cli_types.valid_version_create('1.11.1')
    mock.assert_called_once_with('1.11.1', '^\d+\.\w+$')


@patch('pnc_cli.utils.is_valid_version', return_value=True)
def test_valid_version_update(mock):
    result = cli_types.valid_version_update('1.1.1.GA')
    mock.assert_called_once_with('1.1.1.GA', '^\d+\.\d+\.\d+\.\w+$')
    assert result == '1.1.1.GA'


@patch('pnc_cli.utils.is_valid_version', return_value=False)
def test_valid_version_update_exception(mock):
    with pytest.raises(argparse.ArgumentTypeError):
        cli_types.valid_version_update('1.1.1.GA')
    mock.assert_called_once_with('1.1.1.GA', '^\d+\.\d+\.\d+\.\w+$')


# ProductRelease type tests
@patch('pnc_cli.cli_types.valid_id')
@patch('pnc_cli.common.id_exists', return_value=True)
@patch('pnc_cli.cli_types.releases_api', autospec=ProductreleasesApi)
def test_existing_product_release(mock_releases_api, mock_id_exists, mock_valid_id):
    result = cli_types.existing_product_release('1')
    mock_valid_id.assert_called_once_with('1')
    mock_id_exists.assert_called_once_with(mock_releases_api, '1')
    assert result == '1'


@patch('pnc_cli.cli_types.valid_id')
@patch('pnc_cli.common.id_exists', return_value=False)
@patch('pnc_cli.cli_types.releases_api', autospec=ProductreleasesApi)
def test_existing_product_release_exception(mock_releases_api, mock_id_exists, mock_valid_id):
    with pytest.raises(argparse.ArgumentTypeError):
        cli_types.existing_product_release('1')
    mock_valid_id.assert_called_once_with('1')
    mock_id_exists.assert_called_once_with(mock_releases_api, '1')


@patch('pnc_cli.cli_types.valid_id')
@patch('pnc_cli.common.id_exists', return_value=True)
@patch('pnc_cli.cli_types.envs_api', autospec=EnvironmentsApi)
def test_existing_environment_id(mock_envs_api, mock_id_exists, mock_valid_id):
    result = cli_types.existing_environment_id('1')
    mock_valid_id.assert_called_once_with('1')
    mock_id_exists(mock_envs_api, '1')
    assert result == '1'


@patch('pnc_cli.cli_types.valid_id')
@patch('pnc_cli.common.id_exists', return_value=False)
@patch('pnc_cli.cli_types.envs_api', autospec=EnvironmentsApi)
def test_existing_environment_id_exception(mock_envs_api, mock_id_exists, mock_valid_id):
    with pytest.raises(argparse.ArgumentTypeError):
        cli_types.existing_environment_id('1')
    mock_valid_id.assert_called_once_with('1')
    mock_id_exists(mock_envs_api, '1')


@patch('pnc_cli.common.get_id_by_name', return_value='1')
@patch('pnc_cli.cli_types.envs_api', autospec=EnvironmentsApi)
def test_existing_environment_name(mock_envs_api, mock_get_id_by_name):
    result = cli_types.existing_environment_name('test')
    mock_get_id_by_name.assert_called_once_with(mock_envs_api, 'test')
    assert result == 'test'


@patch('pnc_cli.common.get_id_by_name', return_value=None)
@patch('pnc_cli.cli_types.envs_api', autospec=EnvironmentsApi)
def test_existing_environment_name_exception(mock_envs_api, mock_get_id_by_name):
    with pytest.raises(argparse.ArgumentTypeError):
        cli_types.existing_environment_name('test')
    mock_get_id_by_name.assert_called_once_with(mock_envs_api, 'test')


@patch('pnc_cli.common.get_id_by_name', return_value=None)
@patch('pnc_cli.cli_types.envs_api', autospec=EnvironmentsApi)
def test_unique_environment_name(mock_envs_api, mock_get_id_by_name):
    result = cli_types.unique_environment_name('testerino')
    mock_get_id_by_name.assert_called_once_with(mock_envs_api, 'testerino')
    assert result == 'testerino'


@patch('pnc_cli.common.get_id_by_name', return_value=1)
@patch('pnc_cli.cli_types.envs_api', autospec=EnvironmentsApi)
def test_unique_environment_name_exception(mock_envs_api, mock_get_id_by_name):
    with pytest.raises(argparse.ArgumentTypeError):
        cli_types.unique_environment_name('testerino')
    mock_get_id_by_name.assert_called_once_with(mock_envs_api, 'testerino')


# Project type tests
@patch('pnc_cli.cli_types.valid_id')
@patch('pnc_cli.common.id_exists', return_value=True)
@patch('pnc_cli.cli_types.projects_api', autospec=ProjectsApi)
def test_existing_project_id(mock_projects_api, mock_id_exists, mock_valid_id):
    result = cli_types.existing_project_id('1')
    mock_valid_id.assert_called_once_with('1')
    mock_id_exists.assert_called_once_with(mock_projects_api, '1')
    assert result == '1'


@patch('pnc_cli.cli_types.valid_id')
@patch('pnc_cli.common.id_exists', return_value=False)
@patch('pnc_cli.cli_types.projects_api', autospec=ProjectsApi)
def test_existing_project_id_exception(mock_projects_api, mock_id_exists, mock_valid_id):
    with pytest.raises(argparse.ArgumentTypeError):
        cli_types.existing_project_id('1')
    mock_valid_id.assert_called_once_with('1')
    mock_id_exists.assert_called_once_with(mock_projects_api, '1')


@patch('pnc_cli.common.get_id_by_name', return_value='1')
@patch('pnc_cli.cli_types.projects_api', autospec=ProjectsApi)
def test_existing_project_name(mock_projects_api, mock_get_id_by_name):
    result = cli_types.existing_project_name('testerino')
    mock_get_id_by_name.assert_called_once_with(mock_projects_api, 'testerino')
    assert result == 'testerino'


@patch('pnc_cli.common.get_id_by_name', return_value=None)
@patch('pnc_cli.cli_types.projects_api', autospec=ProjectsApi)
def test_existing_project_name_exception(mock_projects_api, mock_get_id_by_name):
    with pytest.raises(argparse.ArgumentTypeError):
        cli_types.existing_project_name('testerino')
    mock_get_id_by_name.assert_called_once_with(mock_projects_api, 'testerino')


@patch('pnc_cli.common.get_id_by_name', return_value=None)
@patch('pnc_cli.cli_types.projects_api', autospec=ProjectsApi)
def test_unique_project_name(mock_projects_api, mock_get_id_by_name):
    result = cli_types.unique_project_name('testerino')
    mock_get_id_by_name.assert_called_once_with(mock_projects_api, 'testerino')
    assert result == 'testerino'


@patch('pnc_cli.common.get_id_by_name', return_value='1')
@patch('pnc_cli.cli_types.projects_api', autospec=ProjectsApi)
def test_unique_project_name_exception(mock_projects_api, mock_get_id_by_name):
    with pytest.raises(argparse.ArgumentTypeError):
        cli_types.unique_project_name('testerino')
    mock_get_id_by_name.assert_called_once_with(mock_projects_api, 'testerino')


# BuildConfigurationSetRecord type tests
@patch('pnc_cli.cli_types.valid_id')
@patch('pnc_cli.common.id_exists', return_value=True)
@patch('pnc_cli.cli_types.bcsr_api', autospec=BuildconfigsetrecordsApi)
def test_existing_bc_set_record(mock_bcsr_api, mock_id_exists, mock_valid_id):
    result = cli_types.existing_bc_set_record('1')
    mock_valid_id.assert_called_once_with('1')
    mock_id_exists.assert_called_once_with(mock_bcsr_api, '1')
    assert result == '1'


@patch('pnc_cli.cli_types.valid_id')
@patch('pnc_cli.common.id_exists', return_value=False)
@patch('pnc_cli.cli_types.bcsr_api', autospec=BuildconfigsetrecordsApi)
def test_existing_bc_set_record_exception(mock_bcsr_api, mock_id_exists, mock_valid_id):
    with pytest.raises(argparse.ArgumentTypeError):
        cli_types.existing_bc_set_record('1')
    mock_valid_id.assert_called_once_with('1')
    mock_id_exists.assert_called_once_with(mock_bcsr_api, '1')


# BuildRecord type tests
@patch('pnc_cli.cli_types.valid_id')
@patch('pnc_cli.common.id_exists', return_value=True)
@patch('pnc_cli.cli_types.records_api', autospec=BuildrecordsApi)
def test_existing_build_record(mock_records_api, mock_id_exists, mock_valid_id):
    result = cli_types.existing_build_record('1')
    mock_valid_id.assert_called_once_with('1')
    mock_id_exists.assert_called_once_with(mock_records_api, '1')
    assert result == '1'


@patch('pnc_cli.cli_types.valid_id')
@patch('pnc_cli.common.id_exists', return_value=False)
@patch('pnc_cli.cli_types.records_api', autospec=BuildrecordsApi)
def test_existing_build_record_exception(mock_records_api, mock_id_exists, mock_valid_id):
    with pytest.raises(argparse.ArgumentTypeError):
        cli_types.existing_build_record('1')
    mock_valid_id.assert_called_once_with('1')
    mock_id_exists.assert_called_once_with(mock_records_api, '1')


# License type tests
@patch('pnc_cli.cli_types.valid_id')
@patch('pnc_cli.common.id_exists', return_value=True)
@patch('pnc_cli.cli_types.licenses_api', autospec=LicensesApi)
def test_existing_license(mock_licenses_api, mock_id_exists, mock_valid_id):
    result = cli_types.existing_license('1')
    mock_valid_id.assert_called_once_with('1')
    mock_id_exists.assert_called_once_with(mock_licenses_api, '1')
    assert result == '1'


@patch('pnc_cli.cli_types.valid_id')
@patch('pnc_cli.common.id_exists', return_value=False)
@patch('pnc_cli.cli_types.licenses_api', autospec=LicensesApi)
def test_existing_license_exception(mock_licenses_api, mock_id_exists, mock_valid_id):
    with pytest.raises(argparse.ArgumentTypeError):
        cli_types.existing_license('1')
    mock_valid_id.assert_called_once_with('1')
    mock_id_exists.assert_called_once_with(mock_licenses_api, '1')


@patch('pnc_cli.cli_types.valid_id')
@patch('pnc_cli.common.id_exists', return_value=True)
@patch('pnc_cli.cli_types.running_api', autospec=RunningbuildrecordsApi)
def test_existing_running_build(mock_running_api, mock_id_exists, mock_valid_id):
    result = cli_types.existing_running_build(1)
    mock_valid_id.assert_called_once_with(1)
    mock_id_exists.assert_called_once_with(mock_running_api, 1)
    assert result == 1


@patch('pnc_cli.cli_types.valid_id')
@patch('pnc_cli.common.id_exists', return_value=False)
@patch('pnc_cli.cli_types.running_api', autospec=RunningbuildrecordsApi)
def test_existing_running_build_exception(mock_running_api, mock_id_exists, mock_valid_id):
    with pytest.raises(argparse.ArgumentTypeError):
        cli_types.existing_running_build(1)
    mock_valid_id.assert_called_once_with(1)
    mock_id_exists.assert_called_once_with(mock_running_api, 1)
