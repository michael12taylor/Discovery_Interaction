from typing import Collection
from dotenv import get_key
from ibm_watson import DiscoveryV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json
import sys

apikey = get_key('ibm-credentials.env', 'DISCOVERY_APIKEY')
url = get_key('ibm-credentials.env', 'DISCOVERY_URL')
env_id = '723f0839-4d67-4dc0-a42c-99a02be56223'

# ID of "WikiPages"
delete_col_id = '210d513f-405e-4c56-b949-fb4385daafae'

authenticator = IAMAuthenticator(apikey)
discovery = DiscoveryV1(
    version='2021-09-23',
    authenticator=authenticator
)

discovery.set_service_url(url)

try:
    print('Starting...')
    
    # Get the name of the collection and count of documents in it
    collection = discovery.get_collection(
        environment_id = env_id,
        collection_id = delete_col_id,
    ).get_result()

    # Confirm this is the collection to delete
    count_docs = collection['document_counts']['available']
    coll_name = collection['name']
    confirm = input(f"Delete all {count_docs} documents in the collection {coll_name}? (y/n): ")
    if confirm[0] != 'y':
        exit()

    # Get the docs to remove
    docs = discovery.query(
        environment_id = env_id,
        collection_id = delete_col_id,
        count = count_docs,
        return_ = "id"
    ).get_result()

    # Remove each by their ID
    for doc_remove_id in [docresult['id'] for docresult in docs['results']]:
        response = discovery.delete_document(
            environment_id = env_id,
            collection_id = delete_col_id,
            document_id = doc_remove_id
        )

except ApiException as ex:
    print('Failure with status code: %d -> %s' % (ex.code, ex.message) )