import sys
sys.path.insert(0, './lib')

import boto3
from twilio.rest import Client

# def lambda_handler():
def lambda_handler(event, context):
    session = boto3.session.Session(
        region_name='ap-southeast-2'
    )
    client = session.client('ssm')
    parameters = ['twilio-account-sid', 'twilio-auth-token']
    response = client.get_parameters(
        Names=parameters,
        WithDecryption=True
    )
    account_sid = next(param['Value'] for param in response['Parameters'] if param['Name'] == parameters[0])
    auth_token = next(param['Value'] for param in response['Parameters'] if param['Name'] == parameters[1])

    twilio_client = Client(account_sid, auth_token)
    twilio_client.calls.create(url="http://demo.twilio.com/docs/voice.xml",
                               to="+61404839210",
                               from_="+61404839210")

# if __name__ == "__main__":
#     lambda_handler()