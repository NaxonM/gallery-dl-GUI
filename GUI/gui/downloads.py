from __future__ import annotations

from urllib.parse import urlparse
import subprocess

from PyQt6 import QtWidgets, QtGui


class BatchUrlEdit(QtWidgets.QPlainTextEdit):
    """Multiline input widget for batch URLs with validation."""

    def __init__(
        self,
        gallery_dl_path: str,
        parent: QtWidgets.QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._gallery_dl_path = gallery_dl_path
        self._supported: set[str] | None = None
        self._unsupported_lines: set[int] = set()
        self.setPlaceholderText("Enter one URL per line")
        self.viewport().setMouseTracking(True)
        self.textChanged.connect(self._validate)

    def _load_supported(self) -> None:
        if self._supported is not None:
            return
        try:
            proc = subprocess.run(
                [self._gallery_dl_path, "--list-extractors"],
                capture_output=True,
                text=True,
                check=True,
            )
        except Exception:
            self._supported = set()
            return
        domains: set[str] = set()
        for line in proc.stdout.splitlines():
            if line.startswith("Example :"):
                url = line.split("Example :", 1)[1].strip()
                netloc = urlparse(url).netloc.lower()
                if netloc:
                    domains.add(netloc)
        self._supported = domains

    def _is_supported(self, url: str) -> bool:
        self._load_supported()
        if not url:
            return True
        if not self._supported:
            return True
        netloc = urlparse(url).netloc.lower()
        return any(
            netloc == d or netloc.endswith("." + d) for d in self._supported
        )

    def _validate(self) -> None:
        lines = self.toPlainText().splitlines()
        self._unsupported_lines = {
            i
            for i, line in enumerate(lines)
            if line.strip() and not self._is_supported(line.strip())
        }
        selections: list[QtWidgets.QTextEdit.ExtraSelection] = []
        for line_no in self._unsupported_lines:
            selection = QtWidgets.QTextEdit.ExtraSelection()
            selection.format.setForeground(QtGui.QColor("red"))
            cursor = QtGui.QTextCursor(
                self.document().findBlockByNumber(line_no)
            )
            cursor.select(QtGui.QTextCursor.SelectionType.LineUnderCursor)
            selection.cursor = cursor
            selections.append(selection)
        self.setExtraSelections(selections)

    def mouseMoveEvent(
        self, event: QtGui.QMouseEvent
    ) -> None:  # pragma: no cover - GUI
        super().mouseMoveEvent(event)
        cursor = self.cursorForPosition(event.position().toPoint())
        line = cursor.blockNumber()
        if line in self._unsupported_lines:
            QtWidgets.QToolTip.showText(
                event.globalPosition().toPoint(),
                "Unsupported URL",
                self,
            )
        else:
            QtWidgets.QToolTip.hideText()


class DownloadsTab(QtWidgets.QWidget):
    """Downloads tab containing a batch URL editor."""

    def __init__(
        self,
        gallery_dl_path: str,
        parent: QtWidgets.QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        self.url_edit = BatchUrlEdit(gallery_dl_path)
        layout.addWidget(self.url_edit)
        submit = QtWidgets.QPushButton("Submit")
        submit.clicked.connect(self.url_edit._validate)
        layout.addWidget(submit)
        layout.addStretch()
