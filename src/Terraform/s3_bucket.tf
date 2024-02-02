# resource "aws_s3_bucket" "this" {
#   bucket = var.bucket_name
#   tags   = merge({ "resourcename" = "${local.name}" }, local.tags)
# }

# locals {
#   name = "${var.project}-${var.prefix}"
#   tags = {
#     project   = var.project
#     createdon = timestamp()
#   }
# }


# # Tags
# variable "project" {
#   description = "name of project"
#   type        = string
#   default     = "demo"
# }

# variable "prefix" {
#   description = "prefix name"
#   type        = string
#   default     = "pref"
# }

# # Amazon S3
# variable "bucket_name" {
#   description = "name of s3 bucket"
#   type        = string
#   default     = null
# }
