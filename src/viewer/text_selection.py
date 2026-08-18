from PySide6.QtCore import QRectF
from PySide6.QtGui import QColor, QPen
from PySide6.QtWidgets import QGraphicsRectItem


class TextSelection:

    def __init__(
        self,
        scene
    ):

        self.scene = scene

        self.items = []

        self.start_page = None
        self.start_word = None

        self.end_page = None
        self.end_word = None

        self.selected_words = []

    # ==================================================
    # CLEAR
    # ==================================================

    def clear(self):

        for item in self.items:

            try:

                self.scene.removeItem(
                    item
                )

            except RuntimeError:
                pass

        self.items.clear()

        self.start_page = None
        self.start_word = None

        self.end_page = None
        self.end_word = None

        self.selected_words = []

    # ==================================================
    # SET SELECTION
    # ==================================================

    def set_selection(
        self,
        start_page,
        start_word,
        end_page,
        end_word,
        words,
        page_rects,
        zoom_factor
    ):

        self.clear()

        self.start_page = start_page
        self.start_word = start_word

        self.end_page = end_page
        self.end_word = end_word

        self.selected_words = list(
            words
        )

        self._draw(
            page_rects,
            zoom_factor
        )

    # ==================================================
    # DRAW
    # ==================================================

    def _draw(
        self,
        page_rects,
        zoom_factor
    ):

        if not self.selected_words:
            return

        for word in self.selected_words:

            page_number = (
                word.page_number
            )

            if not (
                0 <= page_number
                < len(page_rects)
            ):
                continue

            page_x, page_y, _, _ = (
                page_rects[
                    page_number
                ]
            )

            x = (
                page_x
                + word.x0
                * zoom_factor
            )

            y = (
                page_y
                + word.y0
                * zoom_factor
            )

            width = (
                word.width
                * zoom_factor
            )

            height = (
                word.height
                * zoom_factor
            )

            item = QGraphicsRectItem(
                QRectF(
                    x,
                    y,
                    width,
                    height
                )
            )

            item.setBrush(
                QColor(
                    70,
                    130,
                    255,
                    100
                )
            )

            item.setPen(
                QPen(
                    QColor(
                        70,
                        130,
                        255,
                        160
                    ),
                    1
                )
            )

            item.setZValue(
                20
            )

            self.scene.addItem(
                item
            )

            self.items.append(
                item
            )

    # ==================================================
    # HAS SELECTION
    # ==================================================

    @property
    def has_selection(self):

        return bool(
            self.selected_words
        )

    # ==================================================
    # SELECTED TEXT
    # ==================================================

    def selected_text(
        self,
        text_layout
    ):

        return text_layout.words_to_text(
            self.selected_words
        )