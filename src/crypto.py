import nacl.encoding
from nacl.hash import sha256

_encoder = nacl.encoding.Base64Encoder

def hasher(msg):
    return sha256(msg, encoder=_encoder)

def sign(msg, private_key):
    raise NotImplementedError
