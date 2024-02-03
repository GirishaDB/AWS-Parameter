
resource "aws_iam_role" "iam_for_lambda" {
  name               = join("-", [var.platform_name, var.account_name, "parameter-replication-role", var.env])
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_policy" "policy_for_lambda" {
  name   = join("-", [var.platform_name, var.account_name, "parameter-replication-policy", var.env])
  policy = data.aws_iam_policy_document.lambda_policy.json
}

resource "aws_iam_role_policy_attachment" "role_policy_attachment" {
  role       = aws_iam_role.iam_for_lambda.name
  policy_arn = aws_iam_policy.policy_for_lambda.arn
}

resource "aws_lambda_function" "parameter_replication" {
  description      = "Lambda function to replicate SSM paremeters between regions"
  depends_on       = [aws_iam_role_policy_attachment.role_policy_attachment]
  filename         = "${path.module}/../python/parameter_replication.zip"
  function_name    = local.lambda_function
  role             = aws_iam_role.iam_for_lambda.arn
  handler          = "parameter_replication.lambda_handler"
  runtime          = "python3.11"
  timeout          = 30
  source_code_hash = filebase64sha256("${path.module}/../python/parameter_replication.py")

  environment {
    variables = {
      SOURCE_REGION = var.source_region,
      DEST_REGION   = var.dest_region
    }
  }

}

resource "aws_lambda_permission" "allow_event_bridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.parameter_replication.arn
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.event_bridge.arn
}

resource "aws_cloudwatch_log_group" "log_group" {
  name              = "/aws/lambda/${local.lambda_function}"
  retention_in_days = 30
}

resource "aws_cloudwatch_event_rule" "event_bridge" {
  description = "Capture events of SSM parameters store"
  name        = local.event_bridge
  event_pattern = jsonencode({
    source      = ["aws.ssm"],
    detail-type = ["Parameter Store Change", "Parameter Store Policy Action"]
  })
}

resource "aws_cloudwatch_event_target" "event_bridge_target_lambda" {
  depends_on = [aws_lambda_function.parameter_replication]
  rule       = aws_cloudwatch_event_rule.event_bridge.name
  arn        = aws_lambda_function.parameter_replication.arn
}



#Cloud Watch log group
resource "aws_cloudwatch_log_group" "event_rule_log_group" {
  name              = "/aws/events/${join("-", [var.platform_name, var.account_name, var.region, "parameter-replication-logs", var.env])}"
  retention_in_days = 30
}

#Log Group Policy
data "aws_iam_policy_document" "log_group_policy" {
  statement {
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "logs:PutLogEventsBatch",
    ]

    resources = ["*"]

    principals {
      identifiers = ["events.amazonaws.com", "delivery.logs.amazonaws.com"]
      type        = "Service"
    }
  }
}

resource "aws_cloudwatch_log_resource_policy" "cloudwatch_log_policy" {
  depends_on      = [aws_cloudwatch_log_group.event_rule_log_group]
  policy_name     = join("-", [var.platform_name, var.account_name, "parameter-replication-log-group-policy", var.env])
  policy_document = data.aws_iam_policy_document.log_group_policy.json
}

#Attaching Log group to event bridge
resource "aws_cloudwatch_event_target" "event_bridge_target_logs" {
  depends_on = [aws_cloudwatch_log_group.event_rule_log_group]
  rule       = join("-", [var.platform_name, var.account_name, var.region, "parameter-replication-event-bridge", var.env])
  arn        = aws_cloudwatch_log_group.event_rule_log_group.arn
}


resource "aws_security_group" "https-todo" {

}

