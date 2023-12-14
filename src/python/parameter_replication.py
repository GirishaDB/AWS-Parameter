""" This module is to replicate SSM paremeters from primary to secondary region as part of DR solution """
import boto3
import os


def lambda_handler(event, context):
    """ AWS Lambda function to handle parameter replication between regions """
    # Get the source and destination regions
    source_region = os.environ.get('SOURCE_REGION')
    dest_region = os.environ.get('DEST_REGION')
    source_short_name = 'apso1'
    dest_short_name = 'usea1'
    # Initialize AWS SDK clients for Parameter Store in both regions
    source_ssm_client = boto3.client('ssm', region_name=source_region)
    dest_ssm_client = boto3.client('ssm', region_name=dest_region)
    # Get the parameter details from the event
    parameter_name = event['detail']['name']
    operation = event['detail']['operation']
    # Handle create or update operations
    if operation in ['Create', 'Update']:
        try:
            response = source_ssm_client.get_parameter(
                Name=parameter_name, WithDecryption=True)
            parameter_value = response['Parameter']['Value']
            # Update region name in parameter path if present
            if source_short_name in parameter_name:
                parameter_name = parameter_name.replace(
                    source_short_name, dest_short_name)
            # Set the parameter in the destination region
            dest_ssm_client.put_parameter(
                Name=parameter_name,
                Value=parameter_value,
                Type='SecureString',
                Overwrite=True)
            print("Successful Operation:", operation)
            return True
        except Exception as e:
            print(f"Error: {type(e).__name__}, Message: {str(e)}")

    # Handle delete operation
    elif operation == 'Delete':
        # Update region name in parameter path if present
        try:
            if source_short_name in parameter_name:
                parameter_name = parameter_name.replace(
                    source_short_name, dest_short_name)
            # Delete the parameter in the destination region
            dest_ssm_client.delete_parameter(Name=parameter_name)
            print("Successful Operation:", operation)
            return True
        except Exception as e:
            print(f"Error: {type(e).__name__}, Message: {str(e)}")
