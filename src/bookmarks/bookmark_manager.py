class BookmarkManager:

    def __init__(self):

        self.bookmarks = []

    # ==================================================
    # ADD
    # ==================================================

    def add_bookmark(
        self,
        page_number,
        title=None
    ):

        if self.is_bookmarked(page_number):
            return False

        bookmark = {
            "page": page_number,
            "title": (
                title
                if title
                else f"Page {page_number + 1}"
            )
        }

        self.bookmarks.append(
            bookmark
        )

        self.bookmarks.sort(
            key=lambda item: item["page"]
        )

        return True

    # ==================================================
    # REMOVE
    # ==================================================

    def remove_bookmark(
        self,
        page_number
    ):

        for bookmark in self.bookmarks:

            if bookmark["page"] == page_number:

                self.bookmarks.remove(
                    bookmark
                )

                return True

        return False

    # ==================================================
    # TOGGLE
    # ==================================================

    def toggle_bookmark(
        self,
        page_number
    ):

        if self.is_bookmarked(
            page_number
        ):

            self.remove_bookmark(
                page_number
            )

            return False

        self.add_bookmark(
            page_number
        )

        return True

    # ==================================================
    # CHECK
    # ==================================================

    def is_bookmarked(
        self,
        page_number
    ):

        return any(
            bookmark["page"] == page_number
            for bookmark in self.bookmarks
        )

    # ==================================================
    # GET
    # ==================================================

    def get_bookmarks(self):

        return list(
            self.bookmarks
        )

    # ==================================================
    # CLEAR
    # ==================================================

    def clear(self):

        self.bookmarks.clear()