
resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam-role-${var.lambda_function_name}"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}


resource "aws_iam_policy" "policy_for_lambda" {
  name   = "policy-${var.lambda_function_name}"
  policy = data.aws_iam_policy_document.lambda_policy.json
}

resource "aws_iam_role_policy_attachment" "role_policy_attachment" {
  role       = aws_iam_role.iam_for_lambda.name
  policy_arn = aws_iam_policy.policy_for_lambda.arn
}

#####
resource "aws_lambda_function" "parameter_replication" {
  filename      = "${path.module}/../python/parameter_replication.zip"
  function_name = join("-", [var.platform_name, var.account_name, var.lambda_function_name, var.env])
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "parameter_replication.lambda_handler"
  runtime       = "python3.12"
  depends_on    = [aws_iam_role_policy_attachment.role_policy_attachment]

  environment {
    variables = {
      SOURCE_REGION = var.source_region,
      DEST_REGION   = var.dest_region
    }
  }
}

resource "aws_cloudwatch_log_group" "log_group" {
  name              = "/aws/lambda/${aws_lambda_function.parameter_replication.function_name}"
  retention_in_days = 30
}
