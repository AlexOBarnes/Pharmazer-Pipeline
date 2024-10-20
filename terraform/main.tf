provider "aws" {
  region     = var.AWS_REGION
  access_key = var.AWS_ACCESS_KEY
  secret_key = var.AWS_SECRET_KEY
}

data "aws_vpc" "c13-vpc" {
  id = var.VPC_ID
}

data "aws_security_group" "c13-default-sg" {
  id = var.SECURITY_GROUP_ID
}

data "aws_subnet" "c13-public-subnet" {
  id = var.SUBNET_ID
}

data "aws_db_subnet_group" "public-subnet-group" {
    name = "c13-public-subnet-group"
}

data "aws_ecr_image" "pipeline-image" {
  repository_name = "c13-alex-pharma-pipeline"
  image_tag       = "latest"
}

data "aws_iam_role" "execution-role" {
  name = "ecsTaskExecutionRole"
}

data "aws_ecs_cluster" "c13-cluster" {
  cluster_name = "c13-ecs-cluster"
}

data  "aws_iam_policy_document" "schedule-permissions-policy" {
    statement {
        effect = "Allow"
        resources = [aws_ecs_task_definition.pipeline_task.arn]
        actions = ["ecs:RunTask"]
    }
    statement {
        effect = "Allow"
        resources = ["*"]
        actions = ["iam:PassRole"]
    }
    statement {
        effect = "Allow"
        resources = ["arn:aws:logs:*:*:*"]
        actions = ["logs:CreateLogStream","logs:PutLogEvents","logs:CreateLogGroup"]
    }
}

data  "aws_iam_policy_document" "schedule-trust-policy" {
    statement {
        effect = "Allow"
        principals {
            type        = "Service"
            identifiers = ["scheduler.amazonaws.com"]
        }
        actions = ["sts:AssumeRole"]
    }
}

resource "aws_ecs_task_definition" "pipeline_task" {
  family                   = "c13-alex-pharma-pipeline"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  execution_role_arn       = data.aws_iam_role.execution-role.arn
  cpu                      = 256
  memory                   = 512
  container_definitions = jsonencode([{
    name      = "c13-alex-pipeline-container"
    image     = data.aws_ecr_image.pipeline-image.image_uri
    essential = true
    portMappings = [{
      containerPort = 80
      hostPort      = 80
    }]
    environment = [
      {
        name  = "AWS_ACCESS_KEY"
        value = var.AWS_ACCESS_KEY
      },
      {
        name  = "AWS_SECRET_ACCESS_KEY"
        value = var.AWS_SECRET_KEY
      },
      {
        name  = "INPUTBUCKET"
        value = var.INPUTBUCKET
      },
      {
        name  = "OUTPUTBUCKET"
        value = var.OUTPUTBUCKET
      },
      {
        name  = "TO"
        value = var.TO
      },
      {
        name  = "FROM"
        value = var.FROM
      }
    ]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        awslogs-group         = "/ecs/c13-alex-truck-pipeline"
        mode                  = "non-blocking"
        awslogs-create-group  = "true"
        max-buffer-size       = "25m"
        awslogs-region        = "eu-west-2"
        awslogs-stream-prefix = "ecs"
      }
    }
  }])
}

resource "aws_cloudwatch_event_rule" "s3_event_rule" {
  name        = "c13-alex-s3-object-create-rule"
  description = "Triggered by S3 file uploads to c13/alex/ path"
  event_pattern = <<PATTERN
{
  "source": ["aws.s3"],
  "detail-type": ["AWS API Call via CloudTrail"],
  "detail": {
    "eventSource": ["s3.amazonaws.com"],
    "eventName": ["PutObject"],
    "requestParameters": {
      "bucketName": ["${var.INPUTBUCKET}"],
      "key": [{
        "prefix": "c13/alex/sjogren-data-"
      }]
    }
  }
}
PATTERN
}

resource "aws_cloudwatch_event_target" "ecs_target" {
  rule      = aws_cloudwatch_event_rule.s3_event_rule.name
  arn       = data.aws_ecs_cluster.c13-cluster.arn
  role_arn  = aws_iam_role.schedule-role.arn

  ecs_target {
    task_definition_arn = aws_ecs_task_definition.pipeline_task.arn
    launch_type         = "FARGATE"
    network_configuration {
      subnets         = [data.aws_subnet.c13-public-subnet.id]
      security_groups = [data.aws_security_group.c13-default-sg.id]
      assign_public_ip = true
    }
  }
}

resource "aws_iam_role" "schedule-role" {
  name               = "c13-alex-pipeline-scheduler-role"
  assume_role_policy = data.aws_iam_policy_document.schedule-trust-policy.json

  inline_policy {
    name   = "c13-alex-execution-policy"
    policy = data.aws_iam_policy_document.schedule-permissions-policy.json
  }
}

resource "aws_security_group" "rds_sg" {
  name        = "c13-alex-pubmed-db-sg"
  description = "Allow MySQL access from anywhere on port 3306"
  vpc_id      = data.aws_vpc.c13-vpc.id
  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "allow-mysql-public-access"
  }
}


resource "aws_db_instance" "mysql_db" {
  allocated_storage     = 20
  engine                = "mysql"
  engine_version        = "8.0"
  instance_class        = "db.t3.micro"
  db_subnet_group_name  = data.aws_db_subnet_group.public-subnet-group.name
  identifier            = "c13-alex-pubmed-db"
  username              = var.DB_USER
  password              = var.DB_PW             
  publicly_accessible   = true
  performance_insights_enabled = false
  skip_final_snapshot   = true
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  backup_retention_period   = 0
  delete_automated_backups  = true

  tags = {
    Name = "c13-alex-pubmed-db"
  }
}