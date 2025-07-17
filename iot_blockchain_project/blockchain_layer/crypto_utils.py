from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
import base64

def generate_ecdsa_keys():
    private_key = ECC.generate(curve='P-256')
    public_key = private_key.public_key()
    return private_key, public_key

def sign_data(private_key, data):
    signer = DSS.new(private_key, 'fips-186-3')
    h = SHA256.new(data.encode())
    signature = signer.sign(h)
    return base64.b64encode(signature).decode()

def verify_signature(public_key, data, signature):
    try:
        verifier = DSS.new(public_key, 'fips-186-3')
        h = SHA256.new(data.encode())
        verifier.verify(h, base64.b64decode(signature))
        return True
    except (ValueError, TypeError):
        return False

def encrypt_aes(data, key):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return (
        base64.b64encode(ciphertext).decode(),
        base64.b64encode(cipher.nonce).decode(),
        base64.b64encode(tag).decode()
    )

def decrypt_aes(encrypted_data, nonce, tag, key):
    cipher = AES.new(key, AES.MODE_EAX, nonce=base64.b64decode(nonce))
    return cipher.decrypt_and_verify(
        base64.b64decode(encrypted_data),
        base64.b64decode(tag)
    ).decode()