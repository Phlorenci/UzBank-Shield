"""
Live QR code / barcode scanner dialog for the desktop GUI.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit
)
from PySide6.QtCore import Qt, QThread
from PySide6.QtGui import QPixmap

from core.qr_worker import QRScanWorker
from core.qr_classifier import classify_qr_content
from core.qr_safety import assess_qr_safety


RISK_COLORS = {
    "LOW": "#2ecc71",
    "MEDIUM": "#f1c40f",
    "INFO": "#3498db"
}


class QRScannerDialog(QDialog):
    """
    Shows a live webcam feed and waits for a QR code or barcode to
    be detected.

    For URL QR codes, exposes the decoded URL via self.detected_url
    and closes automatically so the caller can run a full scan.

    For all other types (WiFi, contact card, email, phone, crypto,
    payment QR, barcode, plain text), shows a classification and
    safety summary directly in this dialog instead.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Scan QR Code")
        self.setMinimumSize(480, 480)

        self.detected_url = None

        self.thread = None
        self.worker = None

        self._build_ui()
        self._start_camera()

    def _build_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.preview_label = QLabel("Starting camera...")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumSize(440, 300)
        layout.addWidget(self.preview_label)

        self.status_label = QLabel("Point a QR code or barcode at your camera.")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.hide()
        layout.addWidget(self.result_text)

        self.close_button = QPushButton("Cancel")
        self.close_button.clicked.connect(self._on_cancel)
        layout.addWidget(self.close_button)

    def _start_camera(self):
        self.thread = QThread()
        self.worker = QRScanWorker()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.frame_ready.connect(self._on_frame_ready)
        self.worker.qr_detected.connect(self._on_qr_detected)
        self.worker.camera_error.connect(self._on_camera_error)

        self.thread.start()

    def _on_frame_ready(self, qt_image):
        pixmap = QPixmap.fromImage(qt_image)
        scaled = pixmap.scaled(
            self.preview_label.width(),
            self.preview_label.height(),
            Qt.KeepAspectRatio
        )
        self.preview_label.setPixmap(scaled)

    def _on_qr_detected(self, data, symbology):
        self._stop_camera()

        classification = classify_qr_content(data, symbology)

        if classification["type"] == "url":
            self.detected_url = classification["details"]["url"]
            self.status_label.setText("Website QR code detected — running scan...")
            self.accept()
            return

        self._show_non_url_result(classification)

    def _show_non_url_result(self, classification):
        safety = assess_qr_safety(classification)
        color = RISK_COLORS.get(safety["risk_level"], "#e6f1f7")

        self.preview_label.hide()
        self.close_button.setText("Close")

        self.status_label.setText(f"Detected: {classification['summary']}")
        self.status_label.setStyleSheet(f"color: {color}; font-weight: bold;")

        details_lines = [f"Type: {classification['summary']}\n"]

        for key, value in classification["details"].items():
            if key in ("has_password", "value"):
                continue
            if value is None:
                continue
            details_lines.append(f"{key.replace('_', ' ').capitalize()}: {value}")

        details_lines.append(f"\nSafety: {safety['risk_level']}")
        details_lines.append(safety["message"])
        details_lines.append(f"\nRaw content:\n{classification['raw_data']}")

        self.result_text.setText("\n".join(details_lines))
        self.result_text.show()

    def _on_camera_error(self, message):
        self._stop_camera()
        self.status_label.setText(f"Camera error: {message}")
        self.preview_label.setText("Camera unavailable")

    def _stop_camera(self):
        if self.worker:
            self.worker.stop()

        if self.thread:
            self.thread.quit()
            self.thread.wait()

    def _on_cancel(self):
        self._stop_camera()
        self.reject()

    def closeEvent(self, event):
        self._stop_camera()
        super().closeEvent(event)