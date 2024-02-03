
resource "aws_security_group" "https-sg" {
  vpc_id      = local.vpc_id
  name        = local.https_sg
  description = "Security Group for endpoints - https traffic"
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allowing https traffic for specific subnet IPs ranges"
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allowing All Outbound Traffic"
  }

  tags = {
    "anycompany:cost-center" = "Accounting"
  }
}


resource "aws_security_group" "https-test" {
  vpc_id      = local.vpc_id
  name        = local.https_sg
  description = "Security Group for endpoints - https traffic"
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allowing https traffic for specific subnet IPs ranges"
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allowing All Outbound Traffic"
  }

  tags = {
    "anycompany:cost-center" = "Accounting"
  }
}
