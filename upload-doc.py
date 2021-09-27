from dotenv import get_key
from ibm_watson import DiscoveryV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json
import sys

apikey = get_key('ibm-credentials.env', 'DISCOVERY_APIKEY')
url = get_key('ibm-credentials.env', 'DISCOVERY_URL')
env_id = '723f0839-4d67-4dc0-a42c-99a02be56223'
col_id = 'fca067e8-358c-45d7-b23b-3da88c70b10e'

authenticator = IAMAuthenticator(apikey)
discovery = DiscoveryV1(
    version='2021-09-23',
    authenticator=authenticator
)

discovery.set_service_url(url)

try:
    print('Starting...')
    file_name = sys.argv[1]
    print('FILE: %s' % file_name)
    confirm = input('Upload this document? <y/n> ')
    if confirm == 'y':
        with open(file_name) as f:
            add_doc = discovery.add_document(
                env_id, 
                col_id,
                file=f).get_result()
        print(json.dumps(add_doc, indent=1))
except ApiException as ex:
    print('Failure with status code: %d -> %s' % (ex.code, ex.message) )