from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QToolBar,
    QToolButton,
)


class AnnotationToolbar(QToolBar):

    highlight_requested = Signal()

    underline_requested = Signal()

    strikeout_requested = Signal()

    squiggly_requested = Signal()

    text_note_requested = Signal()

    delete_requested = Signal()

    close_requested = Signal()

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            "Annotations",
            parent
        )

        self.setMovable(
            False
        )

        self.setFloatable(
            False
        )

        self.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonTextOnly
        )

        self.create_buttons()

    # ==================================================
    # BUTTONS
    # ==================================================

    def create_buttons(
        self
    ):

        # --------------------------------------------------
        # Highlight
        # --------------------------------------------------

        self.highlight_button = (
            self.create_button(
                "Highlight"
            )
        )

        self.highlight_button.clicked.connect(
            self.highlight_requested.emit
        )

        self.addWidget(
            self.highlight_button
        )

        # --------------------------------------------------
        # Underline
        # --------------------------------------------------

        self.underline_button = (
            self.create_button(
                "Underline"
            )
        )

        self.underline_button.clicked.connect(
            self.underline_requested.emit
        )

        self.addWidget(
            self.underline_button
        )

        # --------------------------------------------------
        # Strikeout
        # --------------------------------------------------

        self.strikeout_button = (
            self.create_button(
                "Strikeout"
            )
        )

        self.strikeout_button.clicked.connect(
            self.strikeout_requested.emit
        )

        self.addWidget(
            self.strikeout_button
        )

        # --------------------------------------------------
        # Squiggly
        # --------------------------------------------------

        self.squiggly_button = (
            self.create_button(
                "Squiggly"
            )
        )

        self.squiggly_button.clicked.connect(
            self.squiggly_requested.emit
        )

        self.addWidget(
            self.squiggly_button
        )

        # --------------------------------------------------
        # Text note
        # --------------------------------------------------

        self.text_note_button = (
            self.create_button(
                "Text Note"
            )
        )

        self.text_note_button.clicked.connect(
            self.text_note_requested.emit
        )

        self.addWidget(
            self.text_note_button
        )

        self.addSeparator()

        # --------------------------------------------------
        # Delete
        # --------------------------------------------------

        self.delete_button = (
            self.create_button(
                "Delete"
            )
        )

        self.delete_button.clicked.connect(
            self.delete_requested.emit
        )

        self.addWidget(
            self.delete_button
        )

        self.addSeparator()

        # --------------------------------------------------
        # Close
        # --------------------------------------------------

        self.close_button = (
            self.create_button(
                "Close"
            )
        )

        self.close_button.clicked.connect(
            self.close_requested.emit
        )

        self.addWidget(
            self.close_button
        )

    # ==================================================
    # CREATE BUTTON
    # ==================================================

    def create_button(
        self,
        text
    ):

        button = QToolButton(
            self
        )

        button.setText(
            text
        )

        button.setToolTip(
            text
        )

        button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        return button