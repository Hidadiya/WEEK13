import hashlib
import os
import json
import time

HASH_FILE = "hash_values_for_periodic.json"
INTERVAL = 10   # ⏱️ 1 hour (3600 seconds)


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
    print("\n🔍 Checking changes...\n")

    # Modified
    for file in old:
        if file in new:
            if old[file] != new[file]:
                print(f"❗ Modified: {file}")

    # Deleted
    for file in old:
        if file not in new:
            print(f"❌ Deleted: {file}")

    # New
    for file in new:
        if file not in old:
            print(f"➕ New file: {file}")


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