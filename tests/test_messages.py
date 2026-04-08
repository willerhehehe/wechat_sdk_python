import unittest

from weixin_sdk.messages import build_text_message_request, extract_text_body


class MessageHelpersTest(unittest.TestCase):
    def test_build_text_message_request(self) -> None:
        payload = build_text_message_request(
            "user@im.wechat",
            "hello",
            context_token="ctx-1",
            client_id="cid-1",
        )
        self.assertEqual(payload["msg"]["to_user_id"], "user@im.wechat")
        self.assertEqual(payload["msg"]["client_id"], "cid-1")
        self.assertEqual(payload["msg"]["context_token"], "ctx-1")
        self.assertEqual(payload["msg"]["item_list"][0]["text_item"]["text"], "hello")

    def test_extract_voice_text(self) -> None:
        message = {
            "item_list": [
                {
                    "type": 3,
                    "voice_item": {
                        "text": "voice as text",
                    },
                }
            ]
        }
        self.assertEqual(extract_text_body(message), "voice as text")


if __name__ == "__main__":
    unittest.main()
