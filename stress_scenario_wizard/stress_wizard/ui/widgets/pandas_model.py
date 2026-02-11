from __future__ import annotations

from typing import Any

import pandas as pd
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt


class LazyDataFrameModel(QAbstractTableModel):
    """Pandas-backed table model with incremental row fetching for large datasets."""

    def __init__(self, frame: pd.DataFrame | None = None, batch_size: int = 2000) -> None:
        super().__init__()
        self._frame = frame.copy() if frame is not None else pd.DataFrame()
        self._batch_size = batch_size
        self._loaded_rows = min(len(self._frame), self._batch_size)

    def set_frame(self, frame: pd.DataFrame) -> None:
        self.beginResetModel()
        self._frame = frame.copy()
        self._loaded_rows = min(len(self._frame), self._batch_size)
        self.endResetModel()

    @property
    def frame(self) -> pd.DataFrame:
        return self._frame

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:  # noqa: N802
        if parent.isValid():
            return 0
        return self._loaded_rows

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:  # noqa: N802
        if parent.isValid():
            return 0
        return len(self._frame.columns)

    def canFetchMore(self, parent: QModelIndex = QModelIndex()) -> bool:  # noqa: N802
        return self._loaded_rows < len(self._frame)

    def fetchMore(self, parent: QModelIndex = QModelIndex()) -> None:  # noqa: N802
        remainder = len(self._frame) - self._loaded_rows
        items_to_fetch = min(self._batch_size, remainder)
        if items_to_fetch <= 0:
            return
        start = self._loaded_rows
        end = self._loaded_rows + items_to_fetch - 1
        self.beginInsertRows(QModelIndex(), start, end)
        self._loaded_rows += items_to_fetch
        self.endInsertRows()

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:  # noqa: N802
        if not index.isValid():
            return None
        if role in {Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole}:
            value = self._frame.iat[index.row(), index.column()]
            if isinstance(value, float):
                return f"{value:,.6g}"
            return str(value)
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole) -> Any:  # noqa: N802
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            if section < len(self._frame.columns):
                return str(self._frame.columns[section])
        return str(section + 1)
