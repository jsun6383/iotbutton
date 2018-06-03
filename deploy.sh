#!/bin/bash -e

logger() {
    echo "INFO: $1"
}

[ -f iotbutton.zip ] && rm -f iotbutton.zip

zip -r 'iotbutton.zip' lib/ lambda_function.py

logger "uploading lambda to s3"
aws s3 cp iotbutton.zip s3://johns-iotbutton-lambda/iotbutton.zip

logger "validating cloudformation"
if aws --profile jsun --region ap-southeast-2 cloudformation validate-template --template-body file://iotbutton.yaml ; then
    logger "creating cloudformation stack..."
    aws --profile jsun --region ap-southeast-2 cloudformation update-stack --stack-name iotbutton --capabilities CAPABILITY_IAM --template-body file://iotbutton.yaml
else
    logger "cloudformation is invalid"
fi