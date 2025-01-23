import boto3
from app.config import settings

# DynamoDB
dynamodb = boto3.resource("dynamodb", region_name=settings.aws_region)
table = dynamodb.Table(settings.dynamodb_table)

# S3
s3_client = boto3.client("s3", region_name=settings.aws_region)
