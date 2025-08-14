from PyQt6 import QtWidgets
from pathlib import Path

from .config import Config
from .downloader import ensure_gallery_dl
from .settings import SettingsDialog


class MainWindow(QtWidgets.QMainWindow):
    """Main application window."""

    def __init__(self, config: Config) -> None:
        super().__init__()
        self._config = config
        self.setWindowTitle("gallery-dl GUI")
        self.resize(800, 600)

        settings_action = QtWidgets.QAction("Settings", self)
        settings_action.triggered.connect(self._show_settings)
        menu = self.menuBar().addMenu("Options")
        menu.addAction(settings_action)

    def _show_settings(self) -> None:
        dialog = SettingsDialog(self._config, self)
        if dialog.exec():
            self._config.save()
            ensure_gallery_dl(Path(self._config.gallery_dl_path))


def main() -> None:
    """Launch the gallery-dl GUI."""
    app = QtWidgets.QApplication([])
    config = Config.load()
    ensure_gallery_dl(Path(config.gallery_dl_path))
    window = MainWindow(config)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
