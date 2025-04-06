import base64
import json
from datetime import datetime
from Crypto.Signature import pkcs1_15, DSS
from Crypto.PublicKey import RSA, DSA
from Crypto.Hash import SHA256

def sign_data(data, private_key_bytes, algorithm, signer="Anonymous"):
    key = RSA.import_key(private_key_bytes) if algorithm == "RSA" else DSA.import_key(private_key_bytes)
    signer_obj = pkcs1_15.new(key) if algorithm == "RSA" else DSS.new(key, 'fips-186-3')
    h = SHA256.new(data)
    signature = signer_obj.sign(h)
    return {
        "signer": signer,
        "algorithm": algorithm,
        "hash": h.hexdigest(),
        "timestamp": datetime.now().isoformat(),
        "signature": base64.b64encode(signature).decode()
    }

def verify_signature(data, public_key_bytes, metadata):
    key = RSA.import_key(public_key_bytes) if metadata["algorithm"] == "RSA" else DSA.import_key(public_key_bytes)
    verifier = pkcs1_15.new(key) if metadata["algorithm"] == "RSA" else DSS.new(key, 'fips-186-3')
    h = SHA256.new(data)
    try:
        verifier.verify(h, base64.b64decode(metadata["signature"]))
        return True
    except:
        return False
