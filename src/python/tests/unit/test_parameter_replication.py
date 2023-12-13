""" This module contains tests for the parameter_replication lambda_handler function."""
import pytest
from unittest.mock import MagicMock
from pytest_mock import mocker

import sys

sys.path.append('python')
from parameter_replication import lambda_handler
    
@pytest.fixture
def event():
    return {
        'detail': {
            'name': 'my_parameter',
            'operation': 'Create'
        }
    }


def test_lambda_handler_create(event, mocker):
    # Mock the AWS SDK clients
    source_ssm_client = MagicMock()
    dest_ssm_client = MagicMock()
    mocker.patch(
        'boto3.client',
        side_effect=[
            source_ssm_client,
            dest_ssm_client])
    # Define the expected response from the source SSM client
    source_response = {
        'Parameter': {
            'Value': 'my_parameter_value'
        }
    }
    source_ssm_client.get_parameter.return_value = source_response


def test_lambda_handler_update(event, mocker):
    # Mock the AWS SDK clients
    source_ssm_client = MagicMock()
    dest_ssm_client = MagicMock()
    mocker.patch(
        'boto3.client',
        side_effect=[
            source_ssm_client,
            dest_ssm_client])
    # Define the expected response from the source SSM client
    source_response = {
        'Parameter': {
            'Value': 'my_parameter_value'
        }
    }
    source_ssm_client.get_parameter.return_value = source_response
    # Execute the lambda_handler function
    result = lambda_handler(event, None)
    # Assert the expected results
    assert result
    # Assert the expected interactions with the AWS SDK clients
    source_ssm_client.get_parameter.assert_called_once_with(
        Name='my_parameter', WithDecryption=True)
    dest_ssm_client.put_parameter.assert_called_once_with(
        Name='my_parameter',
        Value='my_parameter_value',
        Type='SecureString',
        Overwrite=True)


def test_lambda_handler_delete(event, mocker):
    # Mock the AWS SDK clients
    source_ssm_client = MagicMock()
    dest_ssm_client = MagicMock()
    mocker.patch(
        'boto3.client',
        side_effect=[
            source_ssm_client,
            dest_ssm_client])
    # Execute the lambda_handler function with 'Delete' operation
    event['detail']['operation'] = 'Delete'
    result = lambda_handler(event, None)
    # Assert the expected results
    assert result
    # Assert the expected interactions with the AWS SDK clients
    dest_ssm_client.delete_parameter.assert_called_once_with(
        Name='my_parameter')


def test_lambda_handler_invalid_operation(event, mocker):
    # Mock the AWS SDK clients
    source_ssm_client = MagicMock()
    dest_ssm_client = MagicMock()
    mocker.patch(
        'boto3.client',
        side_effect=[
            source_ssm_client,
            dest_ssm_client])
    # Execute the lambda_handler function with an invalid operation
    event['detail']['operation'] = 'InvalidOperation'
    result = lambda_handler(event, None)
    # Assert the expected results
    assert result is None
    # Assert that no interactions occurred with the AWS SDK clients
    source_ssm_client.get_parameter.assert_not_called()
    dest_ssm_client.put_parameter.assert_not_called()
    dest_ssm_client.delete_parameter.assert_not_called()
