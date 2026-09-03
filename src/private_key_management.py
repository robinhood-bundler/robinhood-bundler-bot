import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

class KeyManager:
    """Manages secure AES-256 local encryption and decryption of private keys."""
    
    def __init__(self, password: str):
        # Derive a secure 32-byte key from the master password using PBKDF2
        salt = b"RobinhoodChainSalt_123"  # In production, load a dynamic per-user salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
            backend=default_backend()
        )
        self.encryption_key = kdf.derive(password.encode())

    def encrypt_private_key(self, raw_private_key: str) -> str:
        """Encrypts a hex private key using AES-256-GCM."""
        iv = os.urandom(12)
        encryptor = Cipher(
            algorithms.AES(self.encryption_key),
            modes.GCM(iv),
            backend=default_backend()
        ).encryptor()
        
        ciphertext = encryptor.update(raw_private_key.encode()) + encryptor.finalize()
        # Combine IV, Tag, and Ciphertext into a single package
        combined = iv + encryptor.tag + ciphertext
        return base64.b64encode(combined).decode('utf-8')

    def decrypt_private_key(self, encrypted_package: str) -> str:
        """Decrypts the encrypted package back into the raw private key string."""
        data = base64.b64decode(encrypted_package.encode('utf-8'))
        iv = data[:12]
        tag = data[12:28]
        ciphertext = data[28:]
        
        decryptor = Cipher(
            algorithms.AES(self.encryption_key),
            modes.GCM(iv, tag),
            backend=default_backend()
        ).decryptor()
        
        raw_bytes = decryptor.update(ciphertext) + decryptor.finalize()
        return raw_bytes.decode('utf-8')
