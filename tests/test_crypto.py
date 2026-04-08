import base64
import unittest

from weixin_sdk.crypto import aes_ecb_padded_size, parse_aes_key_base64


class CryptoHelpersTest(unittest.TestCase):
    def test_padded_size(self) -> None:
        self.assertEqual(aes_ecb_padded_size(1), 16)
        self.assertEqual(aes_ecb_padded_size(16), 32)
        self.assertEqual(aes_ecb_padded_size(17), 32)

    def test_parse_raw_base64_key(self) -> None:
        raw = bytes.fromhex("00112233445566778899aabbccddeeff")
        value = base64.b64encode(raw).decode("ascii")
        self.assertEqual(parse_aes_key_base64(value), raw)

    def test_parse_hex_string_base64_key(self) -> None:
        hex_string = b"00112233445566778899aabbccddeeff"
        value = base64.b64encode(hex_string).decode("ascii")
        self.assertEqual(
            parse_aes_key_base64(value),
            bytes.fromhex("00112233445566778899aabbccddeeff"),
        )


if __name__ == "__main__":
    unittest.main()
