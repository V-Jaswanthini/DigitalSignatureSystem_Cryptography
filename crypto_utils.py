from Crypto.PublicKey import RSA, DSA
from Crypto.Hash import SHA256

def generate_keys(algorithm="RSA"):
    if algorithm == "RSA":
        key = RSA.generate(2048)
    elif algorithm == "DSA":
        key = DSA.generate(2048)
    else:
        raise ValueError("Unsupported Algorithm")
    return key.export_key(), key.publickey().export_key()

def get_hash(data):
    return SHA256.new(data)
