from pathlib import Path

from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QToolButton,
    QSizePolicy,
)


class RightPanel(QWidget):

    # ==================================================
    # SIGNALS
    # ==================================================

    search_requested = Signal()

    bookmark_requested = Signal()

    annotation_requested = Signal()

    download_requested = Signal()

    print_requested = Signal()

    info_requested = Signal()

    # ==================================================
    # INIT
    # ==================================================

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )

        # --------------------------------------------------
        # PANEL
        # --------------------------------------------------

        self.setFixedWidth(
            58
        )

        self.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Expanding
        )

        self.setObjectName(
            "RightPanel"
        )

        # --------------------------------------------------
        # ICON DIRECTORY
        # --------------------------------------------------

        self.icons_dir = (
            Path(__file__).resolve().parent
            / "icons"
        )

        # --------------------------------------------------
        # UI
        # --------------------------------------------------

        self.create_ui()

        self.apply_style()

    # ==================================================
    # UI
    # ==================================================

    def create_ui(
        self
    ):

        self.layout = QVBoxLayout(
            self
        )

        self.layout.setContentsMargins(
            6,
            10,
            6,
            10
        )

        self.layout.setSpacing(
            8
        )

        # ==================================================
        # SEARCH
        # ==================================================

        self.search_button = (
            self.create_button(
                "search.svg",
                "Search"
            )
        )

        self.search_button.clicked.connect(
            self.search_requested.emit
        )

        self.layout.addWidget(
            self.search_button
        )

        # ==================================================
        # BOOKMARK
        # ==================================================

        self.bookmark_button = (
            self.create_button(
                "bookmark.svg",
                "Bookmarks"
            )
        )

        self.bookmark_button.clicked.connect(
            self.bookmark_requested.emit
        )

        self.layout.addWidget(
            self.bookmark_button
        )

        # ==================================================
        # ANNOTATION
        # ==================================================

        self.annotation_button = (
            self.create_button(
                "annotation.svg",
                "Annotations"
            )
        )

        # Annotation is ENABLED.
        self.annotation_button.setEnabled(
            True
        )

        self.annotation_button.clicked.connect(
            self.annotation_requested.emit
        )

        self.layout.addWidget(
            self.annotation_button
        )

        # ==================================================
        # SAVE / DOWNLOAD
        # ==================================================

        self.download_button = (
            self.create_button(
                "download.svg",
                "Save / Download"
            )
        )

        self.download_button.clicked.connect(
            self.download_requested.emit
        )

        self.layout.addWidget(
            self.download_button
        )

        # ==================================================
        # PRINT
        # ==================================================

        self.print_button = (
            self.create_button(
                "print.svg",
                "Print"
            )
        )

        self.print_button.clicked.connect(
            self.print_requested.emit
        )

        self.layout.addWidget(
            self.print_button
        )

        # ==================================================
        # SPACER
        # ==================================================

        self.layout.addStretch(
            1
        )

        # ==================================================
        # INFORMATION
        # ==================================================

        self.info_button = (
            self.create_button(
                "info.svg",
                "Document Information"
            )
        )

        self.info_button.clicked.connect(
            self.info_requested.emit
        )

        self.layout.addWidget(
            self.info_button
        )

    # ==================================================
    # CREATE BUTTON
    # ==================================================

    def create_button(
        self,
        icon_name,
        tooltip
    ):

        button = QToolButton(
            self
        )

        button.setFixedSize(
            44,
            44
        )

        button.setIconSize(
            QSize(
                22,
                22
            )
        )

        # --------------------------------------------------
        # ICON
        # --------------------------------------------------

        icon_path = (
            self.icons_dir
            / icon_name
        )

        if icon_path.exists():

            button.setIcon(
                QIcon(
                    str(icon_path)
                )
            )

        else:

            print(
                "Warning: icon not found:",
                icon_path
            )

        # --------------------------------------------------
        # TOOLTIP
        # --------------------------------------------------

        button.setToolTip(
            tooltip
        )

        button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        button.setFocusPolicy(
            Qt.FocusPolicy.NoFocus
        )

        button.setAutoRaise(
            False
        )

        button.setObjectName(
            "RightPanelButton"
        )

        return button

    # ==================================================
    # STYLE
    # ==================================================

    def apply_style(
        self
    ):

        self.setStyleSheet(
            """
            #RightPanel {

                background-color: #ffffff;

                border-left: 1px solid #d0d0d0;
            }

            QToolButton#RightPanelButton {

                background-color: #ffffff;

                border: 1px solid #d0d0d0;

                border-radius: 6px;

                padding: 5px;
            }

            QToolButton#RightPanelButton:hover {

                background-color: #f0f0f0;

                border: 1px solid #000000;
            }

            QToolButton#RightPanelButton:pressed {

                background-color: #e0e0e0;

                border: 1px solid #000000;
            }

            QToolButton#RightPanelButton:disabled {

                background-color: #f5f5f5;

                border: 1px solid #dddddd;

                opacity: 0.45;
            }

            QToolTip {

                background-color: #000000;

                color: #ffffff;

                border: 1px solid #ffffff;

                padding: 5px 8px;

                font-size: 10pt;
            }
            """
        )

    # ==================================================
    # ENABLE / DISABLE
    # ==================================================

    def set_document_open(
        self,
        is_open
    ):

        # --------------------------------------------------
        # BOOKMARKS
        # --------------------------------------------------

        self.bookmark_button.setEnabled(
            is_open
        )

        # --------------------------------------------------
        # ANNOTATIONS
        # --------------------------------------------------

        self.annotation_button.setEnabled(
            is_open
        )

        # --------------------------------------------------
        # DOWNLOAD
        # --------------------------------------------------

        self.download_button.setEnabled(
            is_open
        )

        # --------------------------------------------------
        # PRINT
        # --------------------------------------------------

        self.print_button.setEnabled(
            is_open
        )

        # --------------------------------------------------
        # INFORMATION
        # --------------------------------------------------

        self.info_button.setEnabled(
            is_open
        )