import logging.config

from typing import Any
from custom_components.myfox.crypto.secure import encode, decode, decode_base64
from custom_components.myfox.api.const import KEY_AUTHORIZED_CODE_ALARM

logging.config.fileConfig('logging.conf', None, True)
_LOGGER = logging.getLogger(__name__)


class TestCrypto :

    # 'logId' =
    # 889915829
    # 'label' =
    # 'Désactivation de la protection depuis internet'
    # 'type' =
    # 'security'
    # 'createdAt' =
    # '2025-02-09T20:30:59Z'
    def testEncryptDecrypt(self):
        password = "1326"
        message = "1111 2222 3333"
        list_str: dict[str, Any] = {}
        list_str[KEY_AUTHORIZED_CODE_ALARM] = message
        encode_str: dict[str, Any] = {}
        _LOGGER.info("map:\t\t\t" + str(list_str))
        encode_str[KEY_AUTHORIZED_CODE_ALARM] = encode(list_str.get(KEY_AUTHORIZED_CODE_ALARM), password)
        list_str.update(encode_str)
        _LOGGER.info("map:\t\t\t" + str(list_str))

        _LOGGER.info("message:\t\t\t" + str(message))
        # encrypt
        input = encode(message, password)
        _LOGGER.info("results chiffré:\t\t" + str(input))
        # decryt
        results = decode(input, password)
        _LOGGER.info("results chiffré/déchiffré:\t" + str(results))
        # decode with bas64?
        _LOGGER.info("results intermediaire:\t" + decode_base64(input))

        assert encode(message, password) != message
        assert decode(encode(message, password), password) == message
