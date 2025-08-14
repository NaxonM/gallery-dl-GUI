from PyQt6 import QtWidgets


def main() -> None:
    """Launch the gallery-dl GUI."""
    app = QtWidgets.QApplication([])
    window = QtWidgets.QMainWindow()
    window.setWindowTitle("gallery-dl GUI")
    window.resize(800, 600)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
