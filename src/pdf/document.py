from pathlib import Path

import pymupdf


class PDFDocument:

    def __init__(
        self
    ):

        self.doc = None

        self.file_path = None

    # ==================================================
    # OPEN
    # ==================================================

    def open(
        self,
        file_path
    ):

        self.close()

        path = Path(
            file_path
        )

        if not path.exists():

            raise FileNotFoundError(
                f"File not found:\n{file_path}"
            )

        if path.suffix.lower() != ".pdf":

            raise ValueError(
                "Selected file is not a PDF."
            )

        try:

            document = pymupdf.open(
                str(path)
            )

        except Exception as exc:

            raise RuntimeError(
                f"Unable to open PDF:\n{exc}"
            )

        if document.needs_pass:

            document.close()

            raise PermissionError(
                "This PDF is password protected."
            )

        self.doc = document

        self.file_path = str(
            path
        )

    # ==================================================
    # CLOSE
    # ==================================================

    def close(
        self
    ):

        if self.doc:

            try:

                self.doc.close()

            except Exception:

                pass

        self.doc = None

        self.file_path = None

    # ==================================================
    # IS OPEN
    # ==================================================

    @property
    def is_open(
        self
    ):

        return self.doc is not None

    # ==================================================
    # PAGE COUNT
    # ==================================================

    @property
    def page_count(
        self
    ):

        if not self.doc:

            return 0

        return self.doc.page_count

    # ==================================================
    # GET PAGE
    # ==================================================

    def get_page(
        self,
        page_number
    ):

        if not self.doc:

            raise RuntimeError(
                "No PDF is open."
            )

        if not (
            0 <= page_number
            < self.doc.page_count
        ):

            raise IndexError(
                "Page number out of range."
            )

        return self.doc.load_page(
            page_number
        )

    # ==================================================
    # TABLE OF CONTENTS / BOOKMARKS
    # ==================================================

    def get_toc(self):

        if not self.is_open:
            return []

        try:
            return self.doc.get_toc(simple=True)

        except Exception:
            return []

    # ==================================================
    # SAVE AS
    # ==================================================

    def save_as(
        self,
        file_path
    ):

        if not self.doc:

            raise RuntimeError(
                "No PDF is open."
            )

        self.doc.save(
            str(file_path),
            garbage=4,
            deflate=True
        )

    # ==================================================
    # SAVE CHANGES
    # ==================================================

    def save_changes(
        self
    ):

        if not self.doc:

            raise RuntimeError(
                "No PDF is open."
            )

        if not self.file_path:

            raise RuntimeError(
                "PDF file path is unavailable."
            )

        temp_path = (
            f"{self.file_path}.tmp"
        )

        self.doc.save(
            temp_path,
            garbage=4,
            deflate=True
        )

        self.doc.close()

        Path(
            temp_path
        ).replace(
            self.file_path
        )

        self.doc = pymupdf.open(
            self.file_path
        )

    # ==================================================
    # METADATA
    # ==================================================

    @property
    def metadata(
        self
    ):

        if not self.doc:

            return {}

        return dict(
            self.doc.metadata
            or {}
        )