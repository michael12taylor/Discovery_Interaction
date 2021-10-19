from dotenv import get_key
from ibm_watson import DiscoveryV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json

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

def get_character_passages(natural_language_query):
    try:
        response = discovery.query(
            environment_id = env_id,
            collection_id = col_id,
            natural_language_query = natural_language_query,
            passages = True,
            count = 25,
            highlight=True,
            passages_characters=500
        ).get_result()
        return response
    except ApiException as ex:
        print('Failure with status code: %d -> %s' % (ex.code, ex.message) )
        return None

def extract_passages(response):
    if not response is None:
        passages = response['passages']
        return passages
    print('ERROR: No response recieved')
    return None

def extract_character_data(response):
    passages = extract_passages(response)
    if passages is None:
        print('ERROR: No response recieved')
        return None
    data = []
    for passage in passages:
        doc_id = passage['document_id']
        pass_score = passage['passage_score']
        text = passage['passage_text']
        data.append( (doc_id, pass_score, text) )
    return data

def get_document_name(doc_id):
    doc_info = discovery.get_document_status(
        env_id, 
        col_id, 
        doc_id).get_result()
    if not 'filename' in doc_info.keys():
        print('ERROR: Document "%s" does not exist' % doc_id)
        return None
    return doc_info['filename']