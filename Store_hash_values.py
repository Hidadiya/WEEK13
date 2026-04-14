import hashlib
import os
import json

#file to save the hash values
HASH_FILE = "hash_values.json"

#calculating the hash value of a file using SHA-256 algorithm
def calculate_hash(file_path):
    hash_obj = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    
    except Exception as e:
        print(f"Error calculating hash for {file_path}: {e}")
        return None


#generating hash values for all files in the specified folder and its subfolders
def generate_hashes(folder_path):
    hash_dict = {}
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)

            # Skip JSON file itself
            if file == HASH_FILE:
                continue
            
            file_hash = calculate_hash(file_path)
            if file_hash:
                hash_dict[file_path] = file_hash
                
    return hash_dict


#saving the hash values to a JSON file
def save_hashes(hashes):
    with open(HASH_FILE, 'w') as json_file:
        json.dump(hashes, json_file, indent=4)


# Main function to execute the file integrity monitoring process
if __name__ == "__main__":
    print("=== File Integrity Monitor ===\n")

    folder_path = input("Enter folder path to monitor: ")

    if not os.path.exists(folder_path):
        print("❌ Invalid folder path!")
        exit()

    print("\nScanning folder...\n")

    hashes = generate_hashes(folder_path)

    save_hashes(hashes)

    print(f"✅ {len(hashes)} files hashed and stored successfully!")