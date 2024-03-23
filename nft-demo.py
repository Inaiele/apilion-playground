import requests
import json
from http import HTTPStatus

BASE_URL='https://api.apillon.io/nfts/collections'
WALLET='0xXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
API_KEY='Basic XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'


headers = {
    'Authorization': f'{API_KEY}',
    'Content-Type': 'application/json'
}

def pretty_print(response : requests.Response):
    print(json.dumps(response.json()['data'], indent=4))


def check_response(response : requests.Response):
    if response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
        pretty_print(response)
    else:
        print("Response status code is not good:", response.status_code)
        print(f"Error: {response.text}")
        raise Exception

def get_collection(uuid):
    print(f"Getting collection {uuid}...")
    response = requests.get(f"{BASE_URL}/{uuid}", headers=headers)
    check_response(response)

def list_collections():
    print("Listing collections...")
    response = requests.get(BASE_URL, headers=headers)
    check_response(response)

def list_collection_transactions(uuid):
    print(f"Listing transactions for collection {uuid}...")
    response = requests.get(f"{BASE_URL}/{uuid}/transactions", headers=headers)
    check_response(response)

def create_collection(collection_data):
    print("Creating new collection...")
    response = requests.post(BASE_URL, headers=headers, json=collection_data)
    check_response(response)
    # print(response.json())
    collection_uuid = response.json()["data"]["collectionUuid"]
    print(f"New collection with UUID {collection_uuid} created successfully!")
    return collection_uuid

def mint_nft(collection_uuid, mint_data):
    print(f"Minting NFT for collection {collection_uuid}...")
    response = requests.post(f"{BASE_URL}/{collection_uuid}/mint", headers=headers, json=mint_data)
    print(response.json())
    if response.status_code == 201:
        print("NFT minted successfully!")
    else:
        print("Failed to mint NFT.")


def main():
    collection_data = {
        "chain": 1287, 
        "collectionType": 1, 
        "name": 'My NFT test API demo',
        "description": 'Test NFT collection',
        "symbol": 'SPCE',
        "royaltiesFees": 0,
        "royaltiesAddress": f'{WALLET}',
        "baseUri": 'www.my-test-api-nft-1.io',
        "baseExtension": '1.json',
        "maxSupply": 100,
        "isRevokable": False,
        "isSoulbound": False,
        "drop": True,
        "dropStart": 1687251003,
        "dropPrice": 0.1,
        "dropReserve": 5
    }

    mint_data = {
        'receivingAddress': f'{WALLET}',
        'quantity': 1
    }
    
    collection_uuid = create_collection(collection_data)
    list_collections()
    get_collection(collection_uuid)
    list_collection_transactions(collection_uuid)
    mint_nft(collection_uuid, mint_data)

if __name__ == '__main__':
    main()