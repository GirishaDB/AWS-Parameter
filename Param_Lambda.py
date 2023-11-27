import json

import boto3
def lambda_handler(event):
    # Get the source and destination regions
    source_region = 'ap-south-1' 
    dest_region = 'us-east-1'  
    
    source_ssm_client = boto3.client('ssm', region_name=source_region)
    dest_ssm_client = boto3.client('ssm', region_name=dest_region)
    
    parameter_name = event['detail']['name']
    operation = event['detail']['operation']
    
    if operation in ['Create', 'Update']:
        # Get the value of the parameter from the source region
        response = source_ssm_client.get_parameter(Name=parameter_name, WithDecryption=True)
        parameter_value = response['Parameter']['Value']
        
        # Set the parameter in the destination region
        dest_ssm_client.put_parameter(Name=parameter_name, Value=parameter_value, Type='SecureString', Overwrite=True)
    
    elif operation == 'Delete':
         dest_ssm_client.delete_parameter(Name=parameter_name)
    
    return {
        'statusCode': 200,
        'body': 'Parameter replication successful!'
    }