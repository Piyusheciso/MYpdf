from collections import OrderedDict

from PySide6.QtGui import QPixmap


class RenderCache:
    """
    Small LRU cache for rendered PDF pages.

    The cache stores rendered QPixmaps so that
    scrolling back to recently viewed pages does
    not require rendering them again.
    """

    def __init__(self, max_items=12):

        self.max_items = max_items

        self._cache = OrderedDict()

    # ==================================================
    # GET
    # ==================================================

    def get(self, key):

        if key not in self._cache:
            return None

        value = self._cache.pop(key)

        # Move recently used item to the end.
        self._cache[key] = value

        return value

    # ==================================================
    # PUT
    # ==================================================

    def put(self, key, pixmap: QPixmap):

        if key in self._cache:

            self._cache.pop(key)

        self._cache[key] = pixmap

        while len(self._cache) > self.max_items:

            self._cache.popitem(
                last=False
            )

    # ==================================================
    # REMOVE
    # ==================================================

    def remove(self, key):

        self._cache.pop(
            key,
            None
        )

    # ==================================================
    # CLEAR
    # ==================================================

    def clear(self):

        self._cache.clear()

    # ==================================================
    # SIZE
    # ==================================================

    def __len__(self):

        return len(
            self._cache
        )