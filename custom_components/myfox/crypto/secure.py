import base64

# https://stackoverflow.com/questions/42568262/how-to-encrypt-text-with-a-password-in-python

ENCODE_BYTES: str = "utf-8"
CODE_SEPARATOR: str = "=="

def encode(string:str, password:str):
    """
    encode code
    """
    return encode_base64(encode_base64(encode_base64(password) + CODE_SEPARATOR) + encode_base64(string))

def decode(string:str, password:str):
    """
    decode code
    """
    return decode_base64(decode_base64(string).replace(encode_base64(encode_base64(password) + CODE_SEPARATOR), "", 1))

def encode_base64(string:str):
    """
    encode code
    """
    return base64.b64encode(str(string).encode(ENCODE_BYTES)).decode(ENCODE_BYTES)

def decode_base64(string:str):
    """
    encode code
    """
    return base64.b64decode(str(string).encode(ENCODE_BYTES)).decode(ENCODE_BYTES)