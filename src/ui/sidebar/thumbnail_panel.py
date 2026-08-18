from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QIcon, QImage, QPixmap
from PySide6.QtWidgets import (
    QListWidget,
    QListWidgetItem,
)

import pymupdf


class ThumbnailPanel(QListWidget):

    page_selected = Signal(int)

    def __init__(self, parent=None):

        super().__init__(parent)

        self.document = None

        self.setViewMode(
            QListWidget.ViewMode.IconMode
        )

        self.setResizeMode(
            QListWidget.ResizeMode.Adjust
        )

        self.setMovement(
            QListWidget.Movement.Static
        )

        self.setIconSize(
            QSize(120, 160)
        )

        self.setSpacing(10)

        self.itemClicked.connect(
            self._item_clicked
        )

    def set_document(self, document):

        self.document = document

        self.clear()

        if (
            not document
            or not document.is_open
        ):
            return

        for page_number in range(
            document.page_count
        ):

            page = document.get_page(
                page_number
            )

            matrix = pymupdf.Matrix(
                0.25,
                0.25
            )

            pixmap = page.get_pixmap(
                matrix=matrix,
                alpha=False
            )

            image = QImage(
                pixmap.samples,
                pixmap.width,
                pixmap.height,
                pixmap.stride,
                QImage.Format.Format_RGB888
            ).copy()

            thumbnail = QPixmap.fromImage(
                image
            )

            item = QListWidgetItem(
                QIcon(thumbnail),
                f"Page {page_number + 1}"
            )

            item.setTextAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            item.setData(
                Qt.ItemDataRole.UserRole,
                page_number
            )

            self.addItem(item)

    def _item_clicked(self, item):

        page_number = item.data(
            Qt.ItemDataRole.UserRole
        )

        if page_number is not None:

            self.page_selected.emit(
                page_number
            )

    def select_page(self, page_number):

        if (
            0 <= page_number
            < self.count()
        ):

            self.setCurrentRow(
                page_number
            )