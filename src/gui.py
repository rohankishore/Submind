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

def format_timestamp(seconds):
    milliseconds = int((seconds - int(seconds)) * 1000)
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"

def write_srt(transcription, output_path, single_speaker=False):
    with open(output_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(transcription["segments"], 1):
            f.write(f"{i}\n")
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = segment["text"].strip()
            line = text if single_speaker else f"[Speaker ?]: {text}"
            f.write(f"{start} --> {end}\n")
            f.write(f"{line}\n\n")

class SubmindGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Submind 🎬")
        self.setFixedSize(420, 300)
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

        browse_btn = QPushButton("📂 Browse")
        browse_btn.clicked.connect(self.browse_file)
        layout.addWidget(browse_btn)

        self.single_checkbox = QCheckBox("🧍 Single Speaker (no tags)")
        layout.addWidget(self.single_checkbox)

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

    def transcribe(self):
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
        write_srt(result, output_path, self.single_checkbox.isChecked())

        self.status.setText("✅ Done! Saved to:\n" + output_path)
        QMessageBox.information(self, "Success", f"Subtitles saved to:\n{output_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = SubmindGUI()
    gui.show()
    sys.exit(app.exec())
