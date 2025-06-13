import os

import whisper
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QPushButton, QFileDialog, QLineEdit, QCheckBox, QMessageBox,
    QTabWidget, QListWidget, QListWidgetItem
)
from qfluentwidgets import ComboBox

from .file_write import write_srt
from ..const import LANGUAGES


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

