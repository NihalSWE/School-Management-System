# In backend/hash_utils.py
import hashlib

# --- THIS IS THE FIX ---
# We import the SPECIFIC hasher, not the general 'check_password'
from django.contrib.auth.hashers import PBKDF2PasswordHasher
# --- END OF FIX ---


# This key is 100% correct from your last step
CI_ENCRYPTION_KEY = "b10dfd85c165a1ec2411a7a6096947f6"


def make_ci_hash(password):
    """
    Creates a raw SHA-512 hash, just like CodeIgniter,
    using the application's encryption key as a salt.
    (This function is already correct)
    """
    if not CI_ENCRYPTION_KEY:
        raise ValueError("CI_ENCRYPTION_KEY in hash_utils.py is not set.")
        
    salted_password = password + CI_ENCRYPTION_KEY
    return hashlib.sha512(salted_password.encode('utf-8')).hexdigest()

def check_ci_hash(password, encoded):
    """
    "Smart" check that handles BOTH hash types.
    'password' is the raw password (e.g., "123")
    'encoded' is the hash from the DB
    """
    
    # 1. Check if it's a Django-style hash (pbkdf2...)
    # We also add a startswith check for safety
    if '$' in encoded and encoded.startswith('pbkdf2_sha256$'):
        # --- THIS IS THE FIX ---
        # We instantiate the specific hasher and call 'verify'
        hasher = PBKDF2PasswordHasher()
        try:
            return hasher.verify(password, encoded)
        except:
            # This will catch any errors if the hash is malformed
            return False
        # --- END OF FIX ---

    # 2. If not, assume it's a raw CodeIgniter SHA-512 hash
    try:
        return make_ci_hash(password) == encoded
    except ValueError:
        return False