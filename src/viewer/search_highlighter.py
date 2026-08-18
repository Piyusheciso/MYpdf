from PySide6.QtCore import QRectF
from PySide6.QtGui import QColor, QPen
from PySide6.QtWidgets import QGraphicsRectItem


class SearchHighlighter:

    def __init__(self, scene):

        self.scene = scene

        self.items = []

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

    # ==================================================
    # HIGHLIGHT
    # ==================================================

    def highlight(
        self,
        results,
        page_rects,
        zoom_factor,
        rotation=0
    ):

        self.clear()

        if not results:
            return

        for result in results:

            page_number = (
                result.page_number
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

            rect = result.rect

            x = (
                page_x
                + rect.x0 * zoom_factor
            )

            y = (
                page_y
                + rect.y0 * zoom_factor
            )

            width = (
                (rect.x1 - rect.x0)
                * zoom_factor
            )

            height = (
                (rect.y1 - rect.y0)
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

            # Transparent fill.
            item.setBrush(
                QColor(
                    255,
                    235,
                    59,
                    100
                )
            )

            item.setPen(
                QPen(
                    QColor(
                        255,
                        193,
                        7,
                        180
                    ),
                    1
                )
            )

            item.setZValue(
                10
            )

            self.scene.addItem(
                item
            )

            self.items.append(
                item
            )