from dataclasses import dataclass


@dataclass
class SearchResult:
    """
    Represents one search result inside a PDF.
    """

    page_number: int
    rect: object
    text: str


class PDFTextSearch:

    def __init__(self, document=None):

        self.document = document

    # ==================================================
    # SET DOCUMENT
    # ==================================================

    def set_document(self, document):

        self.document = document

    # ==================================================
    # SEARCH
    # ==================================================

    def search(
        self,
        query: str,
        case_sensitive: bool = False
    ):

        results = []

        if not self.document:
            return results

        if not self.document.is_open:
            return results

        query = query.strip()

        if not query:
            return results

        for page_number in range(
            self.document.page_count
        ):

            page = self.document.get_page(
                page_number
            )

            # PyMuPDF's search_for handles
            # text searching and returns
            # rectangles around matches.
            matches = page.search_for(
                query
            )

            if matches:

                for rect in matches:

                    results.append(
                        SearchResult(
                            page_number=page_number,
                            rect=rect,
                            text=query
                        )
                    )

        if case_sensitive:
            return results

        return results