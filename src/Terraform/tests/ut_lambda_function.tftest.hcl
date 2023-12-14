provider "aws" {
  region = "eu-west-1"
}

#Global Variables
variables {
  lambda_function_name = "parameter-replication"
}


#unit test for lambda function

run "lambda_function_is_created" {
  command = plan
  assert {
    condition     = aws_lambda_function.parameter_replication.function_name == "se-intelds-dih-${var.lambda_function_name}-dev"
    error_message = "Lambda function name did not match as expected"
  }

  
  assert {
    condition     = aws_lambda_function.parameter_replication.handler == "parameter_replication.lambda_handler"
    error_message = "Lambda Handler is not mentioned as expected"
  }

  assert {
    condition     = aws_lambda_function.parameter_replication.runtime == "python3.12"
    error_message = "Python runtime did not meet the expected version python3.12"
  }
}

run "lambda_iam_role_and_policy" {
  command = plan
  assert {
    condition     = aws_iam_role.iam_for_lambda.name == "iam-role-${var.lambda_function_name}"
    error_message = "IAM role name did not match as expected"
  }

  assert {
    condition     = aws_iam_policy.policy_for_lambda.name == "policy-${var.lambda_function_name}"
    error_message = "IAM policy did not match as expected"
  }
}


run "cloud_watch_log_group_is_created" {
  command = plan
  assert {
    condition     = aws_cloudwatch_log_group.log_group.name == "/aws/lambda/${var.lambda_function_name}"
    error_message = "Log Group path/name did not match as expected"
  }

  assert {
    condition     = aws_cloudwatch_log_group.log_group.retention_in_days == 30
    error_message = "retention days did not meet the expected number 30"
  }
}
