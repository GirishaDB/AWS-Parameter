# import boto3
# from moto import mock_ssm
# import pytest
# import os

# import sys

# sys.path.append('python')
# from parameter_replication import lambda_handler

# @mock_ssm
# def test_lambda_handler():
#     # Create mock SSM clients
#     source_region = os.environ.get('SOURCE_REGION')
#     dest_region = os.environ.get('DEST_REGION')
#     source_ssm_client = boto3.client('ssm', region_name=source_region)
#     dest_ssm_client = boto3.client('ssm', region_name=dest_region)
    
#     # Create test event
#     event = {
#         'detail': {
#             'name': '/example/parameter',
#             'operation': 'Create'
#         }
#     }
    
#     # Set up initial parameter in source region
#     source_ssm_client.put_parameter(
#         Name=event['detail']['name'],
#         Value='create-parameter',
#         Type='SecureString',
#         Overwrite=True
#     )
    
#     # Call the lambda_handler function
#     from parameter_replication import lambda_handler
#     result = lambda_handler(event, None)
    
#     # Assert the result
#     assert result == True
    
#     # Assert the parameter is created in the destination region
#     response = dest_ssm_client.get_parameter(Name=event['detail']['name'])
#     assert response['Parameter']['Value'].split(':')[-1] == 'create-parameter'

#     # Create test event for update
#     update_event = {
#         'detail': {
#             'name': '/example/parameter',
#             'operation': 'Update'
#         }
#     }
#     # Update the parameter in the source region
#     source_ssm_client.put_parameter(
#         Name=update_event['detail']['name'],
#         Value='updated-parameter',
#         Type='SecureString',
#         Overwrite=True
#     )
#     # Call the lambda_handler function for update event
#     result = lambda_handler(update_event, None)
#     # Assert the result for update event
#     assert result is True
#     # Assert the parameter is updated in the destination region
#     response = dest_ssm_client.get_parameter(Name=update_event['detail']['name'])
#     assert response['Parameter']['Value'].split(':')[-1] == 'updated-parameter'
    
    
#     # Cleanup - delete the parameter
#     dest_ssm_client.delete_parameter(Name=event['detail']['name'])
    
#     # Assert the parameter is deleted in the destination region
#     with pytest.raises(dest_ssm_client.exceptions.ParameterNotFound):
#         dest_ssm_client.get_parameter(Name=event['detail']['name'])