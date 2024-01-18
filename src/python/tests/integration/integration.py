import os
import boto3
import time
import json

os.environ['AWS_DEFAULT_REGION'] = 'ap-south-1'


def create_parameters():
    ssm_client = boto3.client(
        'ssm', region_name=os.environ.get('SOURCE_REGION'))
    # Create parameters
    ssm_client.put_parameter(Name='/sample/parameter1',
                             Value='value1', Type='String', Overwrite=True)
    print("Parameters Created")


def validate_event_bridge_create_capture():
    start_time = time.time()
    logs_client = boto3.client(
        'logs', region_name=os.environ.get('SOURCE_REGION'))
    log_group_name = f'/aws/events/se-intelds-{os.environ.get(
        "EDH_ACC_NAME_SHORT")}-euwe1-parameter-replication-logs-{os.environ.get("ENV")}'
    parameter_name = '/sample/parameter1'

    try:
        while time.time() - start_time < 70:
            response = logs_client.describe_log_streams(
                logGroupName=log_group_name,
                descending=True,
                limit=50
            )

            log_streams = response['logStreams']
            latest_log_stream_name = max(log_streams, key=lambda x: x['lastIngestionTime'])[
                'logStreamName']

            response = logs_client.get_log_events(
                logGroupName=log_group_name,
                logStreamName=latest_log_stream_name,
                limit=1,
                startFromHead=True
            )
            if 'events' in response and response['events']:
                latest_event = response['events'][0]
                event_message = json.loads(latest_event['message'])

                if event_message['detail']['name'] == parameter_name and event_message['detail']['operation'] == "Create":
                    print("Validation successful: Event bridge captured 'Create' event")
                    return
            time.sleep(2)

        print("Validation failed: Event bridge failed to capture 'Create' event")

    except Exception as e:
        print(f"Error during validation: {e}")
        # Cleanup by deleting parameters if script fails
        delete_parameters()
        raise


def validate_secondary_region_create_parameter():
    start_time = time.time()
    ssm_client_secondary = boto3.client(
        'ssm', region_name=os.environ.get('DEST_REGION'))

    parameter_name = '/sample/parameter1'

    while time.time() - start_time < 70:
        try:
            parameter1_secondary = ssm_client_secondary.get_parameter(
                Name=parameter_name)

            if 'Value' in parameter1_secondary['Parameter']:
                assert parameter1_secondary['Parameter']['Value'] == 'value1'
                print("Validation successful: Parameter found in the secondary region.")
                return

        except ssm_client_secondary.exceptions.ParameterNotFound:
            pass

        time.sleep(2)

    print("Validation failed: Parameter not found in the secondary region.")


def update_parameters():
    ssm_client = boto3.client(
        'ssm', region_name=os.environ.get('SOURCE_REGION'))

    # Update parameters
    ssm_client.put_parameter(Name='/sample/parameter1',
                             Value='updated_value1', Type='String', Overwrite=True)

    print("Parameters Updated")


def validate_event_bridge_update_capture():
    start_time = time.time()
    logs_client = boto3.client(
        'logs', region_name=os.environ.get('SOURCE_REGION'))
    log_group_name = f'/aws/events/se-intelds-{os.environ.get(
        "EDH_ACC_NAME_SHORT")}-euwe1-parameter-replication-logs-{os.environ.get("ENV")}'
    parameter_name = '/sample/parameter1'

    try:
        while time.time() - start_time < 70:
            response = logs_client.describe_log_streams(
                logGroupName=log_group_name,
                descending=True,
                limit=50
            )

            log_streams = response['logStreams']
            latest_log_stream_name = max(log_streams, key=lambda x: x['lastIngestionTime'])[
                'logStreamName']

            response = logs_client.get_log_events(
                logGroupName=log_group_name,
                logStreamName=latest_log_stream_name,
                limit=1,
                startFromHead=True
            )
            if 'events' in response and response['events']:
                latest_event = response['events'][0]
                event_message = json.loads(latest_event['message'])

                if event_message['detail']['name'] == parameter_name and event_message['detail']['operation'] == "Update":
                    print("Validation successful: Event bridge captured 'Update' event")
                    return
            time.sleep(2)

        print("Validation failed: Event bridge failed to capture 'Update' event")

    except Exception as e:
        print(f"Error during validation: {e}")
        # Cleanup by deleting parameters if script fails
        delete_parameters()
        raise


def validate_secondary_region_update_parameter():
    start_time = time.time()
    ssm_client_secondary = boto3.client(
        'ssm', region_name=os.environ.get('DEST_REGION'))

    parameter_name = '/sample/parameter1'

    while time.time() - start_time < 70:
        try:
            parameter1_secondary = ssm_client_secondary.get_parameter(
                Name=parameter_name)

            if 'Value' in parameter1_secondary['Parameter']:
                assert parameter1_secondary['Parameter']['Value'] == 'updated_value1'
                print("Validation successful: Parameter found in the secondary region.")
                return

        except ssm_client_secondary.exceptions.ParameterNotFound:
            pass

        time.sleep(2)

    print("Validation failed: Parameter not found in the secondary region.")


def delete_parameters():
    ssm_client = boto3.client(
        'ssm', region_name=os.environ.get('SOURCE_REGION'))

    # Delete parameters
    ssm_client.delete_parameter(Name='/sample/parameter1')

    print("Parameters Deleted")


def validate_event_bridge_delete_capture():
    start_time = time.time()
    logs_client = boto3.client(
        'logs', region_name=os.environ.get('SOURCE_REGION'))
    log_group_name = f'/aws/events/se-intelds-{os.environ.get(
        "EDH_ACC_NAME_SHORT")}-euwe1-parameter-replication-logs-{os.environ.get("ENV")}'
    parameter_name = '/sample/parameter1'

    while time.time() - start_time < 70:
        response = logs_client.describe_log_streams(
            logGroupName=log_group_name,
            descending=True,
            limit=50
        )

        log_streams = response['logStreams']
        latest_log_stream_name = max(log_streams, key=lambda x: x['lastIngestionTime'])[
            'logStreamName']

        response = logs_client.get_log_events(
            logGroupName=log_group_name,
            logStreamName=latest_log_stream_name,
            limit=1,
            startFromHead=True
        )
        if 'events' in response and response['events']:
            latest_event = response['events'][0]
            event_message = json.loads(latest_event['message'])

            if event_message['detail']['name'] == parameter_name and event_message['detail']['operation'] == "Delete":
                print("Validation successful: Event bridge captured 'Delete' event")
                return
        time.sleep(2)

    print("Validation failed: Event bridge failed to capture 'Delete' event")


def validate_secondary_region_delete_parameter():
    start_time = time.time()
    ssm_client_secondary = boto3.client(
        'ssm', region_name=os.environ.get('DEST_REGION'))

    parameter_name = '/sample/parameter1'

    while time.time() - start_time < 70:
        try:
            parameter1_secondary = ssm_client_secondary.get_parameter(
                Name=parameter_name)

            time.sleep(2)  # Adjust the sleep duration based on your needs

        except ssm_client_secondary.exceptions.ParameterNotFound:
            print(
                "Validation successful: Parameter not found in the secondary region after delete.")
            return

    print("Validation failed: Parameter still found in the secondary region after delete.")


# Validating Create Operation
create_parameters()
validate_event_bridge_create_capture()
validate_secondary_region_create_parameter()

# Validating Update Operation
update_parameters()
validate_event_bridge_update_capture()
validate_secondary_region_update_parameter()

# Validating Delete Operation
delete_parameters()
validate_event_bridge_delete_capture()
validate_secondary_region_delete_parameter()
