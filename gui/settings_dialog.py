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
from core.messages import get_message
from PySide6.QtWidgets import QLineEdit


LANGUAGE_OPTIONS = [
    ("English", "en"),
    ("Russian", "ru"),
    ("Uzbek", "uz")
]

LOG_LEVEL_OPTIONS = ["DEBUG", "INFO", "WARNING", "ERROR"]


class SettingsDialog(QDialog):
    def __init__(self, current_config, language="en", parent=None):
        super().__init__(parent)

        self.current_config = current_config
        self.language = language
        self.updated_config = None

        self.setMinimumWidth(300)

        self._build_ui()
        self._retranslate_ui()

    def _t(self, key):
        return get_message(key, self.language)

    def _build_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.form = QFormLayout()

        self.language_combo = QComboBox()
        for label, code in LANGUAGE_OPTIONS:
            self.language_combo.addItem(label, userData=code)

        current_language = self.current_config.get("language", "en")
        for index, (_, code) in enumerate(LANGUAGE_OPTIONS):
            if code == current_language:
                self.language_combo.setCurrentIndex(index)
                break

        self.form.addRow(" ", self.language_combo)

        self.log_level_combo = QComboBox()
        self.log_level_combo.addItems(LOG_LEVEL_OPTIONS)

        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.Password)
        self.api_key_input.setText(self.current_config.get("openai_api_key", ""))

        self.form.addRow(" ", self.api_key_input)

        current_log_level = self.current_config.get("log_level", "INFO")
        if current_log_level in LOG_LEVEL_OPTIONS:
            self.log_level_combo.setCurrentText(current_log_level)

        self.form.addRow(" ", self.log_level_combo)

        layout.addLayout(self.form)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel
        )
        self.buttons.accepted.connect(self._on_save)
        self.buttons.rejected.connect(self.reject)

        layout.addWidget(self.buttons)

    def _retranslate_ui(self):
        self.setWindowTitle(self._t("settings_title"))

        self.form.labelForField(self.language_combo).setText(
            self._t("settings_language_label")
        )
        self.form.labelForField(self.log_level_combo).setText(
            self._t("settings_log_level_label")
        )
        self.form.labelForField(self.api_key_input).setText(
            self._t("settings_openai_key_label")
        )
        self.api_key_input.setPlaceholderText(self._t("settings_openai_key_placeholder"))

        self.buttons.button(QDialogButtonBox.Save).setText(self._t("settings_save"))
        self.buttons.button(QDialogButtonBox.Cancel).setText(self._t("settings_cancel"))

    def _on_save(self):
        new_config = {
            "language": self.language_combo.currentData(),
            "log_level": self.log_level_combo.currentText(),
            "openai_api_key": self.api_key_input.text().strip()
        }

        self.updated_config = save_config(new_config)
        self.accept()