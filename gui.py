"""
UzBank Shield - Desktop GUI entry point.
"""

from pathlib import Path
import sys

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
    QListWidgetItem
)
from PySide6.QtCore import Qt, QThread, QObject, Signal

from core.validator import validate_url
from core.analyzer import URLAnalyzer
from PySide6.QtWidgets import QToolBar
from PySide6.QtGui import QAction

from core.config import load_config, save_config, CONFIG_PATH, DEFAULT_CONFIG
from gui_settings import SettingsDialog
from core.messages import get_message
from PySide6.QtGui import QColor
from PySide6.QtGui import QIcon


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
    stays responsive during network I/O (HTTPS, SSL, WHOIS checks).
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

        self.setWindowTitle("UzBank Shield")
        icon_path = Path(__file__).parent / "assets" / "uzbank_shield_logo.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        self.resize(900, 600)

        self.thread = None
        self.worker = None
        self.scan_history = []

        # Session-only scan history: list index -> full result dict.
        # Not persisted to disk; cleared when the app closes.
        
        self.config = self._load_or_setup_config()

        self._build_ui()
        self._build_toolbar()

    def _build_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self._open_settings)
        toolbar.addAction(settings_action)

    def _load_or_setup_config(self):
        if not CONFIG_PATH.exists():
            # Fresh install — don't call load_config() here, since it
            # would try to run a terminal input() prompt for first-run
            # setup, which doesn't work in a windowed app. Show our
            # own Settings dialog instead, pre-filled with defaults.
            dialog = SettingsDialog(DEFAULT_CONFIG, self)

            if dialog.exec():
                return dialog.updated_config

            # User cancelled first-run setup — fall back to defaults
            # without writing a config.json, so they'll be asked again
            # next launch.
            return dict(DEFAULT_CONFIG)

        return load_config()

    def _open_settings(self):
        dialog = SettingsDialog(self.config, self)

        if dialog.exec():
            self.config = dialog.updated_config
            self.status_label.setText(
                "Settings saved. Re-scan or reselect a history item to see language changes."
            )
            
    def _build_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        outer_layout = QVBoxLayout()
        central_widget.setLayout(outer_layout)

        # ---------------------------------
        # URL input row
        # ---------------------------------

        input_row = QHBoxLayout()

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter a website URL...")
        self.url_input.returnPressed.connect(self._on_scan_clicked)

        self.scan_button = QPushButton("Scan")
        self.scan_button.clicked.connect(self._on_scan_clicked)

        input_row.addWidget(self.url_input)
        input_row.addWidget(self.scan_button)

        outer_layout.addLayout(input_row)

        # ---------------------------------
        # Status message (errors, "scanning...")
        # ---------------------------------

        self.status_label = QLabel("Enter a URL and click Scan.")
        self.status_label.setWordWrap(True)

        outer_layout.addWidget(self.status_label)

        # ---------------------------------
        # Split view: history list | results
        # ---------------------------------

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

        self.verification_box = QGroupBox("Official Domain Verification")
        self.verification_form = QFormLayout()
        self.verification_box.setLayout(self.verification_form)
        self.results_layout.addWidget(self.verification_box)

        self.payment_box = QGroupBox("Official Payment Processor Verification")
        self.payment_form = QFormLayout()
        self.payment_box.setLayout(self.payment_form)
        self.results_layout.addWidget(self.payment_box)

        self.connection_box = QGroupBox("Connection & SSL")
        self.connection_form = QFormLayout()
        self.connection_box.setLayout(self.connection_form)
        self.results_layout.addWidget(self.connection_box)

        self.whois_box = QGroupBox("Domain Information (WHOIS)")
        self.whois_form = QFormLayout()
        self.whois_box.setLayout(self.whois_form)
        self.results_layout.addWidget(self.whois_box)

        self.keywords_box = QGroupBox("Detected Keywords")
        keywords_layout = QVBoxLayout()
        self.keywords_label = QLabel("-")
        self.keywords_label.setWordWrap(True)
        keywords_layout.addWidget(self.keywords_label)
        self.keywords_box.setLayout(keywords_layout)
        self.results_layout.addWidget(self.keywords_box)

        self.results_layout.addStretch()

        self._clear_result_sections()

    def _clear_result_sections(self):
        for form in (self.verification_form, self.payment_form, self.connection_form, self.whois_form):
            while form.rowCount():
                form.removeRow(0)

        self.score_label.setText("")
        self.keywords_label.setText("-")

    def _on_scan_clicked(self):
        url = self.url_input.text().strip()

        if not url:
            self.status_label.setText("Please enter a URL first.")
            return

        if not validate_url(url):
            self.status_label.setText("Invalid URL format.")
            return

        self._set_scanning_state(True)
        self._clear_result_sections()
        self.status_label.setText("Scanning... please wait.")

        self._start_scan(url)

    def _set_scanning_state(self, scanning):
        self.scan_button.setEnabled(not scanning)
        self.url_input.setEnabled(not scanning)

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
        self.status_label.setText(f"Scan complete: {result['components']['original_url']}")

        self._add_to_history(result)
        self._display_result(result)

        self.url_input.clear()

    def _on_scan_failed(self, error_message):
        self._set_scanning_state(False)
        self.status_label.setText(f"Scan failed: {error_message}")

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

        self._clear_result_sections()
        self._display_result(result)
        self.status_label.setText(f"Viewing: {result['components']['original_url']}")

    def _display_result(self, result):
        score = result["score"]
        level = result["level"]
        color = LEVEL_COLORS.get(level, "#ffffff")

        self.score_label.setText(f"{score}/100 — {level} RISK")
        self.score_label.setStyleSheet(f"color: {color};")

        verification = result["verification"]

        language = self.config.get("language", "en")

        self.verification_form.addRow(
            "Status:",
            QLabel(
                get_message("verified", language)
                if verification["verified"]
                else get_message("not_verified", language)
            )
        )
        self.verification_form.addRow(
            "Bank:", QLabel(verification["bank"] or "-")
        )
        self.verification_form.addRow(
            "Closest Domain:", QLabel(verification["closest_domain"] or "-")
        )
        self.verification_form.addRow(
            "Similarity:", QLabel(f"{verification['similarity']}%")
        )
        self.verification_form.addRow(
            "Possible Impersonation:",
            QLabel("Yes" if verification["possible_typosquatting"] else "No")
        )

        payment_verification = result["payment_verification"]

        self.payment_form.addRow(
            "Status:",
            QLabel("Verified" if payment_verification["verified"] else "Not Verified")
        )
        self.payment_form.addRow(
            "Processor:", QLabel(payment_verification["processor"] or "-")
        )
        self.payment_form.addRow(
            "Closest Domain:", QLabel(payment_verification["closest_domain"] or "-")
        )
        self.payment_form.addRow(
            "Similarity:", QLabel(f"{payment_verification['similarity']}%")
        )
        self.payment_form.addRow(
            "Possible Impersonation:",
            QLabel("Yes" if payment_verification["possible_typosquatting"] else "No")
        )

        connection = result["connection"]
        ssl_info = result["ssl_info"]

        self.connection_form.addRow(
            "Protocol:", QLabel(connection["protocol"])
        )
        self.connection_form.addRow(
            "Reachable:", QLabel("Yes" if connection["reachable"] else "No")
        )
        self.connection_form.addRow(
            "Suspicious TLD:", QLabel("Yes" if result["suspicious_tld"] else "No")
        )

        if ssl_info["valid"] is True:
            ssl_status = "Valid"
        elif ssl_info["valid"] is False:
            ssl_status = "Invalid"
        else:
            ssl_status = "Not Checked"

        self.connection_form.addRow("SSL Certificate:", QLabel(ssl_status))
        self.connection_form.addRow(
            "SSL Expires:", QLabel(ssl_info["expires"] or "-")
        )

        domain_info = result["domain_info"]

        self.whois_form.addRow(
            "WHOIS Data:",
            QLabel("Available" if domain_info["available"] else "Not Available")
        )
        self.whois_form.addRow(
            "Registrar:", QLabel(domain_info["registrar"] or "-")
        )
        self.whois_form.addRow(
            "Created:", QLabel(domain_info["created"] or "-")
        )

        age_text = (
            f"{domain_info['age_days']} days"
            if domain_info["age_days"] is not None
            else "-"
        )
        self.whois_form.addRow("Domain Age:", QLabel(age_text))

        keywords = result["keywords"]
        self.keywords_label.setText(", ".join(keywords) if keywords else "None detected")


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_STYLESHEET)

    icon_path = Path(__file__).parent / "assets" / "uzbank_shield_logo.png"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()