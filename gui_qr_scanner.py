#Live QR code / barcode scanner dialog for the desktop GUI.

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit
)
from PySide6.QtCore import Qt, QThread
from PySide6.QtGui import QPixmap

from core.qr_worker import QRScanWorker
from core.qr_classifier import classify_qr_content
from core.qr_safety import assess_qr_safety
from core.messages import get_message


RISK_COLORS = {
    "LOW": "#2ecc71",
    "MEDIUM": "#f1c40f",
    "INFO": "#3498db"
}


class QRScannerDialog(QDialog):

    def __init__(self, language="en", parent=None):
        super().__init__(parent)

        self.language = language
        self.detected_url = None

        self.thread = None
        self.worker = None

        self.setMinimumSize(480, 480)

        self._build_ui()
        self._retranslate_ui()
        self._start_camera()

    def _t(self, key):
        return get_message(key, self.language)

    def _build_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumSize(440, 300)
        layout.addWidget(self.preview_label)

        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.hide()
        layout.addWidget(self.result_text)

        self.close_button = QPushButton()
        self.close_button.clicked.connect(self._on_cancel)
        layout.addWidget(self.close_button)

    def _retranslate_ui(self):
        self.setWindowTitle(self._t("qr_dialog_title"))
        self.preview_label.setText(self._t("qr_dialog_starting"))
        self.status_label.setText(self._t("qr_dialog_prompt"))
        self.close_button.setText(self._t("qr_dialog_cancel"))

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

        classification = classify_qr_content(data, symbology, self.language)

        if classification["type"] == "url":
            self.detected_url = classification["details"]["url"]
            self.status_label.setText(self._t("qr_dialog_url_detected"))
            self.accept()
            return

        self._show_non_url_result(classification)

    def _show_non_url_result(self, classification):
        safety = assess_qr_safety(classification, self.language)
        color = RISK_COLORS.get(safety["risk_level"], "#e6f1f7")

        self.preview_label.hide()
        self.close_button.setText(self._t("qr_dialog_close"))

        self.status_label.setText(f"{self._t('qr_dialog_detected_prefix')}: {classification['summary']}")
        self.status_label.setStyleSheet(f"color: {color}; font-weight: bold;")

        details_lines = [f"{self._t('qr_dialog_type_label')}: {classification['summary']}\n"]

        for key, value in classification["details"].items():
            if key in ("has_password", "value"):
                continue
            if value is None:
                continue
            if key == "length":
                label = self._t("qr_field_length")
            else:
                label = key.replace('_', ' ').capitalize()

            details_lines.append(f"{label}: {value}")

        details_lines.append(f"\n{self._t('qr_dialog_safety_label')}: {safety['risk_level']}")
        details_lines.append(safety["message"])
        details_lines.append(f"\n{self._t('qr_dialog_raw_content_label')}:\n{classification['raw_data']}")

        self.result_text.setText("\n".join(details_lines))
        self.result_text.show()

    def _on_camera_error(self, message):
        self._stop_camera()
        self.status_label.setText(f"{self._t('qr_dialog_camera_error_prefix')}: {message}")
        self.preview_label.setText(self._t("qr_dialog_camera_unavailable"))

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