import os

import whisper
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QPushButton, QFileDialog, QLineEdit, QCheckBox, QMessageBox,
    QTabWidget, QListWidget, QListWidgetItem
)
from qfluentwidgets import ComboBox

from Core.file_write import write_srt
from const import LANGUAGES


class SubmindGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Submind")
        self.setMinimumSize(580, 460)
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

        self.tabs = QTabWidget(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.tabs)

        # Add tabs
        self.tabs.addTab(self.create_single_tab(), "🎧 Single File")
        self.tabs.addTab(self.create_batch_tab(), "🗂 Batch Files")

    def create_single_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(14)
        layout.setContentsMargins(30, 20, 30, 20)

        label = QLabel("🎙️ Select an audio or video file")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("No file selected...")
        layout.addWidget(self.file_input)

        self.translate_checkbox = QCheckBox("🌍 Auto Translate Subtitles")
        self.translate_checkbox.stateChanged.connect(self.toggle_language_dropdown)
        layout.addWidget(self.translate_checkbox)

        self.lang_dropdown = ComboBox()
        self.lang_dropdown.addItems(LANGUAGES.keys())
        self.lang_dropdown.hide()
        layout.addWidget(self.lang_dropdown)

        self.save_trf_cbox = QCheckBox("🗃️ Save Translated SRT Separately")
        self.save_trf_cbox.hide()
        layout.addWidget(self.save_trf_cbox)

        browse_btn = QPushButton("📂 Browse")
        browse_btn.clicked.connect(self.browse_file)
        layout.addWidget(browse_btn)

        transcribe_btn = QPushButton("📝 Transcribe to SRT")
        transcribe_btn.clicked.connect(self.transcribe)
        layout.addWidget(transcribe_btn, alignment=Qt.AlignmentFlag.AlignBottomz)

        self.status = QLabel("")
        self.status.setObjectName("StatusLabel")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status)

        return tab

    def create_batch_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(14)
        layout.setContentsMargins(30, 20, 30, 20)

        label = QLabel("🗂️ Select multiple audio/video files to transcribe")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        self.batch_list = QListWidget()
        layout.addWidget(self.batch_list)

        browse_btn = QPushButton("📂 Browse Files")
        browse_btn.clicked.connect(self.browse_batch_files)
        layout.addWidget(browse_btn)

        self.batch_translate_checkbox = QCheckBox("🌍 Auto Translate Subtitles")
        self.batch_translate_checkbox.stateChanged.connect(self.toggle_batch_translation_controls)
        layout.addWidget(self.batch_translate_checkbox)

        self.batch_lang_dropdown = ComboBox()
        self.batch_lang_dropdown.addItems(LANGUAGES.keys())
        self.batch_lang_dropdown.hide()
        layout.addWidget(self.batch_lang_dropdown)

        self.batch_save_trf_cbox = QCheckBox("🗃️ Save Translated SRT Separately")
        self.batch_save_trf_cbox.hide()
        layout.addWidget(self.batch_save_trf_cbox)

        start_btn = QPushButton("🚀 Start Batch Transcription")
        start_btn.clicked.connect(self.batch_transcribe)
        layout.addWidget(start_btn)

        self.batch_status = QLabel("")
        self.batch_status.setObjectName("StatusLabel")
        self.batch_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.batch_status)

        return tab

    def toggle_language_dropdown(self):
        show = self.translate_checkbox.isChecked()
        self.lang_dropdown.setVisible(show)
        self.save_trf_cbox.setVisible(show)

    def toggle_batch_translation_controls(self):
        show = self.batch_translate_checkbox.isChecked()
        self.batch_lang_dropdown.setVisible(show)
        self.batch_save_trf_cbox.setVisible(show)

    def browse_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Media File", "", "Media Files (*.mp4 *.mp3 *.wav *.mkv)")
        if path:
            self.file_input.setText(path)

    def browse_batch_files(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Select Media Files", "", "Media Files (*.mp4 *.mp3 *.wav *.mkv)")
        if paths:
            self.batch_list.clear()
            for path in paths:
                self.batch_list.addItem(QListWidgetItem(path))

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
        if save_sep_srt():
            msg += f"\nTranslated subtitles saved to:\n{translated_path}"
        QMessageBox.information(self, "Success", msg)
        self.status.setText("✅ Done!")

    def batch_transcribe(self):
        items = [self.batch_list.item(i).text() for i in range(self.batch_list.count())]
        if not items:
            QMessageBox.warning(self, "No files", "Please select at least one file.")
            return

        self.batch_status.setText("🧠 Processing batch...")
        QApplication.processEvents()

        model = whisper.load_model("base")

        translate = self.batch_translate_checkbox.isChecked()
        save_sep = self.batch_save_trf_cbox.isChecked()
        lang = LANGUAGES.get(self.batch_lang_dropdown.currentText()) if translate else None

        for path in items:
            result = model.transcribe(path)
            base = os.path.splitext(path)[0]
            output_path = base + "_submind.srt"
            write_srt(result, output_path)

            if translate:
                if save_sep:
                    translated_path = base + f"_submind_translated_{lang}.srt"
                else:
                    translated_path = output_path  # Overwrite same file
                write_srt(result, translated_path, lang)

        self.batch_status.setText("✅ All files processed!")
        QMessageBox.information(self, "Done", "All files have been transcribed.")

