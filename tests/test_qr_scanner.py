import cv2
import qrcode
import numpy as np
import pytest

from core.qr_scanner import decode_qr_from_frame


def _generate_qr_frame(data):
    """
    Generate a QR code image in-memory as an OpenCV-compatible frame.
    """

    img = qrcode.make(data)
    img = img.convert("RGB")

    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    return frame


def test_decode_qr_from_frame_finds_url():
    frame = _generate_qr_frame("https://kapitalbank.uz")

    result = decode_qr_from_frame(frame)

    assert result["found"] is True
    assert result["data"] == "https://kapitalbank.uz"
    assert result["symbology"] == "QRCODE"


def test_decode_qr_from_frame_no_code_present():
    blank_frame = np.zeros((200, 200, 3), dtype=np.uint8)

    result = decode_qr_from_frame(blank_frame)

    assert result["found"] is False
    assert result["data"] is None
    assert result["symbology"] is None