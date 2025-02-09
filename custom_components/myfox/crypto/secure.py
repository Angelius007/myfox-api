import base64

# https://stackoverflow.com/questions/42568262/how-to-encrypt-text-with-a-password-in-python

ENCODE_BYTES: str = "utf-8"
CODE_SEPARATOR: str = "&&"

def encode(string:str, password:str):
    """
    Base64 encoding schemes are commonly used when there is a need to encode 
    binary data that needs be stored and transferred over media that are 
    designed to deal with textual data.
    This is to ensure that the data remains intact without 
    modification during transport.
    """
    return base64.b64encode((password + CODE_SEPARATOR + string).encode(ENCODE_BYTES)).decode(ENCODE_BYTES)

def decode(string:str, password:str):
    return base64.b64decode(string.encode(ENCODE_BYTES)).decode(ENCODE_BYTES).replace(password + CODE_SEPARATOR, "", 1)
