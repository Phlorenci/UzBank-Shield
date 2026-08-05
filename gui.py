"""
UzBank Shield - Desktop GUI entry point.
"""

import sys
from pathlib import Path
import ctypes

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QGroupBox,
    QScrollArea,
    QSplitter,
    QListWidget,
    QListWidgetItem,
    QToolBar
)
from PySide6.QtCore import Qt, QThread, QObject, Signal
from PySide6.QtGui import QAction, QColor, QIcon

from core.validator import validate_url
from core.analyzer import URLAnalyzer
from core.config import load_config, save_config, CONFIG_PATH, DEFAULT_CONFIG
from core.messages import get_message
from gui.settings_dialog import SettingsDialog
from gui.qr_scanner_dialog import QRScannerDialog
from gui.message_analyzer_dialog import MessageAnalyzerDialog
from gui.ai_assistant_dialog import AIAssistantDialog

LEVEL_COLORS = {
    "LOW": "#2ecc71",
    "MEDIUM": "#f1c40f",
    "HIGH": "#e74c3c"
}

DARK_STYLESHEET = """
QMainWindow, QDialog {
    background-color: #0a1929;
}

QWidget {
    background-color: #0a1929;
    color: #e6f1f7;
    font-size: 13px;
}

QLineEdit {
    background-color: #0f2942;
    border: 1px solid #22d3ee;
    border-radius: 4px;
    padding: 6px;
    color: #e6f1f7;
}

QLineEdit:focus {
    border: 1px solid #67e8f9;
}

QPushButton {
    background-color: #22d3ee;
    color: #0a1929;
    border: none;
    border-radius: 4px;
    padding: 6px 16px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #67e8f9;
}

QPushButton:disabled {
    background-color: #1e3a52;
    color: #5a7a8f;
}

QGroupBox {
    border: 1px solid #1e3a52;
    border-radius: 6px;
    margin-top: 10px;
    padding-top: 10px;
    font-weight: bold;
    color: #22d3ee;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
}

QListWidget {
    background-color: #0f2942;
    border: 1px solid #1e3a52;
    border-radius: 4px;
}

QListWidget::item {
    padding: 6px;
}

QListWidget::item:selected {
    background-color: #1e3a52;
}

QScrollArea {
    border: none;
}

QToolBar {
    background-color: #0f2942;
    border: none;
    spacing: 6px;
    padding: 4px;
}

QComboBox {
    background-color: #0f2942;
    border: 1px solid #22d3ee;
    border-radius: 4px;
    padding: 4px;
    color: #e6f1f7;
}

QSplitter::handle {
    background-color: #1e3a52;
}

QDialogButtonBox QPushButton {
    min-width: 70px;
}
"""


class ScanWorker(QObject):
    """
    Runs URLAnalyzer.analyze() on a background thread so the GUI
    stays responsive during network I/O.
    """

    finished = Signal(dict)
    failed = Signal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        try:
            analyzer = URLAnalyzer()
            result = analyzer.analyze(self.url)
            self.finished.emit(result)

        except Exception as error:
            self.failed.emit(str(error))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        icon_path = Path(__file__).parent / "assets" / "uzbank_shield_logo.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        self.resize(900, 600)

        self.thread = None
        self.worker = None
        self.scan_history = []
        self.last_result = None

        self.config = self._load_or_setup_config()

        self._build_ui()
        self._build_toolbar()
        self._retranslate_ui()

    def _t(self, key):
        return get_message(key, self.config.get("language", "en"))

    # ---------------------------------
    # Config
    # ---------------------------------

    def _load_or_setup_config(self):
        if not CONFIG_PATH.exists():
            dialog = SettingsDialog(DEFAULT_CONFIG, DEFAULT_CONFIG["language"], self)

            if dialog.exec():
                return dialog.updated_config

            return dict(DEFAULT_CONFIG)

        return load_config()

    # ---------------------------------
    # Toolbar
    # ---------------------------------

    def _build_toolbar(self):
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        self.settings_action = QAction(self)
        self.settings_action.triggered.connect(self._open_settings)
        self.toolbar.addAction(self.settings_action)

    def _open_settings(self):
        dialog = SettingsDialog(self.config, self.config.get("language", "en"), self)

        if dialog.exec():
            self.config = dialog.updated_config
            self._retranslate_ui()
            self.status_label.setText(self._t("gui_status_settings_saved"))

    # ---------------------------------
    # UI construction
    # ---------------------------------

    def _build_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        outer_layout = QVBoxLayout()
        central_widget.setLayout(outer_layout)

        input_row = QHBoxLayout()

        self.url_input = QLineEdit()
        self.url_input.returnPressed.connect(self._on_scan_clicked)

        #scan button
        self.scan_button = QPushButton()
        self.scan_button.clicked.connect(self._on_scan_clicked)
        # QR button
        self.qr_button = QPushButton()
        self.qr_button.clicked.connect(self._on_qr_button_clicked)
        # message button
        self.message_button = QPushButton()
        self.message_button.clicked.connect(self._on_message_button_clicked)
        # AI assistant button
        self.ai_button = QPushButton()
        self.ai_button.clicked.connect(self._on_ai_button_clicked)

        input_row.addWidget(self.url_input)
        input_row.addWidget(self.scan_button)
        input_row.addWidget(self.qr_button)
        input_row.addWidget(self.message_button)
        input_row.addWidget(self.ai_button)

        outer_layout.addLayout(input_row)

        self.status_label = QLabel()
        self.status_label.setWordWrap(True)
        outer_layout.addWidget(self.status_label)

        splitter = QSplitter(Qt.Horizontal)

        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self._on_history_item_clicked)
        self.history_list.setMaximumWidth(250)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        self.results_container = QWidget()
        self.results_layout = QVBoxLayout()
        self.results_container.setLayout(self.results_layout)

        scroll_area.setWidget(self.results_container)

        splitter.addWidget(self.history_list)
        splitter.addWidget(scroll_area)
        splitter.setStretchFactor(1, 1)

        outer_layout.addWidget(splitter)

        self._build_result_sections()

    def _build_result_sections(self):
        self.score_label = QLabel("")
        self.score_label.setAlignment(Qt.AlignCenter)
        font = self.score_label.font()
        font.setPointSize(18)
        font.setBold(True)
        self.score_label.setFont(font)

        self.results_layout.addWidget(self.score_label)

        self.verification_box = QGroupBox()
        self.verification_form = QFormLayout()
        self.verification_box.setLayout(self.verification_form)
        self.results_layout.addWidget(self.verification_box)

        self.payment_box = QGroupBox()
        self.payment_form = QFormLayout()
        self.payment_box.setLayout(self.payment_form)
        self.results_layout.addWidget(self.payment_box)

        self.page_box = QGroupBox()
        self.page_form = QFormLayout()
        self.page_box.setLayout(self.page_form)
        self.results_layout.addWidget(self.page_box)

        self.connection_box = QGroupBox()
        self.connection_form = QFormLayout()
        self.connection_box.setLayout(self.connection_form)
        self.results_layout.addWidget(self.connection_box)

        self.whois_box = QGroupBox()
        self.whois_form = QFormLayout()
        self.whois_box.setLayout(self.whois_form)
        self.results_layout.addWidget(self.whois_box)

        self.keywords_box = QGroupBox()
        keywords_layout = QVBoxLayout()
        self.keywords_label = QLabel("-")
        self.keywords_label.setWordWrap(True)
        keywords_layout.addWidget(self.keywords_label)
        self.keywords_box.setLayout(keywords_layout)
        self.results_layout.addWidget(self.keywords_box)

        self.results_layout.addStretch()

        self._clear_result_sections()

    def _clear_result_sections(self):
        for form in (
            self.verification_form,
            self.payment_form,
            self.page_form,
            self.connection_form,
            self.whois_form
        ):
            while form.rowCount():
                form.removeRow(0)

        self.score_label.setText("")
        self.keywords_label.setText(self._t("gui_no_keywords"))

    # ---------------------------------
    # Retranslation — called on startup and whenever language changes
    # ---------------------------------

    def _retranslate_ui(self):
        self.setWindowTitle("UzBank Shield")

        self.url_input.setPlaceholderText(self._t("gui_url_placeholder"))
        self.scan_button.setText(self._t("gui_scan_button"))
        self.qr_button.setText(self._t("gui_qr_button"))
        self.message_button.setText(self._t("gui_message_button"))
        self.settings_action.setText(self._t("gui_settings_button"))
        self.ai_button.setText(self._t("gui_ai_button"))

        if not self.scan_history:
            self.status_label.setText(self._t("gui_status_ready"))

        self.verification_box.setTitle(self._t("gui_group_verification"))
        self.payment_box.setTitle(self._t("gui_group_payment"))
        self.page_box.setTitle(self._t("gui_group_page_analysis"))
        self.connection_box.setTitle(self._t("gui_group_connection"))
        self.whois_box.setTitle(self._t("gui_group_whois"))
        self.keywords_box.setTitle(self._t("gui_group_keywords"))

        # Re-render the currently displayed result (if any) in the
        # new language, since form rows were built with the old
        # language's labels baked in as plain text.
        if self.last_result:
            self._clear_result_sections()
            self._display_result(self.last_result)
        elif not self.scan_history:
            self.keywords_label.setText(self._t("gui_no_keywords"))

    # ---------------------------------
    # Scanning
    # ---------------------------------

    def _on_scan_clicked(self):
        url = self.url_input.text().strip()

        if not url:
            self.status_label.setText(self._t("gui_status_empty_url"))
            return

        if not validate_url(url):
            self.status_label.setText(self._t("gui_status_invalid_url"))
            return

        self._set_scanning_state(True)
        self._clear_result_sections()
        self.status_label.setText(self._t("gui_status_scanning"))

        self._start_scan(url)

    def _set_scanning_state(self, scanning):
        self.scan_button.setEnabled(not scanning)
        self.url_input.setEnabled(not scanning)
        self.qr_button.setEnabled(not scanning)

    def _start_scan(self, url):
        self.thread = QThread()
        self.worker = ScanWorker(url)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self._on_scan_finished)
        self.worker.failed.connect(self._on_scan_failed)

        self.worker.finished.connect(self.thread.quit)
        self.worker.failed.connect(self.thread.quit)
        self.thread.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def _on_scan_finished(self, result):
        self._set_scanning_state(False)

        url = result["components"]["original_url"]
        self.status_label.setText(f"{self._t('gui_status_scan_complete')}: {url}")

        self._add_to_history(result)
        self.last_result = result
        self._display_result(result)

        self.url_input.clear()

    def _on_scan_failed(self, error_message):
        self._set_scanning_state(False)
        self.status_label.setText(f"{self._t('gui_status_scan_failed')}: {error_message}")

    def _on_qr_button_clicked(self):
        dialog = QRScannerDialog(self.config.get("language", "en"), self)

        if dialog.exec() and dialog.detected_url:
            self.url_input.setText(dialog.detected_url)
            self._on_scan_clicked()

    def _on_message_button_clicked(self):
        dialog = MessageAnalyzerDialog(self.config.get("language", "en"), self)
        dialog.exec()

    def _on_ai_button_clicked(self):
        dialog = AIAssistantDialog(
            self.config.get("openai_api_key", ""),
            self.config.get("language", "en"),
            self.last_result,
            self
        )
        dialog.exec()

    # ---------------------------------
    # History
    # ---------------------------------

    def _add_to_history(self, result):
        self.scan_history.append(result)

        url = result["components"]["original_url"]
        level = result["level"]

        item_text = f"[{level}] {url}"
        item = QListWidgetItem(item_text)

        color = LEVEL_COLORS.get(level)
        if color:
            item.setForeground(QColor(color))

        self.history_list.addItem(item)
        self.history_list.setCurrentItem(item)

    def _on_history_item_clicked(self, item):
        index = self.history_list.row(item)
        result = self.scan_history[index]

        self.last_result = result
        self._clear_result_sections()
        self._display_result(result)

        url = result["components"]["original_url"]
        self.status_label.setText(f"{self._t('gui_status_viewing')}: {url}")

    # ---------------------------------
    # Results display
    # ---------------------------------

    def _display_result(self, result):
        score = result["score"]
        level = result["level"]
        color = LEVEL_COLORS.get(level, "#ffffff")

        level_key = f"risk_level_{level.lower()}"
        self.score_label.setText(f"{score}/100 — {self._t(level_key)}")
        self.score_label.setStyleSheet(f"color: {color};")

        lang = self.config.get("language", "en")

        def yn(value):
            return get_message("value_yes", lang) if value else get_message("value_no", lang)

        verification = result["verification"]

        self.verification_form.addRow(
            self._t("gui_field_status"),
            QLabel(
                get_message("verified", lang)
                if verification["verified"]
                else get_message("not_verified", lang)
            )
        )
        self.verification_form.addRow(
            self._t("gui_field_bank"), QLabel(verification["bank"] or "-")
        )
        self.verification_form.addRow(
            self._t("gui_field_closest_domain"), QLabel(verification["closest_domain"] or "-")
        )
        self.verification_form.addRow(
            self._t("gui_field_similarity"), QLabel(f"{verification['similarity']}%")
        )
        self.verification_form.addRow(
            self._t("gui_field_impersonation"),
            QLabel(yn(verification["possible_typosquatting"]))
        )

        payment_verification = result["payment_verification"]

        self.payment_form.addRow(
            self._t("gui_field_status"),
            QLabel(
                get_message("verified", lang)
                if payment_verification["verified"]
                else get_message("not_verified", lang)
            )
        )
        self.payment_form.addRow(
            self._t("gui_field_processor"), QLabel(payment_verification["processor"] or "-")
        )
        self.payment_form.addRow(
            self._t("gui_field_closest_domain"), QLabel(payment_verification["closest_domain"] or "-")
        )
        self.payment_form.addRow(
            self._t("gui_field_similarity"), QLabel(f"{payment_verification['similarity']}%")
        )
        self.payment_form.addRow(
            self._t("gui_field_impersonation"),
            QLabel(yn(payment_verification["possible_typosquatting"]))
        )

        page_analysis = result["page_analysis"]

        self.page_form.addRow(
            self._t("gui_field_page_analyzed"),
            QLabel(yn(page_analysis["analyzed"]))
        )
        self.page_form.addRow(
            self._t("gui_field_requests_card"),
            QLabel(yn(page_analysis["requests_card_info"]))
        )

        connection = result["connection"]
        ssl_info = result["ssl_info"]

        self.connection_form.addRow(self._t("gui_field_protocol"), QLabel(connection["protocol"]))
        self.connection_form.addRow(
            self._t("gui_field_reachable"),
            QLabel(yn(connection["reachable"]))
        )
        self.connection_form.addRow(
            self._t("gui_field_suspicious_tld"),
            QLabel(yn(result["suspicious_tld"]))
        )

        if ssl_info["valid"] is True:
            ssl_status = self._t("gui_value_valid")
        elif ssl_info["valid"] is False:
            ssl_status = self._t("gui_value_invalid")
        else:
            ssl_status = self._t("gui_value_not_checked")

        self.connection_form.addRow(self._t("gui_field_ssl_certificate"), QLabel(ssl_status))
        self.connection_form.addRow(
            self._t("gui_field_ssl_expires"), QLabel(ssl_info["expires"] or "-")
        )

        domain_info = result["domain_info"]

        self.whois_form.addRow(
            self._t("gui_field_whois_data"),
            QLabel(
                self._t("gui_value_available")
                if domain_info["available"]
                else self._t("gui_value_not_available")
            )
        )
        self.whois_form.addRow(
            self._t("gui_field_registrar"), QLabel(domain_info["registrar"] or "-")
        )
        self.whois_form.addRow(
            self._t("gui_field_created"), QLabel(domain_info["created"] or "-")
        )

        age_text = (
            f"{domain_info['age_days']} {self._t('gui_days_suffix')}"
            if domain_info["age_days"] is not None
            else "-"
        )
        self.whois_form.addRow(self._t("gui_field_domain_age"), QLabel(age_text))

        keywords = result["keywords"]
        self.keywords_label.setText(
            ", ".join(keywords) if keywords else self._t("gui_no_keywords")
        )


def main():
    if sys.platform == "win32":
        app_id = "UzBankShield.DesktopApp.1.0"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_STYLESHEET)

    icon_path = Path(__file__).parent / "assets" / "uzbank_shield_logo.ico"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()