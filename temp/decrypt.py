import json
from cryptography.fernet import Fernet
import base64
import hashlib
import os
def derive_key(passphrase: str) -> bytes:
    # Use SHA256 to derive a key
    key = hashlib.sha256(passphrase.encode()).digest()
    return base64.urlsafe_b64encode(key)

def decrypt_json(input_file: str, passphrase: str) -> dict:
    key = derive_key(passphrase)
    cipher = Fernet(key)
    
    # Read the encrypted file
    with open(input_file, "rb") as f:
        encrypted_data = f.read()
    print(os.listdir())
    # Decrypt the data
    decrypted_data = cipher.decrypt(encrypted_data).decode()
    if decrypted_data : print("Decryption completed.")
    # Convert the decrypted data to a Python dictionary
    return json.loads(decrypted_data)


