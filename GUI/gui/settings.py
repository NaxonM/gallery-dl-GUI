from __future__ import annotations

from PyQt6 import QtWidgets
from typing import Optional

from .config import Config


class SettingsDialog(QtWidgets.QDialog):
    """Dialog to configure application settings."""

    def __init__(self, config: Config, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)
        self._config = config
        self.setWindowTitle("Settings")

        self._path_edit = QtWidgets.QLineEdit(self._config.gallery_dl_path)
        browse_btn = QtWidgets.QPushButton("Browse")
        browse_btn.clicked.connect(self._browse)

        path_layout = QtWidgets.QHBoxLayout()
        path_layout.addWidget(self._path_edit)
        path_layout.addWidget(browse_btn)

        form = QtWidgets.QFormLayout(self)
        form.addRow("gallery-dl executable", path_layout)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self._accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def _browse(self) -> None:
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select gallery-dl executable")
        if path:
            self._path_edit.setText(path)

    def _accept(self) -> None:
        self._config.gallery_dl_path = self._path_edit.text()
        self.accept()
