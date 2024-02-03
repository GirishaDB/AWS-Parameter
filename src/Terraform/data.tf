data "aws_region" "current" {}

data "aws_caller_identity" "current" {}

locals {
  aws_region      = data.aws_region.current.name
  account_id      = data.aws_caller_identity.current.account_id
  lambda_function = join("-", [var.platform_name, var.account_name, var.region, var.function_name, var.env])
  event_bridge    = join("-", [var.platform_name, var.account_name, var.region, "parameter-replication-event-bridge", var.env])
}

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
    resources = ["arn:aws:logs:${local.aws_region}:${local.account_id}:log-group:/aws/lambda/${local.lambda_function}"]
  }
  statement {
    sid    = "LogsCollection"
    effect = "Allow"
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]

    resources = ["arn:aws:logs:${local.aws_region}:${local.account_id}:log-group:/aws/lambda/${local.lambda_function}*"]
  }

  statement {
    sid     = "ParametersOperations"
    effect  = "Allow"
    actions = ["ssm:*"]
    # resources = ["arn:aws:ssm:${var.source_region}:${local.account_id}:parameter/*", "arn:aws:ssm:${var.dest_region}:${local.account_id}:parameter/*"]
    resources = ["*"]
  }
  statement {
    sid     = "EventBridgeActions"
    effect  = "Allow"
    actions = ["events:*"]
    # resources = ["arn:aws:events:${local.aws_region}:${local.account_id}:rule/${local.event_bridge}"]
    resources = ["*"]
  }
  statement {
    sid     = "InvokeFunction"
    effect  = "Allow"
    actions = ["lambda:InvokeFunction"]
    # resources = ["arn:aws:lambda:${local.aws_region}:${local.account_id}:function/${local.lambda_function}*"]
    resources = ["*"]
  }

}

data "archive_file" "python_file" {
  type        = "zip"
  source_file = "${path.module}/../python/parameter_replication.py"
  output_path = "${path.module}/../python/parameter_replication.zip"
}

