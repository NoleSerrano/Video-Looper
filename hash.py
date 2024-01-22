import hashlib
import os

def calculate_file_hash(file_path, hash_algorithm="sha256", chunk_size=8192):
    hasher = hashlib.new(hash_algorithm)
    with open(file_path, "rb") as file:
        while chunk := file.read(chunk_size):
            hasher.update(chunk)
    return hasher.hexdigest()

def calculate_hashes_in_folder(folder_path, file_extension=".mp4"):
    file_hashes = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(file_extension):
            file_path = os.path.join(folder_path, filename)
            file_hash = calculate_file_hash(file_path)
            file_hashes[filename] = file_hash
    return file_hashes

if __name__ == "__main__":
    current_folder = os.path.dirname(os.path.abspath(__file__))
    hashes = calculate_hashes_in_folder(current_folder)

    headers = ["Video File", "Hash"]
    print(f"{headers[0]:<30}| {headers[1]}")
    print('-' * 50)

    for filename, file_hash in hashes.items():
        print(f"{filename:<30}| {file_hash}")
