import base64

# https://stackoverflow.com/questions/42568262/how-to-encrypt-text-with-a-password-in-python

ENCODE_BYTES: str = "utf-8"
CODE_SEPARATOR: str = "&&"

def encode(string:str, password:str):
    """
    encode code
    """
    return base64.b64encode((str(password) + CODE_SEPARATOR + str(string)).encode(ENCODE_BYTES)).decode(ENCODE_BYTES)

def decode(string:str, password:str):
    """
    decode code
    """
    return base64.b64decode(string.encode(ENCODE_BYTES)).decode(ENCODE_BYTES).replace(str(password) + CODE_SEPARATOR, "", 1)
