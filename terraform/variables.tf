variable "AWS_REGION" {
    type = string
    default = "eu-west-2"
}

variable "AWS_ACCESS_KEY"{
    type = string
}

variable "AWS_SECRET_KEY" {
  type = string
}

variable "INPUTBUCKET" {
    type = string
}

variable "OUTPUTBUCKET" {
    type = string
}

variable "SECURITY_GROUP_ID" {
    type = string
}

variable "SUBNET_ID" {
    type = string
}

variable "IMAGE_URI" {
    type = string
}
variable "FROM" {
  type = string
}

variable "TO" {
    type = string
}

variable "VPC_ID"{
    type = string
}

variable DB_USER{
    type = string
}

variable DB_PW{
    type = string
}