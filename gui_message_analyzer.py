"""
SMS/message analysis dialog for the desktop GUI.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton,
    QLabel, QScrollArea, QWidget, QGroupBox
)
from PySide6.QtCore import Qt, QThread, QObject, Signal

from core.sms_analyzer import analyze_message, assess_message_risk
from core.messages import get_message


LEVEL_COLORS = {
    "LOW": "#2ecc71",
    "MEDIUM": "#f1c40f",
    "HIGH": "#e74c3c"
}

CATEGORY_KEYS = {
    "urgency": "message_dialog_category_urgency",
    "sensitive_info_request": "message_dialog_category_sensitive_info_request",
    "too_good_to_be_true": "message_dialog_category_too_good_to_be_true",
    "fake_authority": "message_dialog_category_fake_authority"
}


class MessageAnalysisWorker(QObject):
    """
    Runs analyze_message() on a background thread, since it may
    call URLAnalyzer (network I/O) for each URL found in the message.
    """

    finished = Signal(dict)
    failed = Signal(str)

    def __init__(self, text):
        super().__init__()
        self.text = text

    def run(self):
        try:
            result = analyze_message(self.text)
            self.finished.emit(result)
        except Exception as error:
            self.failed.emit(str(error))


class MessageAnalyzerDialog(QDialog):
    def __init__(self, language="en", parent=None):
        super().__init__(parent)

        self.language = language
        self.thread = None
        self.worker = None

        self.setMinimumSize(600, 600)

        self._build_ui()
        self._retranslate_ui()

    def _t(self, key):
        return get_message(key, self.language)

    def _build_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.message_input = QTextEdit()
        self.message_input.setMinimumHeight(120)
        layout.addWidget(self.message_input)

        button_row = QHBoxLayout()

        self.analyze_button = QPushButton()
        self.analyze_button.clicked.connect(self._on_analyze_clicked)
        button_row.addWidget(self.analyze_button)

        self.close_button = QPushButton()
        self.close_button.clicked.connect(self.reject)
        button_row.addWidget(self.close_button)

        layout.addLayout(button_row)

        self.status_label = QLabel()
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        self.results_container = QWidget()
        self.results_layout = QVBoxLayout()
        self.results_container.setLayout(self.results_layout)

        scroll_area.setWidget(self.results_container)
        layout.addWidget(scroll_area)

    def _retranslate_ui(self):
        self.setWindowTitle(self._t("message_dialog_title"))
        self.message_input.setPlaceholderText(self._t("message_dialog_placeholder"))
        self.analyze_button.setText(self._t("message_dialog_analyze"))
        self.close_button.setText(self._t("message_dialog_close"))

    def _clear_results(self):
        while self.results_layout.count():
            item = self.results_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def _on_analyze_clicked(self):
        text = self.message_input.toPlainText().strip()

        if not text:
            self.status_label.setText(self._t("message_dialog_empty"))
            return

        self._clear_results()
        self.analyze_button.setEnabled(False)
        self.status_label.setText("...")

        self.thread = QThread()
        self.worker = MessageAnalysisWorker(text)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self._on_analysis_finished)
        self.worker.failed.connect(self._on_analysis_failed)

        self.worker.finished.connect(self.thread.quit)
        self.worker.failed.connect(self.thread.quit)
        self.thread.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def _on_analysis_finished(self, analysis):
        self.analyze_button.setEnabled(True)

        risk = assess_message_risk(analysis)
        color = LEVEL_COLORS.get(risk["level"], "#e6f1f7")

        verdict_label = QLabel(f"{self._t('message_dialog_verdict')}: {risk['level']}")
        verdict_label.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 16px;")
        self.results_layout.addWidget(verdict_label)

        for reason in risk["reasons"]:
            reason_label = QLabel(f"• {reason}")
            reason_label.setWordWrap(True)
            self.results_layout.addWidget(reason_label)

        if analysis["has_url"]:
            url_box = QGroupBox(self._t("message_dialog_urls_found"))
            url_layout = QVBoxLayout()

            for url_result in analysis["urls"]:
                url = url_result["url"]

                if url_result.get("analysis"):
                    level = url_result["analysis"]["level"]
                    score = url_result["analysis"]["score"]
                    level_color = LEVEL_COLORS.get(level, "#e6f1f7")
                    line = QLabel(f"{url} — {score}/100 ({level})")
                    line.setStyleSheet(f"color: {level_color};")
                else:
                    line = QLabel(f"{url} — analysis failed")

                line.setWordWrap(True)
                url_layout.addWidget(line)

            url_box.setLayout(url_layout)
            self.results_layout.addWidget(url_box)

        if analysis["has_suspicious_patterns"]:
            pattern_box = QGroupBox(self._t("message_dialog_patterns_found"))
            pattern_layout = QVBoxLayout()

            for category, phrases in analysis["matched_patterns"].items():
                category_label_key = CATEGORY_KEYS.get(category, category)
                category_title = QLabel(f"<b>{self._t(category_label_key)}</b>")
                pattern_layout.addWidget(category_title)

                for phrase in phrases:
                    phrase_label = QLabel(f"  \"{phrase}\"")
                    pattern_layout.addWidget(phrase_label)

            pattern_box.setLayout(pattern_layout)
            self.results_layout.addWidget(pattern_box)

        if not analysis["has_url"] and not analysis["has_suspicious_patterns"]:
            self.results_layout.addWidget(QLabel(self._t("message_dialog_no_findings")))

        self.results_layout.addStretch()
        self.status_label.setText("")

    def _on_analysis_failed(self, error_message):
        self.analyze_button.setEnabled(True)
        self.status_label.setText(f"Error: {error_message}")