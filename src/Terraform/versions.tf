# Specify which versions of terraform and providers to use
/*
terraform {
  required_version = "~> 1.6.2"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.20.1"
    }
  }
}

provider "aws" {
  # region = var.aws_region
  assume_role {
    role_arn    = var.build_role
    external_id = var.build_role_external_id
  }

  default_tags {
    tags = {
      ENV              = var.env
      CC               = "FR012121"
      FINID            = "1607"
      Team             = "UrbanIntelDS_DCS"
      TerraformManaged = true
    }
  }
}
*/
