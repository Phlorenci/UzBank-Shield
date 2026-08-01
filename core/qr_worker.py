"""
Background worker for live QR code and barcode scanning via webcam.

Runs on a QThread so camera capture and per-frame decoding don't
block the GUI's main thread.
"""

import cv2
from PySide6.QtCore import QObject, Signal, QMutex
from PySide6.QtGui import QImage

from core.qr_scanner import decode_qr_from_frame


class QRScanWorker(QObject):
    """
    Continuously captures frames from the default webcam and checks
    each one for a QR code or barcode. Emits frame_ready for live
    preview and qr_detected once a code is successfully decoded.
    """

    frame_ready = Signal(QImage)
    qr_detected = Signal(str, str)
    camera_error = Signal(str)

    def __init__(self):
        super().__init__()
        self._running = False
        self._mutex = QMutex()

    def stop(self):
        self._mutex.lock()
        self._running = False
        self._mutex.unlock()

    def run(self):
        self._mutex.lock()
        self._running = True
        self._mutex.unlock()

        capture = cv2.VideoCapture(0)

        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        if not capture.isOpened():
            self.camera_error.emit("Could not access the webcam.")
            return

        try:
            while True:
                self._mutex.lock()
                should_continue = self._running
                self._mutex.unlock()

                if not should_continue:
                    break

                success, frame = capture.read()

                if not success:
                    self.camera_error.emit("Failed to read from webcam.")
                    break

                display_frame = cv2.flip(frame, 1)

                result = self._try_decode(frame)

                if result["found"]:
                    self.qr_detected.emit(result["data"], result["symbology"])
                    break

                self._emit_preview_frame(display_frame)

        finally:
            capture.release()

    def _try_decode(self, frame):
        """
        Attempt decoding on the raw frame first, then fall back to a
        grayscale + contrast-enhanced version if that fails.
        """

        result = decode_qr_from_frame(frame)

        if result["found"]:
            return result

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        enhanced = cv2.equalizeHist(gray)

        return decode_qr_from_frame(enhanced)

    def _emit_preview_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channels = rgb_frame.shape
        bytes_per_line = channels * width

        qt_image = QImage(
            rgb_frame.data,
            width,
            height,
            bytes_per_line,
            QImage.Format_RGB888
        )

        self.frame_ready.emit(qt_image.copy())