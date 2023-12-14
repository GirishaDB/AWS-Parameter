

# variable "region" {
#   type        = string
#   description = "Primary AWS region"
#   default     = "euwe1"
# }

variable "platform_name" {
  type        = string
  description = "The name of the project"
  default     = "org"
}

# variable "account_id" {
#   type        = string
#   description = "AWS account where infrastructure will be deployed"
# }

variable "account_name" {
  type        = string
  description = "Name of the account"
  default     = "test"

}

# variable "build_role" {
#   type        = string
#   description = "Build role to be used on AWS provider"
# }

# variable "build_role_external_id" {
#   type        = string
#   sensitive   = true
#   description = "External ID used to assume the build role"
# }

variable "env" {
  type        = string
  description = "Name of the Environment"
  default     = "dev"
}



variable "lambda_function_name" {
  type        = string
  description = "Name of the lambda function"
  default     = "parameter-replication"

}

variable "access_key" {
  type        = string
  description = "aws access key"
}

variable "secret_key" {
  type        = string
  description = "aws secret key"
}
