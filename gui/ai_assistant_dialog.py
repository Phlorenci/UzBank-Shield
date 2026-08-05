"""
AI Security Assistant chat dialog for the desktop GUI.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit,
    QPushButton, QLabel, QScrollArea, QWidget
)
from PySide6.QtCore import Qt, QThread, QObject, Signal

from core.ai_assistant import ask_assistant, AssistantError
from core.messages import get_message


class AssistantWorker(QObject):
    """
    Runs ask_assistant() on a background thread so the GUI stays
    responsive during the API call.
    """

    finished = Signal(str)
    failed = Signal(str)

    def __init__(self, api_key, question, scan_result, history):
        super().__init__()
        self.api_key = api_key
        self.question = question
        self.scan_result = scan_result
        self.history = history

    def run(self):
        try:
            response = ask_assistant(
                self.api_key,
                self.question,
                self.scan_result,
                self.history
            )
            self.finished.emit(response)

        except AssistantError as error:
            self.failed.emit(str(error))

        except Exception as error:
            self.failed.emit(f"Unexpected error: {error}")


class AIAssistantDialog(QDialog):
    def __init__(self, api_key, language="en", scan_result=None, parent=None):
        super().__init__(parent)

        self.api_key = api_key
        self.language = language
        self.scan_result = scan_result
        self.conversation_history = []

        self.thread = None
        self.worker = None

        self.setMinimumSize(560, 600)

        self._build_ui()
        self._retranslate_ui()

        if scan_result:
            self._show_context_notice()

    def _t(self, key):
        return get_message(key, self.language)

    def _build_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout()
        self.chat_layout.addStretch()
        self.chat_container.setLayout(self.chat_layout)

        scroll_area.setWidget(self.chat_container)
        self.scroll_area = scroll_area
        layout.addWidget(scroll_area)

        input_row = QHBoxLayout()

        self.question_input = QLineEdit()
        self.question_input.returnPressed.connect(self._on_send_clicked)
        input_row.addWidget(self.question_input)

        self.send_button = QPushButton()
        self.send_button.clicked.connect(self._on_send_clicked)
        input_row.addWidget(self.send_button)

        layout.addLayout(input_row)

        self.status_label = QLabel()
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        self.close_button = QPushButton()
        self.close_button.clicked.connect(self.reject)
        layout.addWidget(self.close_button)

    def _retranslate_ui(self):
        self.setWindowTitle(self._t("ai_dialog_title"))
        self.question_input.setPlaceholderText(self._t("ai_dialog_placeholder"))
        self.send_button.setText(self._t("ai_dialog_send"))
        self.close_button.setText(self._t("ai_dialog_close"))

    def _show_context_notice(self):
        url = self.scan_result["components"]["original_url"]
        self._add_message(
            self._t("ai_dialog_context_notice").format(url=url),
            is_user=False,
            is_notice=True
        )

    def _add_message(self, text, is_user, is_notice=False):
        label = QLabel(text)
        label.setWordWrap(True)
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        if is_notice:
            label.setStyleSheet(
                "background-color: #1e3a52; color: #9ac4d8; "
                "padding: 8px; border-radius: 6px; font-style: italic;"
            )
        elif is_user:
            label.setStyleSheet(
                "background-color: #22d3ee; color: #0a1929; "
                "padding: 8px; border-radius: 6px; font-weight: bold;"
            )
        else:
            label.setStyleSheet(
                "background-color: #0f2942; color: #e6f1f7; "
                "padding: 8px; border-radius: 6px;"
            )

        # Insert before the trailing stretch so new messages append
        # in order and the layout keeps growing downward
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, label)

        # Scroll to the newest message
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )

    def _on_send_clicked(self):
        question = self.question_input.text().strip()

        if not question:
            return

        if not self.api_key:
            self.status_label.setText(self._t("ai_dialog_no_key"))
            return

        self._add_message(question, is_user=True)
        self.question_input.clear()

        self._set_sending_state(True)
        self.status_label.setText(self._t("ai_dialog_thinking"))

        self.thread = QThread()
        self.worker = AssistantWorker(
            self.api_key,
            question,
            self.scan_result,
            list(self.conversation_history)
        )
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(lambda response: self._on_response(question, response))
        self.worker.failed.connect(self._on_failed)

        self.worker.finished.connect(self.thread.quit)
        self.worker.failed.connect(self.thread.quit)
        self.thread.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def _set_sending_state(self, sending):
        self.send_button.setEnabled(not sending)
        self.question_input.setEnabled(not sending)

    def _on_response(self, question, response):
        self._set_sending_state(False)
        self.status_label.setText("")

        self.conversation_history.append({"role": "user", "content": question})
        self.conversation_history.append({"role": "assistant", "content": response})

        self._add_message(response, is_user=False)

    def _on_failed(self, error_message):
        self._set_sending_state(False)
        self.status_label.setText(f"⚠ {error_message}")