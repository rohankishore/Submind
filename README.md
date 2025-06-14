<div align="center">

# 🎙️ Submind — AI Subtitle Generator

Submind is a modern, PyQt6-based GUI app powered by OpenAI Whisper. It enables you to **generate perfectly timed subtitles** (SRT files) from any audio or video file, with optional **language translation** and **batch processing**.

![image](https://github.com/user-attachments/assets/b6972908-4986-400f-ba31-b23e36f4db7c)

</div>

---

## 📚 Table of Contents

- [✨ Features](#-features)
- [🖥️ Preview](#-preview)
- [🚀 Getting Started](#-getting-started)
- [🛠️ Usage](#-usage)
  - [🎧 Single File Mode](#-single-file-mode)
  - [🗂️ Batch File Mode](#-batch-file-mode)
- [🌍 Language Support](#-language-support)
- [📦 Dependencies](#-dependencies)
- [📁 Folder Structure](#-folder-structure)
- [🔒 License](#-license)

---

## ✨ Features

- 🎧 **Single File Transcription** — transcribe any media file to subtitles.
- 🗂️ **Batch Mode** — select multiple files and transcribe them at once.
- 🌍 **Auto Translation** — optional translation of subtitles to other languages.
- 🗃️ **Save Separately** — choose to save translated subtitles as separate files.
- 💻 **Clean Dark UI** — modern, minimal dark interface built with PyQt6 + Fluent Widgets.
- 🔊 Powered by OpenAI [Whisper](https://github.com/openai/whisper)


---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/rohankishore/Submind.git
cd submind

### 2. Install requirements

```bash
pip install -r requirements.txt
```

*Make sure [ffmpeg](https://ffmpeg.org/) is installed and added to PATH.*

### 3. Run the app

```bash
python main.py
```

---

## 🛠️ Usage

### 🎧 Single File Mode
- Select any audio/video file.
- Enable translation (optional).
- Choose a language.
- Hit "📝 Transcribe to SRT".

### 🗂️ Batch File Mode
- Click "📂 Browse Files" to select multiple files.
- Enable translation (optional).
- Choose target language.
- Start batch transcription.

---

## 🌍 Language Support

Over 50+ languages supported via OpenAI Whisper translation.

To add/remove options, edit the `LANGUAGES` dictionary in [`const.py`](./const.py).

---

## 📦 Dependencies

- [whisper](https://github.com/openai/whisper)
- PyQt6
- qfluentwidgets
- ffmpeg (system-installed)
- numpy
- torch

You can install them with:

```bash
pip install whisper PyQt6 qfluentwidgets numpy torch
```

---

## 📁 Folder Structure

```
Submind/
├── Core/
│   └── file_write.py       # Function to save SRT from the whisper result
├── assets/
│   └── preview.png         # UI screenshot for README
├── const.py                # Language map
├── main.py                 # Entry point
├── README.md
└── requirements.txt
```

---

## 🔒 License

This project is licensed under the **MIT License**.  
Feel free to use, modify, and distribute it.

---

> Built with ❤️ by [Rohan Kishore](https://github.com/rohankishore)
