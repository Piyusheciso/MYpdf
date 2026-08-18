from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QToolButton


class IconButton(QToolButton):

    def __init__(
        self,
        icon,
        tooltip,
        parent=None
    ):

        super().__init__(
            parent
        )

        # ==================================================
        # ICON
        # ==================================================

        self.setIcon(
            icon
        )

        self.setIconSize(
            QSize(
                22,
                22
            )
        )

        # ==================================================
        # SIZE
        # ==================================================

        self.setFixedSize(
            44,
            44
        )

        # ==================================================
        # TOOLTIP
        # ==================================================

        self.setToolTip(
            tooltip
        )

        # ==================================================
        # CURSOR
        # ==================================================

        self.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        # ==================================================
        # STYLE
        # ==================================================

        self.setStyleSheet(
            """
            QToolButton {
                background-color: white;
                color: black;
                border: 1px solid #d0d0d0;
                border-radius: 7px;
                margin: 2px;
            }

            QToolButton:hover {
                background-color: #f1f1f1;
                border: 1px solid #777777;
            }

            QToolButton:pressed {
                background-color: #dedede;
                border: 1px solid #444444;
            }

            QToolButton:checked {
                background-color: #e8e8e8;
                border: 1px solid #333333;
            }
            """
        )