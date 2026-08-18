from pathlib import Path


class PDFMetadata:

    def __init__(self, document=None):

        self.document = document

    def set_document(self, document):

        self.document = document

    def get_metadata(self):

        if self.document is None:
            return {}

        try:

            metadata = self.document.metadata

            return {
                "title": metadata.get("title", ""),
                "author": metadata.get("author", ""),
                "subject": metadata.get("subject", ""),
                "keywords": metadata.get("keywords", ""),
                "creator": metadata.get("creator", ""),
                "producer": metadata.get("producer", ""),
                "creation_date": metadata.get("creationDate", ""),
                "modification_date": metadata.get("modDate", ""),
            }

        except Exception:

            return {}

    def get_file_info(self):

        if self.document is None:
            return {}

        try:

            path = Path(self.document.name)

            return {
                "filename": path.name,
                "path": str(path),
                "size": path.stat().st_size,
                "pages": len(self.document),
            }

        except Exception:

            return {}