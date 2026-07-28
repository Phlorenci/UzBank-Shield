#UzBank Shield - Desktop GUI entry point

import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel
)

from core.validator import validate_url
from core.analyzer import URLAnalyzer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("UzBank Shield")
        self.resize(600, 400)

        self.analyzer = URLAnalyzer()

        self._build_ui()

    def _build_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # ---------------------------------
        # URL input row
        # ---------------------------------

        input_row = QHBoxLayout()

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter a website URL...")

        self.scan_button = QPushButton("Scan")
        self.scan_button.clicked.connect(self._on_scan_clicked)

        input_row.addWidget(self.url_input)
        input_row.addWidget(self.scan_button)

        layout.addLayout(input_row)

        # ---------------------------------
        # Status/result placeholder
        # ---------------------------------

        self.status_label = QLabel("Enter a URL and click Scan.")
        self.status_label.setWordWrap(True)

        layout.addWidget(self.status_label)
        layout.addStretch()

    def _on_scan_clicked(self):
        url = self.url_input.text().strip()

        if not url:
            self.status_label.setText("Please enter a URL first.")
            return

        if not validate_url(url):
            self.status_label.setText("Invalid URL format.")
            return

        self.status_label.setText("Scanning... please wait.")

        # NOTE: this call blocks the UI thread while it runs (network
        # I/O for HTTPS/SSL/WHOIS checks). The window will look frozen
        # during the scan. This gets fixed in the threading stage —
        # for now the goal is just proving the engine wiring works.
        result = self.analyzer.analyze(url)

        self._display_raw_result(result)

    def _display_raw_result(self, result):
        summary = (
            f"Score: {result['score']}/100 ({result['level']})\n"
            f"Verified: {result['verification']['verified']}\n"
            f"Bank: {result['verification']['bank']}\n"
            f"Suspicious TLD: {result['suspicious_tld']}\n"
            f"HTTPS: {result['connection']['https']}\n"
            f"Keywords: {', '.join(result['keywords']) or 'None'}"
        )

        self.status_label.setText(summary)


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()