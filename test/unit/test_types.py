import argparse

import pytest
from mock import patch

import pnc_cli.types as types
# create_autospec dud import
from pnc_cli.swagger_client import BuildconfigurationsApi

__author__ = 'thauser'


# Common validation tests
def test_valid_id():
    result = types.valid_id('1')
    assert result == '1'


def test_valid_id_exception():
    with pytest.raises(argparse.ArgumentTypeError):
        types.valid_id('-1000')


def test_valid_date():
    result = types.valid_date('2015-06-01')
    assert result == '2015-06-01'


def test_valid_date_exception():
    with pytest.raises(argparse.ArgumentTypeError):
        types.valid_date('06-01-1989')


def test_valid_url():
    result = types.valid_url("http://www.tomhauser.com")
    assert result == 'http://www.tomhauser.com'


def test_valid_url_exception():
    with pytest.raises(argparse.ArgumentTypeError):
        types.valid_url('httpzzz://localhost:8080')


# BuildConfiguration tests

def test_valid_bc_name():
    result = types.valid_bc_name('test')
    assert result == 'test'


def test_valid_bc_name_exception():
    with pytest.raises(argparse.ArgumentTypeError):
        types.valid_bc_name("invalid #@)H*! name")


@patch('pnc_cli.common.get_id_by_name', return_value=None)
@patch('pnc_cli.types.configs_api', autospec=BuildconfigurationsApi)
def test_unique_bc_name(mock_configs_api, mock_get_id_by_name):
    result = types.unique_bc_name('test')
    mock_get_id_by_name.assert_called_once_with(mock_configs_api, 'test')
    assert result == 'test'


@patch('pnc_cli.common.get_id_by_name', return_value=1)
@patch('pnc_cli.types.configs_api', autospec=BuildconfigurationsApi)
def test_unique_bc_name_exception(mock_configs_api, mock_get_id_by_name):
    with pytest.raises(argparse.ArgumentTypeError):
        types.unique_bc_name('non-unique')
    mock_get_id_by_name.assert_called_once_with(mock_configs_api, 'non-unique')


@patch('pnc_cli.types.unique_bc_name', return_value='test')
@patch('pnc_cli.types.valid_bc_name', return_value='test')
def test_valid_unique_bc_name(mock_valid_bc_name, mock_unique_bc_name):
    result = types.valid_unique_bc_name('test')
    mock_unique_bc_name.assert_called_once_with('test')
    mock_valid_bc_name.assert_called_once_with('test')
    assert result == 'test'


def test_valid_unique_bc_name_exception():
    with pytest.raises(argparse.ArgumentTypeError):
        types.valid_unique_bc_name("invalid #@)H*! name")


@patch('pnc_cli.types.valid_bc_name')
@patch('pnc_cli.common.get_id_by_name', return_value=1)
@patch('pnc_cli.types.configs_api', autospec=BuildconfigurationsApi)
def test_existing_bc_name(mock_configs_api, mock_get_id_by_name, mock_valid_bc_name):
    result = types.existing_bc_name('test')
    mock_valid_bc_name.assert_called_once_with('test')
    mock_get_id_by_name.assert_called_once_with(mock_configs_api, 'test')
    assert result == 'test'


@patch('pnc_cli.types.valid_bc_name')
@patch('pnc_cli.common.get_id_by_name', return_value=None)
@patch('pnc_cli.types.configs_api', autospec=BuildconfigurationsApi)
def test_existing_bc_name_exception(mock_configs_api, mock_get_id_by_name, mock_valid_bc_name):
    with pytest.raises(argparse.ArgumentTypeError):
        types.existing_bc_name('test')
    mock_valid_bc_name.assert_called_once_with('test')
    mock_get_id_by_name.assert_called_once_with(mock_configs_api, 'test')


@patch('pnc_cli.types.valid_id')
@patch('pnc_cli.common.id_exists', return_value=True)
@patch('pnc_cli.types.configs_api', autospec=BuildconfigurationsApi)
def test_existing_bc_id(mock_configs_api, mock_id_exists, mock_valid_id):
    result = types.existing_bc_id('1')
    mock_valid_id.assert_called_once_with('1')
    mock_id_exists.assert_called_once_with(mock_configs_api, '1')
    assert result == '1'


@patch('pnc_cli.types.valid_id')
@patch('pnc_cli.common.id_exists', return_value=False)
@patch('pnc_cli.types.configs_api', autospec=BuildconfigurationsApi)
def test_existing_bc_id_exception(mock_configs_api, mock_id_exists, mock_valid_id):
    with pytest.raises(argparse.ArgumentTypeError):
        types.existing_bc_id('1')
    mock_valid_id.assert_called_once_with('1')
    mock_id_exists.assert_called_once_with(mock_configs_api, '1')


# Product type tests
@patch('pnc_cli.types.valid_id')
@patch('pnc_cli.common.id_exists', return_value=True)
@patch('pnc_cli.types.products_api', autospec=BuildconfigurationsApi)
def test_existing_product_id(mock_products_api, mock_id_exists, mock_valid_id):
    result = types.existing_product_id('1')
    mock_valid_id.assert_called_once_with('1')
    mock_id_exists.assert_called_once_with(mock_products_api, '1')
    assert result == '1'


@patch('pnc_cli.types.valid_id')
@patch('pnc_cli.common.id_exists', return_value=False)
@patch('pnc_cli.types.products_api', autospec=BuildconfigurationsApi)
def test_existing_product_id_exception(mock_products_api, mock_id_exists, mock_valid_id):
    with pytest.raises(argparse.ArgumentTypeError):
        types.existing_product_id('1')
    mock_valid_id.assert_called_once_with('1')
    mock_id_exists.assert_called_once_with(mock_products_api, '1')


@patch('pnc_cli.common.get_id_by_name', return_value=1)
@patch('pnc_cli.types.products_api', autospec=BuildconfigurationsApi)
def test_existing_product_name(mock_products_api, mock_get_id_by_name):
    result = types.existing_product_name('test')
    mock_get_id_by_name.assert_called_once_with(mock_products_api, 'test')
    assert result == 'test'


@patch('pnc_cli.common.get_id_by_name', return_value=None)
@patch('pnc_cli.types.products_api', autospec=BuildconfigurationsApi)
def test_existing_product_name_exception(mock_products_api, mock_get_id_by_name):
    with pytest.raises(argparse.ArgumentTypeError):
        types.existing_product_name('test')
    mock_get_id_by_name.assert_called_once_with(mock_products_api, 'test')
