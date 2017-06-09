######################################################################################################################
#  Copyright 2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.                                           #
#                                                                                                                    #
#  Licensed under the Amazon Software License (the "License"). You may not use this file except in compliance        #
#  with the License. A copy of the License is located at                                                             #
#                                                                                                                    #
#      http://aws.amazon.com/asl/                                                                                    #
#                                                                                                                    #
#  or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES #
#  OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions    #
#  and limitations under the License.                                                                                #
######################################################################################################################


import boto3
import datetime
import json
from urllib2 import Request
from urllib2 import urlopen
from collections import Counter
from botocore.exceptions import ClientError

def putCloudWatchMetric(region, instance_id, instance_state):

    cw = boto3.client('cloudwatch')

    cw.put_metric_data(
        Namespace='EC2Scheduler',
        MetricData=[{
            'MetricName': instance_id,
            'Value': instance_state,

            'Unit': 'Count',
            'Dimensions': [
                {
                    'Name': 'Region',
                    'Value': region
                }
            ]
        }]

    )

def lambda_handler(event, context):

    print "Running EC2 Scheduler"

    ec2 = boto3.client('ec2')
    cf = boto3.client('cloudformation')
    autoscaling = boto3.client('autoscaling')
    dynamodb = boto3.resource('dynamodb')

    outputs = {}
    stack_name = context.invoked_function_arn.split(':')[6].rsplit('-', 2)[0]
    response = cf.describe_stacks(StackName=stack_name)
    for e in response['Stacks'][0]['Outputs']:
        outputs[e['OutputKey']] = e['OutputValue']
    ddbTableName = outputs['DDBTableName']
    ddbTableNameState = outputs['DDBTableNameState']
    awsRegions = ec2.describe_regions()['Regions']
    table = dynamodb.Table(ddbTableName)
    tableState = dynamodb.Table(ddbTableNameState)

    response = table.get_item(
        Key={
            'SolutionName': 'EC2Scheduler'
        }
    )
    item = response['Item']

    # Reading Default Values from DynamoDB
    customTagName = str(item['CustomTagName'])
    customTagLen = len(customTagName)
    defaultStartTime = str(item['DefaultStartTime'])
    defaultStopTime = str(item['DefaultStopTime'])
    defaultTimeZone = 'utc'
    defaultDaysActive = str(item['DefaultDaysActive'])
    sendData = str(item['SendAnonymousData']).lower()
    createMetrics = str(item['CloudWatchMetrics']).lower()
    UUID = str(item['UUID'])
    TimeNow = datetime.datetime.utcnow().isoformat()
    TimeStamp = str(TimeNow)

    # Declare Dicts
    regionDict = {}
    allRegionDict = {}
    regionsLabelDict = {}
    postDict = {}

    now = datetime.datetime.now().strftime("%H%M")
    nowMax = datetime.datetime.now() - datetime.timedelta(minutes=59)
    nowMax = nowMax.strftime("%H%M")
    nowDay = datetime.datetime.today().strftime("%a").lower()

    # evaluates auto scaling groups
    for index, g in enumerate(autoscaling.describe_auto_scaling_groups()['AutoScalingGroups']):
        tags = g['Tags']
        instances = g['Instances']
        desiredCapacity = g['DesiredCapacity']
        minCapacity = g['MinSize']
        maxCapacity = g['MaxSize']
        arn = g['AutoScalingGroupARN']
        itemfound = []
        print "Testing",arn
        try:
            resourceFound = tableState.get_item(
                Key={
                    'arn': arn
                }
            )
            itemfound = resourceFound['Item']
            print "Found state for",itemfound
        except ClientError as e:
            print(e.response['Error']['Message'])
        except KeyError:
            # key not found, time to save original values
            Item={
                'arn': arn,
                'DesiredCapacity': desiredCapacity,
                'MinSize': minCapacity,
                'MaxSize': maxCapacity
            }
            responsePut = tableState.put_item(
                Item=Item
            )
            itemFound = Item;

        for t in tags:
            print "tag", t['Key'][:customTagLen], "custom", customTagName
            if t['Key'][:customTagLen] == customTagName:
                ptag = t['Value'].split(";")

                # Split out Tag & Set Variables to default
                default1 = 'default'
                default2 = 'true'
                startTime = defaultStartTime
                stopTime = defaultStopTime
                timeZone = defaultTimeZone
                daysActive = defaultDaysActive
                # Parse tag-value
                if len(ptag) >= 1:
                    if ptag[0].lower() in (default1, default2):
                        startTime = defaultStartTime
                    else:
                        startTime = ptag[0]
                        stopTime = ptag[0]
                if len(ptag) >= 2:
                    stopTime = ptag[1]
                if len(ptag) >= 3:
                    timeZone = ptag[2].lower()
                if len(ptag) >= 4:
                    daysActive = ptag[3].lower()

                isActiveDay = False
                # Days Interpreter
                if daysActive == "all":
                    isActiveDay = True
                elif daysActive == "weekdays":
                    weekdays = ['mon', 'tue', 'wed', 'thu', 'fri']
                    if (nowDay in weekdays):
                        isActiveDay = True
                else:
                    daysActive = daysActive.split(",")
                    for d in daysActive:
                        if d.lower() == nowDay:
                            isActiveDay = True

                # Append to start list
                print "now",now,"nowMax",nowMax
                if startTime >= str(nowMax) and startTime <= str(now) and \
                        str(now) <= stopTime and isActiveDay == True and desiredCapacity == 0:
                    # time to start the auto scaling group
                    previousCapacity = int(itemfound['DesiredCapacity'])
                    previousMin = int(itemfound['MinSize'])
                    previousMax = int(itemfound['MaxSize'])
                    print "Starting autoscaling", arn, " MinSize", previousMin, " DesiredCapacity",previousCapacity,"MaxSize",previousMax
                    autoscaling.update_auto_scaling_group(
                        AutoScalingGroupName=g['AutoScalingGroupName'],
                        DesiredCapacity=previousCapacity,
                        MinSize=previousMin,
                        MaxSize=previousMax
                    )
                    print "Started autoscaling", arn, " MinSize", previousMin, " DesiredCapacity",previousCapacity
                # Append to stop list
                if stopTime >= str(nowMax) and stopTime <= str(now) and \
                        isActiveDay == True and desiredCapacity > 0:
                    # time to stop auto scaling group
                    print "Shutting down", arn
                    autoscaling.update_auto_scaling_group(
                        AutoScalingGroupName=g['AutoScalingGroupName'],
                        DesiredCapacity=0,
                        MinSize=0
                    )
                    print "Done shutdown for", arn

    for region in awsRegions:
        try:

            # Create connection to the EC2 using Boto3 resources interface
            ec2 = boto3.resource('ec2', region_name=region['RegionName'])

            awsregion = region['RegionName']

            # Declare Lists
            startList = []
            stopList = []
            runningStateList = []
            stoppedStateList = []

            # List all instances
            instances = ec2.instances.all()

            print "Creating", region['RegionName'], "instance lists..."

            for i in instances:
                if i.tags != None:
                    for t in i.tags:
                        if t['Key'][:customTagLen] == customTagName:

                            ptag = t['Value'].split(";")

                            # Split out Tag & Set Variables to default
                            default1 = 'default'
                            default2 = 'true'
                            startTime = defaultStartTime
                            stopTime = defaultStopTime
                            timeZone = defaultTimeZone
                            daysActive = defaultDaysActive
                            state = i.state['Name']
                            itype = i.instance_type

                            # Post current state of the instances
                            if createMetrics == 'enabled':
                                if state == "running":
                                    putCloudWatchMetric(region['RegionName'], i.instance_id, 1)
                                if state == "stopped":
                                    putCloudWatchMetric(region['RegionName'], i.instance_id, 0)

                            # Parse tag-value
                            if len(ptag) >= 1:
                                if ptag[0].lower() in (default1, default2):
                                    startTime = defaultStartTime
                                else:
                                    startTime = ptag[0]
                                    stopTime = ptag[0]
                            if len(ptag) >= 2:
                                stopTime = ptag[1]
                            if len(ptag) >= 3:
                                timeZone = ptag[2].lower()
                            if len(ptag) >= 4:
                                daysActive = ptag[3].lower()

                            isActiveDay = False

                            # Days Interpreter
                            if daysActive == "all":
                                isActiveDay = True
                            elif daysActive == "weekdays":
                                weekdays = ['mon', 'tue', 'wed', 'thu', 'fri']
                                if (nowDay in weekdays):
                                    isActiveDay = True
                            else:
                                daysActive = daysActive.split(",")
                                for d in daysActive:
                                    if d.lower() == nowDay:
                                        isActiveDay = True

                            # Append to start list
                            if startTime >= str(nowMax) and startTime <= str(now) and \
                                    isActiveDay == True and state == "stopped":
                                startList.append(i.instance_id)
                                print i.instance_id, " added to START list"
                                if createMetrics == 'enabled':
                                    putCloudWatchMetric(region['RegionName'], i.instance_id, 1)

                            # Append to stop list
                            if stopTime >= str(nowMax) and stopTime <= str(now) and \
                                    isActiveDay == True and state == "running":
                                stopList.append(i.instance_id)
                                print i.instance_id, " added to STOP list"
                                if createMetrics == 'enabled':
                                    putCloudWatchMetric(region['RegionName'], i.instance_id, 0)

                            if state == 'running':
                                runningStateList.append(itype)
                            if state == 'stopped':
                                stoppedStateList.append(itype)

            # Execute Start and Stop Commands
            if startList:
                print "Starting", len(startList), "instances", startList
                ec2.instances.filter(InstanceIds=startList).start()
            else:
                print "No Instances to Start"

            if stopList:
                print "Stopping", len(stopList) ,"instances", stopList
                ec2.instances.filter(InstanceIds=stopList).stop()
            else:
                print "No Instances to Stop"


            # Built payload for each region
            if sendData == "yes":
                countRunDict = {}
                typeRunDict = {}
                countStopDict = {}
                typeStopDict = {}
                runDictType = {}
                stopDictType = {}
                runDict = dict(Counter(runningStateList))
                for k, v in runDict.iteritems():
                    countRunDict['Count'] = v
                    typeRunDict[k] = countRunDict['Count']

                stopDict = dict(Counter(stoppedStateList))
                for k, v in stopDict.iteritems():
                    countStopDict['Count'] = v
                    typeStopDict[k] = countStopDict['Count']

                runDictType['instance_type'] = typeRunDict
                stopDictType['instance_type'] = typeStopDict

                typeStateSum = {}
                typeStateSum['running'] = runDictType
                typeStateSum['stopped'] = stopDictType
                StateSum = {}
                StateSum['instance_state'] = typeStateSum
                regionDict[awsregion] = StateSum
                allRegionDict.update(regionDict)

        except Exception as e:
            print ("Exception: "+str(e))
            continue

    # Build payload for the account
    if sendData == "yes":
        regionsLabelDict['regions'] = allRegionDict
        postDict['Data'] = regionsLabelDict
        postDict['TimeStamp'] = TimeStamp
        postDict['Solution'] = 'SO0002'
        postDict['UUID'] = UUID
        # API Gateway URL to make HTTP POST call
        url = 'https://metrics.awssolutionsbuilder.com/generic'
        data=json.dumps(postDict)
        headers = {'content-type': 'application/json'}
        req = Request(url, data, headers)
        rsp = urlopen(req)
        content = rsp.read()
        rsp_code = rsp.getcode()
        print ('Response Code: {}'.format(rsp_code))
