import unittest

from weixin_sdk.media import _infer_extension_from_bytes


class MediaHelpersTest(unittest.TestCase):
    def test_infer_jpeg_extension_for_image(self) -> None:
        item = {"type": 2, "image_item": {}}
        raw = b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01"
        self.assertEqual(_infer_extension_from_bytes(item, raw), ".jpg")

    def test_infer_png_extension_for_image(self) -> None:
        item = {"type": 2, "image_item": {}}
        raw = b"\x89PNG\r\n\x1a\nrest"
        self.assertEqual(_infer_extension_from_bytes(item, raw), ".png")

    def test_keep_original_file_suffix(self) -> None:
        item = {"type": 4, "file_item": {"file_name": "report.pdf"}}
        self.assertEqual(_infer_extension_from_bytes(item, b"anything"), ".pdf")


if __name__ == "__main__":
    unittest.main()
