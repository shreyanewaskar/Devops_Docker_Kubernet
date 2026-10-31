terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

data "aws_instance" "cloudcart_jenkins" {
  filter {
    name   = "instance-id"
    values = ["i-00374cc00b3720a2c"]
  }
}

output "cloudcart_jenkins_instance_id" {
  value = data.aws_instance.cloudcart_jenkins.id
}

output "cloudcart_jenkins_public_ip" {
  value = data.aws_instance.cloudcart_jenkins.public_ip
}
