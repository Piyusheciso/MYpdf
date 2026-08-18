from PySide6.QtCore import QRectF
from PySide6.QtGui import QColor, QPen
from PySide6.QtWidgets import QGraphicsRectItem

from .annotation import Annotation


class AnnotationManager:

    def __init__(
        self,
        scene
    ):

        self.scene = scene

        # ==================================================
        # DATA
        # ==================================================

        self.annotations = []

        # ==================================================
        # GRAPHICS ITEMS
        #
        # One annotation can contain multiple rectangles.
        # ==================================================

        self.annotation_items = {}

        # ==================================================
        # ID
        # ==================================================

        self.next_id = 1

    # ==================================================
    # CLEAR
    # ==================================================

    def clear(
        self
    ):

        for items in self.annotation_items.values():

            for item in items:

                try:

                    self.scene.removeItem(
                        item
                    )

                except RuntimeError:

                    pass

        self.annotation_items.clear()

        self.annotations.clear()

        self.next_id = 1

    # ==================================================
    # ADD ANNOTATION
    # ==================================================

    def add_annotation(
        self,
        annotation
    ):

        if annotation is None:
            return None

        annotation.annotation_id = (
            self.next_id
        )

        self.next_id += 1

        self.annotations.append(
            annotation
        )

        self._draw_annotation(
            annotation
        )

        return annotation

    # ==================================================
    # CREATE HIGHLIGHT
    # ==================================================

    def create_highlight(
        self,
        words,
        text=""
    ):

        if not words:
            return None

        annotation = Annotation(
            annotation_type="highlight",
            page_number=words[0].page_number,
            text=text
        )

        # --------------------------------------------------
        # Create a rectangle for every selected word.
        #
        # This is deliberately simple and reliable.
        # Later we can merge adjacent rectangles.
        # --------------------------------------------------

        for word in words:

            annotation.add_rect(
                word.x0,
                word.y0,
                word.x1,
                word.y1
            )

        return self.add_annotation(
            annotation
        )

    # ==================================================
    # DRAW ANNOTATION
    # ==================================================

    def _draw_annotation(
        self,
        annotation
    ):

        if not annotation.has_rects:
            return

        items = []

        for rect in annotation.rects:

            x0, y0, x1, y1 = rect

            width = (
                x1 - x0
            )

            height = (
                y1 - y0
            )

            item = QGraphicsRectItem(
                QRectF(
                    x0,
                    y0,
                    width,
                    height
                )
            )

            color = QColor(
                *annotation.color
            )

            item.setBrush(
                color
            )

            item.setPen(
                QPen(
                    QColor(
                        color.red(),
                        color.green(),
                        color.blue(),
                        min(
                            color.alpha(),
                            180
                        )
                    ),
                    0.5
                )
            )

            # --------------------------------------------------
            # Annotation should appear above PDF page.
            # --------------------------------------------------

            item.setZValue(
                10
            )

            self.scene.addItem(
                item
            )

            items.append(
                item
            )

        self.annotation_items[
            annotation.annotation_id
        ] = items

    # ==================================================
    # REMOVE ANNOTATION
    # ==================================================

    def remove_annotation(
        self,
        annotation_id
    ):

        items = self.annotation_items.pop(
            annotation_id,
            []
        )

        for item in items:

            try:

                self.scene.removeItem(
                    item
                )

            except RuntimeError:

                pass

        self.annotations = [
            annotation
            for annotation in self.annotations
            if annotation.annotation_id
            != annotation_id
        ]

    # ==================================================
    # GET ANNOTATION
    # ==================================================

    def get_annotation(
        self,
        annotation_id
    ):

        for annotation in self.annotations:

            if (
                annotation.annotation_id
                == annotation_id
            ):

                return annotation

        return None

    # ==================================================
    # PAGE ANNOTATIONS
    # ==================================================

    def get_page_annotations(
        self,
        page_number
    ):

        return [
            annotation
            for annotation in self.annotations
            if annotation.page_number
            == page_number
        ]

    # ==================================================
    # REDRAW
    # ==================================================

    def redraw(
        self,
        page_rects,
        zoom_factor,
        rotation=0
    ):

        # --------------------------------------------------
        # Remove existing graphics items.
        # --------------------------------------------------

        for items in self.annotation_items.values():

            for item in items:

                try:

                    self.scene.removeItem(
                        item
                    )

                except RuntimeError:

                    pass

        self.annotation_items.clear()

        # --------------------------------------------------
        # Redraw every annotation.
        # --------------------------------------------------

        for annotation in self.annotations:

            self._draw_scaled_annotation(
                annotation,
                page_rects,
                zoom_factor,
                rotation
            )

    # ==================================================
    # DRAW SCALED ANNOTATION
    # ==================================================

    def _draw_scaled_annotation(
        self,
        annotation,
        page_rects,
        zoom_factor,
        rotation=0
    ):

        page_number = (
            annotation.page_number
        )

        if not (
            0 <= page_number
            < len(page_rects)
        ):

            return

        page_x, page_y, _, _ = (
            page_rects[
                page_number
            ]
        )

        items = []

        for rect in annotation.rects:

            x0, y0, x1, y1 = rect

            # --------------------------------------------------
            # PDF coordinate -> scene coordinate
            # --------------------------------------------------

            scene_x = (
                page_x
                + x0
                * zoom_factor
            )

            scene_y = (
                page_y
                + y0
                * zoom_factor
            )

            width = (
                x1 - x0
            ) * zoom_factor

            height = (
                y1 - y0
            ) * zoom_factor

            item = QGraphicsRectItem(
                QRectF(
                    scene_x,
                    scene_y,
                    width,
                    height
                )
            )

            color = QColor(
                *annotation.color
            )

            item.setBrush(
                color
            )

            item.setPen(
                QPen(
                    QColor(
                        color.red(),
                        color.green(),
                        color.blue(),
                        min(
                            color.alpha(),
                            180
                        )
                    ),
                    0.5
                )
            )

            item.setZValue(
                10
            )

            self.scene.addItem(
                item
            )

            items.append(
                item
            )

        self.annotation_items[
            annotation.annotation_id
        ] = items

    # ==================================================
    # GET ALL
    # ==================================================

    def all_annotations(
        self
    ):

        return list(
            self.annotations
        )

    # ==================================================
    # EXPORT
    # ==================================================

    def to_dict(
        self
    ):

        return [
            annotation.to_dict()
            for annotation
            in self.annotations
        ]

    # ==================================================
    # IMPORT
    # ==================================================

    def from_dict(
        self,
        data
    ):

        self.clear()

        if not isinstance(
            data,
            list
        ):

            return

        for annotation_data in data:

            try:

                annotation = (
                    Annotation.from_dict(
                        annotation_data
                    )
                )

                self.add_annotation(
                    annotation
                )

            except Exception:

                continue