from dotenv import get_key
from ibm_watson import DiscoveryV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json
import sys

apikey = get_key('ibm-credentials.env', 'DISCOVERY_APIKEY')
url = get_key('ibm-credentials.env', 'DISCOVERY_URL')

authenticator = IAMAuthenticator(apikey)
discovery = DiscoveryV1(
    version='2021-09-23',
    authenticator=authenticator
)

discovery.set_service_url(url)

try:
    print('Starting...')
    name = input('What is the name of the collection? ')
    description = input('what is the description of %s? ' % name)
    print('NAME: %s' % name)
    print('DESC: %s' % description)
    confirm = input('Create collection? <y/n> ')
    if confirm == 'y':
        response = discovery.create_collection(
            environment_id='723f0839-4d67-4dc0-a42c-99a02be56223',
            name=name,
            description=description
        ).get_result()
        print('\n\nNEW COLLECTION')
        print(json.dumps(response, indent=1))
        print('END COLLECTION\n\n')
except ApiException as ex:
    print('Failure with status code: %d -> %s' % (ex.code, ex.message) )