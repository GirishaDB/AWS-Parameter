data "aws_region" "current" {}

data "aws_caller_identity" "current" {}

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

data "aws_iam_policy_document" "lambda_policy" {

  statement {
    sid       = "CreateLogGroup"
    effect    = "Allow"
    actions   = ["logs:CreateLogGroup"]
    resources = ["arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:*"]
  }
  statement {
    sid    = "LogsCollection"
    effect = "Allow"
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]

    resources = ["arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${aws_lambda_function.parameter_replication.function_name}:*"]
  }

  statement {
    sid    = "ParametersOperations"
    effect = "Allow"
    actions = [
      "ssm:GetParameter",
      "ssm:PutParameter",
      "ssm:DeleteParameter"
    ]
    resources = ["arn:aws:ssm:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:parameter/*"]
  }
  statement {
    sid     = "EventBridgeActions"
    effect  = "Allow"
    actions = ["events:*"]
    resources = ["arn:aws:events:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:rule/*",
    "arn:aws:events:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:event-bus/*"]
  }
  statement {
    sid       = "IAMCreateServiceLinkedRoleForApiDestinations"
    effect    = "Allow"
    actions   = ["iam:CreateServiceLinkedRole"]
    resources = ["arn:aws:iam::*:role/aws-service-role/AmazonEventBridgeApiDestinationsServiceRolePolicy"]
    condition {
      test     = "StringEquals"
      variable = "iam:AWSServiceName"
      values   = ["apidestinations.events.amazonaws.com"]
    }
  }
}


data "archive_file" "python_file" {
  type        = "zip"
  source_dir  = "${path.module}/../python/"
  output_path = "${path.module}/../python/parameter_replication.zip"
}
