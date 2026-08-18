from pathlib import Path

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QVBoxLayout,
)


class DocumentInfoDialog(
    QDialog
):

    def __init__(
        self,
        parent,
        pdf_document
    ):

        super().__init__(
            parent
        )

        self.pdf_document = (
            pdf_document
        )

        self.setWindowTitle(
            "Document Information"
        )

        self.setMinimumWidth(
            450
        )

        self.create_ui()

    # ==================================================
    # UI
    # ==================================================

    def create_ui(
        self
    ):

        layout = QVBoxLayout(
            self
        )

        form = QFormLayout()

        file_path = (
            self.pdf_document.file_path
        )

        filename = (
            Path(file_path).name
            if file_path
            else "Unknown"
        )

        # --------------------------------------------------
        # Filename
        # --------------------------------------------------

        form.addRow(
            "Filename:",
            QLabel(filename)
        )

        # --------------------------------------------------
        # Path
        # --------------------------------------------------

        form.addRow(
            "Location:",
            QLabel(
                file_path
                if file_path
                else "Unknown"
            )
        )

        # --------------------------------------------------
        # Pages
        # --------------------------------------------------

        form.addRow(
            "Pages:",
            QLabel(
                str(
                    self.pdf_document.page_count
                )
            )
        )

        # --------------------------------------------------
        # File size
        # --------------------------------------------------

        try:

            size = Path(
                file_path
            ).stat().st_size

            size_mb = (
                size / (1024 * 1024)
            )

            size_text = (
                f"{size_mb:.2f} MB"
            )

        except Exception:

            size_text = "Unknown"

        form.addRow(
            "File size:",
            QLabel(size_text)
        )

        # --------------------------------------------------
        # Metadata
        # --------------------------------------------------

        metadata = {}

        try:

            metadata = (
                self.pdf_document.document.metadata
                or {}
            )

        except Exception:

            pass

        form.addRow(
            "Title:",
            QLabel(
                metadata.get(
                    "title",
                    ""
                )
                or "—"
            )
        )

        form.addRow(
            "Author:",
            QLabel(
                metadata.get(
                    "author",
                    ""
                )
                or "—"
            )
        )

        form.addRow(
            "Subject:",
            QLabel(
                metadata.get(
                    "subject",
                    ""
                )
                or "—"
            )
        )

        form.addRow(
            "Creator:",
            QLabel(
                metadata.get(
                    "creator",
                    ""
                )
                or "—"
            )
        )

        layout.addLayout(
            form
        )

        # --------------------------------------------------
        # Buttons
        # --------------------------------------------------

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
        )

        buttons.accepted.connect(
            self.accept
        )

        layout.addWidget(
            buttons
        )