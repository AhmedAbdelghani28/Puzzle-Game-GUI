from __future__ import annotations

from typing import Any, Callable

from PyQt6.QtCore import QThread, pyqtSignal


class Worker(QThread):
    """Runs *fn* on a background thread and emits its return value on *finished*."""

    finished: pyqtSignal = pyqtSignal(object)

    def __init__(self, fn: Callable[[], Any]) -> None:
        super().__init__()
        self._fn = fn

    def run(self) -> None:
        self.finished.emit(self._fn())
