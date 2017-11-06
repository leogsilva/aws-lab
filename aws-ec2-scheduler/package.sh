#!/bin/bash

PROFILE=$1
BUCKET_NAME=$2
aws cloudformation package --profile $PROFILE --region us-east-1 --s3-bucket $BUCKET_NAME --template-file cform/ec2-scheduler.template --output-template-file cform/ec2-scheduler.output.template
