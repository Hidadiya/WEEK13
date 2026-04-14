import hashlib
import os
import json
import time
from urllib import response
import requests
from requests.auth import HTTPBasicAuth

# 🔐 Jira credentials
JIRA_URL = "https://hida12.atlassian.net"
EMAIL = "yazra3119@gmail.com"
API_TOKEN = "ATATT3xFfGF0kA44Y4LIGc9CTv9-BE1pYtWaA_oMDwEL8G2cW1KYitcwW1wU3HAIuxOJyjmsOidqfLmfImx2CO7VUVGcz_lR-3lUlLFns6jf226djLMV6eX9dkjKCR-0dAHJUawf6rK2hsyaQDqJYEX4KYEeTb_ch5e3k89IY4f0OhGXnttL0d0=F4447DC0"
PROJECT_KEY = "KAN"

def create_jira_ticket(title, description):
    url = f"{JIRA_URL}/rest/api/3/issue"

    auth = HTTPBasicAuth(EMAIL, API_TOKEN)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "fields": {
            "project": {
                "key": PROJECT_KEY
            },
            "summary": title,
            "description": {
    "type": "doc",
    "version": 1,
    "content": [
        {
            "type": "paragraph",
            "content": [
                {
                    "type": "text",
                    "text": description
                }
            ]
        }
    ]
},
            "issuetype": {
                "name": "Task"
            }
        }
    }

    response = requests.post(url, json=payload, headers=headers, auth=auth)
    
    print("Status Code:", response.status_code)
    print("Response:", response.text)

    if response.status_code == 201:
        print("✅ Jira ticket created successfully!")
    else:
        print("❌ Failed to create Jira ticket")
        print(response.text)

# Testing jira

# create_jira_ticket(
#     "TEST FROM PYTHON",
#     "This is a test ticket"
# )
HASH_FILE = "hash_values_for_periodic_with_jira.json"
INTERVAL = 20   # ⏱️ 1 hour (3600 seconds)


#  Calculate hash
def calculate_hash(file_path):
    hash_obj = hashlib.sha256()
    
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    
    except Exception as e:
        print(f"Error: {file_path}: {e}")
        return None


#  Generate hashes
def generate_hashes(folder_path):
    hash_dict = {}
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file == HASH_FILE:
                continue

            file_path = os.path.join(root, file)
            file_hash = calculate_hash(file_path)

            if file_hash:
                hash_dict[file_path] = file_hash
                
    return hash_dict


#  Save hashes
def save_hashes(hashes):
    with open(HASH_FILE, 'w') as f:
        json.dump(hashes, f, indent=4)


#  Load hashes
def load_hashes():
    if not os.path.exists(HASH_FILE):
        return {}
    
    with open(HASH_FILE, 'r') as f:
        return json.load(f)


#  Compare hashes
def compare_hashes(old, new):

    for file in old:
        if file in new and old[file] != new[file]:
            print(f"❗ Modified: {file}")
            create_jira_ticket(
                "File Modified Alert",
                f"File modified: {file}"
            )

    for file in old:
        if file not in new:
            print(f"❌ Deleted: {file}")
            create_jira_ticket(
                "File Deleted Alert",
                f"File deleted: {file}"
            )

    for file in new:
        if file not in old:
            print(f"➕ New file: {file}")
            create_jira_ticket(
                "New File Detected",
                f"New file created: {file}"
            )


# 🚀 Main Monitoring Loop
if __name__ == "__main__":
    print("------!!!!!! File Integrity Monitor -----!!\n")

    folder_path = input("Enter folder path to monitor: ")

    if not os.path.exists(folder_path):
        print("❌ Invalid folder path!")
        exit()

    print("\n ----------- Monitoring started... ---------\n")

    try:
        while True:
            old_hashes = load_hashes()
            new_hashes = generate_hashes(folder_path)

            if not old_hashes:
                print("📌 Creating baseline...")
            else:
                compare_hashes(old_hashes, new_hashes)

            save_hashes(new_hashes)

            print(f"\n⏳ Waiting {INTERVAL} seconds...\n")
            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user. Exiting safely...")