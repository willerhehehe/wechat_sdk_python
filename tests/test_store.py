import tempfile
import unittest

from weixin_sdk.models import AccountCredentials, LoginSession
from weixin_sdk.store import StateStore


class StateStoreTest(unittest.TestCase):
    def test_account_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            store = StateStore(tmpdir)
            creds = AccountCredentials(
                account_id="bot@im.bot",
                token="token",
                base_url="https://ilinkai.weixin.qq.com",
                user_id="user@im.wechat",
            )
            store.save_account(creds)
            loaded = store.load_account("bot@im.bot")
            self.assertIsNotNone(loaded)
            assert loaded is not None
            self.assertEqual(loaded.account_id, creds.account_id)
            self.assertEqual(loaded.user_id, creds.user_id)

    def test_context_token_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            store = StateStore(tmpdir)
            store.set_context_token("bot@im.bot", "user@im.wechat", "ctx-token")
            self.assertEqual(
                store.get_context_token("bot@im.bot", "user@im.wechat"),
                "ctx-token",
            )

    def test_login_session_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            store = StateStore(tmpdir)
            session = LoginSession(
                session_key="session-1",
                qrcode="qr",
                qrcode_url="https://example.com/qr",
                started_at=1.0,
                current_api_base_url="https://ilinkai.weixin.qq.com",
                bot_type="3",
            )
            store.save_login_session(session)
            loaded = store.load_login_session("session-1")
            self.assertIsNotNone(loaded)
            assert loaded is not None
            self.assertEqual(loaded.qrcode_url, session.qrcode_url)


if __name__ == "__main__":
    unittest.main()
