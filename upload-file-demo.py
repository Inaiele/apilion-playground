import requests
import argparse

BASE_URL='https://api.apillon.io/storage/buckets'
BUCKET_UID='MY-BACKET-UID'
API_KEY='MY APY KEY IN BASE64'

headers = {
    "Authorization": f"{API_KEY}",
    "Content-Type": "application/json"
}

def upload_to_bucket(bucket_uuid, file_name, file_path):
    data = {
        "files": [{
          "fileName": file_name,
          "contentType": "image/jpeg"
        }]
    }
    print("Uploading file...")
    response = requests.post(f"{BASE_URL}/{bucket_uuid}/upload", headers=headers, json=data)
    upload_response_json = response.json()['data']

    file_url = next(file["url"] for file in upload_response_json["files"] if file["fileName"] == file_name)

    with open(file_path, 'rb') as file:
        file_content = file.read()
        requests.put(file_url, data=file_content)

    requests.post(f"{BASE_URL}/{bucket_uuid}/upload/{upload_response_json['sessionUuid']}/end", headers=headers)
    print("File uploaded successfully!")

def main():
    parser = argparse.ArgumentParser() 
    parser.add_argument('--file_path', type=str, required=True)
    parser.add_argument('--file_name', type=str, required=True)
    args = parser.parse_args()
    upload_to_bucket(BUCKET_UID, args.file_name, args.file_path)

if __name__ == '__main__':
    main()