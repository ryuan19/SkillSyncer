from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def encrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    return encrypted_data, iv

def decrypt_data(encrypted_data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted_data

# Original data to be encrypted
data = "Your data here"

print(f"Initial data: {data}")

data = data.encode()

# AES key (16 bytes for AES 128)
key = get_random_bytes(16)

# Encrypt the data
encrypted_data, iv = encrypt_data(data, key)
print(f"Encrypted data: {encrypted_data}")

# Decrypt the data
try:
    decrypted_data = decrypt_data(encrypted_data, key, iv)
    print(f"Decrypted data: {decrypted_data.decode()}")
except (ValueError, KeyError):
    print("Incorrect decryption")

# Verification
if decrypted_data == data:
    print("Verification successful: The data is identical")
else:
    print("Verification failed: The data is not identical")
