import json
from cryptography.fernet import Fernet
import base64
import hashlib


def derive_key(passphrase: str) -> bytes:
    # Use SHA256 to derive a key
    key = hashlib.sha256(passphrase.encode()).digest()
    return base64.urlsafe_b64encode(key)


def encrypt_json(input_file: str, output_file: str, passphrase: str):
    key = derive_key(passphrase)
    cipher = Fernet(key)
    
    # Read the JSON file
    with open(input_file, "r") as f:
        data = f.read()
    
    # Encrypt the JSON data
    encrypted_data = cipher.encrypt(data.encode())
    
    # Save the encrypted data to the output file
    with open(output_file, "wb") as f:
        f.write(encrypted_data)
    
    print(f"Encrypted data saved to {output_file}")




# Example Usage
passphrase = "myApp101!"  # Replace with your passphrase
encrypt_json("token.json", "encrypted_data.json", passphrase)
