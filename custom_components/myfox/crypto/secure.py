import base64

# https://stackoverflow.com/questions/42568262/how-to-encrypt-text-with-a-password-in-python

ENCODE_BYTES: str = "utf-8"
CODE_SEPARATOR: str = "=="


def encode(code: str, site_id: str):
    """
    encode code
    """
    return encode_base64(seed_(site_id) + encode_base64(code))


def decode(code: str, site_id: str):
    """
    decode code
    """
    return decode_base64(decode_base64(code).replace(seed_(site_id), "", 1))


def seed_(string: str):
    return encode_base64(encode_base64(string) + CODE_SEPARATOR).replace("==", "")


def encode_base64(string: str):
    """
    encode code
    """
    return base64.b64encode(str(string).encode(ENCODE_BYTES)).decode(ENCODE_BYTES)


def decode_base64(string: str):
    """
    encode code
    """
    return base64.b64decode(str(string).encode(ENCODE_BYTES)).decode(ENCODE_BYTES)
