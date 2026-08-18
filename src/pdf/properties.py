class PDFProperties:

    def __init__(
        self,
        document
    ):

        self.document = document

    def get_metadata(self):

        if not self.document:
            return {}

        if not self.document.is_open:
            return {}

        return dict(
            self.document.doc.metadata
            or {}
        )

    def update_metadata(
        self,
        metadata
    ):

        if not self.document:
            return False

        if not self.document.is_open:
            return False

        try:

            self.document.doc.set_metadata(
                metadata
            )

            return True

        except Exception:

            return False