import whisper
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QPushButton, QFileDialog, QLineEdit, QCheckBox, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import os
from datetime import timedelta
import sys
import googletrans
from qfluentwidgets import ComboBox

from const import LANGUAGES
from Core.file_write import write_srt


class SubmindGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Submind")
        self.setMinimumSize(520, 400)
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', sans-serif;
                background-color: #1e1e1e;
                color: #f0f0f0;
                font-size: 15px;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #555;
                border-radius: 8px;
                background-color: #2c2c2c;
                color: #f0f0f0;
            }
            QPushButton {
                padding: 10px;
                border: none;
                border-radius: 8px;
                background-color: #3a9ff3;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #60b7ff;
            }
            QCheckBox {
                padding: 6px;
            }
            QLabel#StatusLabel {
                font-size: 13px;
                color: #bbbbbb;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(14)
        layout.setContentsMargins(30, 20, 30, 20)

        label = QLabel("🎙️ Select an audio or video file")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("No file selected...")
        layout.addWidget(self.file_input)

        # Auto Translate Checkbox
        self.translate_checkbox = QCheckBox("🌍 Auto Translate Subtitles")
        self.translate_checkbox.stateChanged.connect(self.toggle_language_dropdown)
        layout.addWidget(self.translate_checkbox)

        # Language Selector Dropdown
        self.lang_dropdown = ComboBox()
        self.lang_dropdown.addItems(LANGUAGES.keys())
        self.lang_dropdown.hide()  # Initially hidden
        layout.addWidget(self.lang_dropdown)

        self.save_trf_cbox = QCheckBox("🗃️ Save Translated SRT Separately")
        self.save_trf_cbox.hide()
        layout.addWidget(self.save_trf_cbox)

        browse_btn = QPushButton("📂 Browse")
        browse_btn.clicked.connect(self.browse_file)
        layout.addWidget(browse_btn)

        transcribe_btn = QPushButton("📝 Transcribe to SRT")
        transcribe_btn.clicked.connect(self.transcribe)
        layout.addWidget(transcribe_btn)

        self.status = QLabel("")
        self.status.setObjectName("StatusLabel")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status)

        self.setLayout(layout)

    def browse_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Media File", "", "Media Files (*.mp4 *.mp3 *.wav *.mkv)")
        if path:
            self.file_input.setText(path)

    def toggle_language_dropdown(self):
        is_checked = self.translate_checkbox.isChecked()
        if is_checked:
            self.save_trf_cbox.show()
            self.lang_dropdown.show()
        else:
            self.save_trf_cbox.hide()
            self.lang_dropdown.hide()

    def transcribe(self):
        global translated_path
        path = self.file_input.text()
        if not os.path.exists(path):
            QMessageBox.critical(self, "Error", "Please select a valid file.")
            return

        self.status.setText("🔊 Loading model...")
        QApplication.processEvents()
        model = whisper.load_model("base")

        self.status.setText("🧠 Transcribing...")
        QApplication.processEvents()
        result = model.transcribe(path)

        output_path = os.path.splitext(path)[0] + "_submind.srt"
        translate_to = None
        if self.translate_checkbox.isChecked():
            selected_lang = self.lang_dropdown.currentText()
            translate_to = LANGUAGES.get(selected_lang)
        write_srt(result, output_path)

        save_sep_srt = self.save_trf_cbox.isChecked()

        if save_sep_srt:
            selected_lang = self.lang_dropdown.currentText()
            translate_to = LANGUAGES.get(selected_lang)
            translated_path = os.path.splitext(path)[0] + f"_submind_translated_{translate_to}.srt"
            write_srt(result, translated_path, translate_to)

        self.status.setText("✅ Done! Saved to:\n" + output_path)

        msg = f"Original subtitles saved to:\n{output_path}"
        if self.translate_checkbox.isChecked():
            msg += f"\nTranslated subtitles saved to:\n{translated_path}"
        QMessageBox.information(self, "Success", msg)
        self.status.setText("✅ Done!")
