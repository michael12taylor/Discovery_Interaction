from dotenv import get_key
from ibm_watson import DiscoveryV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json
import sys

apikey = get_key('ibm-credentials.env', 'DISCOVERY_APIKEY')
url = get_key('ibm-credentials.env', 'DISCOVERY_URL')
env_id = '723f0839-4d67-4dc0-a42c-99a02be56223'
col_id = '210d513f-405e-4c56-b949-fb4385daafae'

authenticator = IAMAuthenticator(apikey)
discovery = DiscoveryV1(
    version='2021-09-23',
    authenticator=authenticator
)

discovery.set_service_url(url)

try:
    print('Starting...')
    response = discovery.query(
        environment_id = env_id,
        collection_id = col_id,
        natural_language_query = 'My name is Sam',
        passages = True,
        count = 10,
        highlight=True,
        passages_characters=500
    ).get_result()
    print(json.dumps(response, indent=1))
except ApiException as ex:
    print('Failure with status code: %d -> %s' % (ex.code, ex.message) )