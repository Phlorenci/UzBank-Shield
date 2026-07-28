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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("UzBank Shield")
        self.resize(600, 400)

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

        layout.addWidget(self.status_label)
        layout.addStretch()

    def _on_scan_clicked(self):
        url = self.url_input.text().strip()

        if not url:
            self.status_label.setText("Please enter a URL first.")
            return

        self.status_label.setText(f"Scanning: {url}...")


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()