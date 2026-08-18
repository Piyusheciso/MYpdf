import pymupdf


class PDFPageTools:

    def __init__(
        self,
        document
    ):

        self.document = document

    # ==================================================
    # ROTATE
    # ==================================================

    def rotate_page(
        self,
        page_number,
        degrees=90
    ):

        if not self._valid(
            page_number
        ):
            return False

        page = self.document.get_page(
            page_number
        )

        current = page.rotation

        page.set_rotation(
            (
                current
                + degrees
            ) % 360
        )

        return True

    # ==================================================
    # DELETE
    # ==================================================

    def delete_page(
        self,
        page_number
    ):

        if not self._valid(
            page_number
        ):
            return False

        if (
            self.document.page_count
            <= 1
        ):

            raise ValueError(
                "A PDF must contain at least one page."
            )

        self.document.doc.delete_page(
            page_number
        )

        return True

    # ==================================================
    # EXTRACT
    # ==================================================

    def extract_pages(
        self,
        start_page,
        end_page,
        output_path
    ):

        if not self.document:
            return False

        if not self.document.is_open:
            return False

        if start_page < 0:
            return False

        if end_page >= self.document.page_count:
            return False

        if start_page > end_page:
            return False

        new_doc = pymupdf.open()

        new_doc.insert_pdf(
            self.document.doc,
            from_page=start_page,
            to_page=end_page
        )

        new_doc.save(
            output_path
        )

        new_doc.close()

        return True

    # ==================================================
    # INSERT BLANK PAGE
    # ==================================================

    def insert_blank_page(
        self,
        page_number=None,
        width=595,
        height=842
    ):

        if not self.document:
            return False

        if not self.document.is_open:
            return False

        if page_number is None:

            page_number = (
                self.document.page_count
            )

        self.document.doc.new_page(
            pno=page_number,
            width=width,
            height=height
        )

        return True

    # ==================================================
    # VALID
    # ==================================================

    def _valid(
        self,
        page_number
    ):

        if not self.document:
            return False

        if not self.document.is_open:
            return False

        return (
            0 <= page_number
            < self.document.page_count
        )