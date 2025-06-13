import sys

from PyQt6.QtWidgets import QApplication
import window


def main():
    app = QApplication(sys.argv)
    win = window.SubmindGUI()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
