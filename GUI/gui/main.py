from pathlib import Path

from PyQt6 import QtWidgets
import qdarktheme

from .config import Config
from .downloader import ensure_gallery_dl
from .settings import SettingsDialog
from .downloads import DownloadsTab


class MainWindow(QtWidgets.QMainWindow):
    """Main application window."""

    def __init__(self, config: Config) -> None:
        super().__init__()
        self._config = config
        self.setWindowTitle("gallery-dl GUI")
        self.resize(800, 600)

        # Central tab widget
        tabs = QtWidgets.QTabWidget()
        self.setCentralWidget(tabs)

        downloads_tab = DownloadsTab(self._config.gallery_dl_path)
        tabs.addTab(downloads_tab, "Downloads")
        tabs.addTab(QtWidgets.QWidget(), "Options")
        tabs.addTab(QtWidgets.QWidget(), "History/Logs")

        settings_tab = QtWidgets.QWidget()
        settings_layout = QtWidgets.QVBoxLayout(settings_tab)
        open_settings_button = QtWidgets.QPushButton("Open Settings…")
        open_settings_button.clicked.connect(self._show_settings)
        settings_layout.addWidget(open_settings_button)
        settings_layout.addStretch()
        tabs.addTab(settings_tab, "Settings")

        # Toolbar
        settings_action = QtWidgets.QAction("Settings", self)
        settings_action.triggered.connect(self._show_settings)
        toolbar = self.addToolBar("Main")
        toolbar.addAction(settings_action)

        # Status bar
        self.statusBar().showMessage("Ready")

    def _show_settings(self) -> None:
        dialog = SettingsDialog(self._config, self)
        if dialog.exec():
            self._config.save()
            ensure_gallery_dl(Path(self._config.gallery_dl_path))


def main() -> None:
    """Launch the gallery-dl GUI."""
    app = QtWidgets.QApplication([])
    qdarktheme.setup_theme()
    config = Config.load()
    ensure_gallery_dl(Path(config.gallery_dl_path))
    window = MainWindow(config)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
