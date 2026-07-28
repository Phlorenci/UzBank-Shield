"""
Settings dialog for the UzBank Shield desktop GUI.
"""

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QComboBox,
    QDialogButtonBox
)

from core.config import save_config


LANGUAGE_OPTIONS = [
    ("English", "en"),
    ("Russian", "ru"),
    ("Uzbek", "uz")
]

LOG_LEVEL_OPTIONS = ["DEBUG", "INFO", "WARNING", "ERROR"]


class SettingsDialog(QDialog):
    def __init__(self, current_config, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Settings")
        self.setMinimumWidth(300)

        self.current_config = current_config
        self.updated_config = None

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        form = QFormLayout()

        self.language_combo = QComboBox()
        for label, code in LANGUAGE_OPTIONS:
            self.language_combo.addItem(label, userData=code)

        current_language = self.current_config.get("language", "en")
        for index, (_, code) in enumerate(LANGUAGE_OPTIONS):
            if code == current_language:
                self.language_combo.setCurrentIndex(index)
                break

        form.addRow("Language:", self.language_combo)

        self.log_level_combo = QComboBox()
        self.log_level_combo.addItems(LOG_LEVEL_OPTIONS)

        current_log_level = self.current_config.get("log_level", "INFO")
        if current_log_level in LOG_LEVEL_OPTIONS:
            self.log_level_combo.setCurrentText(current_log_level)

        form.addRow("Log Level:", self.log_level_combo)

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self._on_save)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def _on_save(self):
        new_config = {
            "language": self.language_combo.currentData(),
            "log_level": self.log_level_combo.currentText()
        }

        self.updated_config = save_config(new_config)
        self.accept()