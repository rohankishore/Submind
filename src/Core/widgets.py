from PyQt6.QtWidgets import (
    QLineEdit, QListWidget, QListWidgetItem
)


class DraggableLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if not urls:
            return

        paths = [url.toLocalFile() for url in urls if url.isLocalFile()]
        media_exts = (".mp4", ".mp3", ".wav", ".mkv")

        valid_files = [p for p in paths if p.lower().endswith(media_exts)]
        if valid_files:
            self.setText(valid_files[0])

class DraggableListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if not urls:
            return

        paths = [url.toLocalFile() for url in urls if url.isLocalFile()]
        media_exts = (".mp4", ".mp3", ".wav", ".mkv")

        valid_files = [p for p in paths if p.lower().endswith(media_exts)]
        if valid_files:
            self.clear()
            for path in valid_files:
                self.addItem(QListWidgetItem(path))
