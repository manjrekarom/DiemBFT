import nacl.encoding
from nacl.hash import sha256

_encoder = nacl.encoding.Base64Encoder

def hasher(*items) -> str:
    """
    Return digest as string
    """
    msg = ''
    items = list(map(repr, items))
    msg = '|||'.join(items)
    if msg is str:
        msg = msg.encode('utf-8')
    else:
        msg = repr(msg).encode('utf8')
    return sha256(msg, encoder=_encoder).decode('utf-8')

def sign(msg, private_key):
    raise NotImplementedError

def valid_signatures(block: 'Block', last_tc: 'TC'):
    raise NotImplementedError
