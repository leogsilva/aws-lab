#!/bin/bash

PROFILE=$1
aws cloudformation deploy --profile $PROFILE --region us-east-1 --template-file cform/ec2-scheduler.output.template --stack-name tools-ec2-scheduler --parameter-overrides CustomTagName=scheduler:ec2-startstop Schedule=5minutes DefaultStartTime=1100 DefaultStopTime=2200 DefaultDaysActive=weekdays DynamoDBTableName=EC2-Scheduler DynamoDBTableNameState=EC2-Scheduler-State ReadCapacityUnits=1 WriteCapacityUnits=1 CloudWatchMetrics=Disabled SendAnonymousData=No --capabilities CAPABILITY_IAM
