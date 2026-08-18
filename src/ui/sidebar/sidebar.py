from PySide6.QtWidgets import (
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from src.ui.sidebar.thumbnail_panel import (
    ThumbnailPanel
)

from src.ui.sidebar.outline_panel import (
    OutlinePanel
)


class Sidebar(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.thumbnails = ThumbnailPanel()

        self.outline = OutlinePanel()

        self.tabs = QTabWidget()

        self.tabs.addTab(
            self.thumbnails,
            "Pages"
        )

        self.tabs.addTab(
            self.outline,
            "Outline"
        )

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout.addWidget(
            self.tabs
        )

    def set_document(self, document):

        self.thumbnails.set_document(
            document
        )

        self.outline.set_document(
            document
        )

    def select_page(self, page_number):

        self.thumbnails.select_page(
            page_number
        )