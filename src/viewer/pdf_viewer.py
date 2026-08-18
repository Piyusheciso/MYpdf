from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QGraphicsPixmapItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
)

import pymupdf

from src.viewer.render_cache import RenderCache
from src.viewer.search_highlighter import SearchHighlighter
from src.viewer.text_selection import TextSelection
from src.pdf.text_layout import PDFTextLayout

from src.annotations.annotation_manager import (
    AnnotationManager,
)


class PDFViewer(QGraphicsView):

    page_changed = Signal(int)

    selection_changed = Signal()

    annotation_added = Signal(object)

    # ==================================================
    # INIT
    # ==================================================

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )

        # ==================================================
        # SCENE
        # ==================================================

        self.scene = QGraphicsScene(
            self
        )

        self.setScene(
            self.scene
        )

        # ==================================================
        # DOCUMENT
        # ==================================================

        self.pdf_document = None

        # ==================================================
        # TEXT
        # ==================================================

        self.text_layout = (
            PDFTextLayout()
        )

        self.text_selection = (
            TextSelection(
                self.scene
            )
        )

        # ==================================================
        # ANNOTATIONS
        # ==================================================

        self.annotation_manager = (
            AnnotationManager(
                self.scene
            )
        )

        # ==================================================
        # PAGE
        # ==================================================

        self.current_page = 0

        # ==================================================
        # ZOOM
        # ==================================================

        self.zoom_factor = 1.0

        # ==================================================
        # ROTATION
        # ==================================================

        self.rotation = 0

        # ==================================================
        # PAGE SPACING
        # ==================================================

        self.page_spacing = 20

        # ==================================================
        # RENDER
        # ==================================================

        self.render_radius = 2

        self.page_items = []

        self.page_rects = []

        self.placeholder_items = []

        # ==================================================
        # CACHE
        # ==================================================

        self.render_cache = RenderCache(
            max_items=12
        )

        # ==================================================
        # SEARCH
        # ==================================================

        self.search_highlighter = (
            SearchHighlighter(
                self.scene
            )
        )

        # ==================================================
        # SELECTION STATE
        # ==================================================

        self.selecting = False

        self.selection_start_page = None

        self.selection_start_word = None

        # ==================================================
        # INTERNAL
        # ==================================================

        self._updating_page = False

        self._rebuilding = False

        # ==================================================
        # VIEW
        # ==================================================

        self.setBackgroundBrush(
            Qt.GlobalColor.black
        )

        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.setDragMode(
            QGraphicsView.DragMode.ScrollHandDrag
        )

        self.setFocusPolicy(
            Qt.FocusPolicy.StrongFocus
        )

        self.verticalScrollBar().valueChanged.connect(
            self._scroll_changed
        )

    # ==================================================
    # DOCUMENT
    # ==================================================

    def set_document(
        self,
        document
    ):

        self.pdf_document = document

        self.text_layout.set_document(
            document
        )

        self.current_page = 0

        self.zoom_factor = 1.0

        self.rotation = 0

        self.render_cache.clear()

        self.search_highlighter.clear()

        self.text_selection.clear()

        self.annotation_manager.clear()

        self.clear()

        if (
            document
            and document.is_open
        ):

            self._build_page_layout()

            self.go_to_page(
                0,
                emit_signal=False
            )

            self.page_changed.emit(
                0
            )

            self.setFocus()

    # ==================================================
    # CLEAR
    # ==================================================

    def clear(
        self
    ):

        self.scene.clear()

        self.page_items.clear()

        self.page_rects.clear()

        self.placeholder_items.clear()

        self.search_highlighter.clear()

        self.text_selection = (
            TextSelection(
                self.scene
            )
        )

        self.annotation_manager = (
            AnnotationManager(
                self.scene
            )
        )

        self.current_page = 0

        self.render_cache.clear()

    # ==================================================
    # BUILD PAGE LAYOUT
    # ==================================================

    def _build_page_layout(
        self
    ):

        if (
            not self.pdf_document
            or not self.pdf_document.is_open
        ):

            return

        # --------------------------------------------------
        # Preserve annotations.
        #
        # The scene is rebuilt during zoom/rotation.
        # AnnotationManager stores the actual annotation
        # data independently from the graphics items.
        # --------------------------------------------------

        self.scene.clear()

        self.search_highlighter = (
            SearchHighlighter(
                self.scene
            )
        )

        self.text_selection = (
            TextSelection(
                self.scene
            )
        )

        self.page_items = [
            None
            for _ in range(
                self.pdf_document.page_count
            )
        ]

        self.page_rects = []

        self.placeholder_items = []

        y = 0

        viewport_width = (
            self.viewport().width()
        )

        for page_number in range(
            self.pdf_document.page_count
        ):

            page = (
                self.pdf_document.get_page(
                    page_number
                )
            )

            rect = page.rect

            width = (
                rect.width
                * self.zoom_factor
            )

            height = (
                rect.height
                * self.zoom_factor
            )

            if self.rotation in (
                90,
                270
            ):

                width, height = (
                    height,
                    width
                )

            x = max(
                0,
                (
                    viewport_width
                    - width
                ) / 2
            )

            self.page_rects.append(
                (
                    x,
                    y,
                    width,
                    height
                )
            )

            placeholder = (
                QGraphicsRectItem(
                    x,
                    y,
                    width,
                    height
                )
            )

            placeholder.setBrush(
                Qt.GlobalColor.white
            )

            placeholder.setPen(
                Qt.NoPen
            )

            placeholder.setZValue(
                -10
            )

            self.scene.addItem(
                placeholder
            )

            self.placeholder_items.append(
                placeholder
            )

            y += (
                height
                + self.page_spacing
            )

        self.scene.setSceneRect(
            0,
            0,
            max(
                viewport_width,
                self._document_width()
            ),
            y + 20
        )

        self._render_nearby_pages(
            self.current_page
        )

        # --------------------------------------------------
        # Redraw saved annotations.
        # --------------------------------------------------

        self.annotation_manager.redraw(
            self.page_rects,
            self.zoom_factor,
            self.rotation
        )

    # ==================================================
    # DOCUMENT WIDTH
    # ==================================================

    def _document_width(
        self
    ):

        if not self.page_rects:
            return 0

        return max(
            rect[0] + rect[2]
            for rect in self.page_rects
        )

    # ==================================================
    # RENDER PAGE
    # ==================================================

    def _render_page(
        self,
        page_number
    ):

        if (
            not self.pdf_document
            or not self.pdf_document.is_open
        ):

            return None

        cache_key = (
            page_number,
            round(
                self.zoom_factor,
                4
            ),
            self.rotation
        )

        cached = self.render_cache.get(
            cache_key
        )

        if cached is not None:
            return cached

        page = (
            self.pdf_document.get_page(
                page_number
            )
        )

        matrix = pymupdf.Matrix(
            self.zoom_factor,
            self.zoom_factor
        )

        if self.rotation:

            matrix = matrix.prerotate(
                self.rotation
            )

        pixmap = page.get_pixmap(
            matrix=matrix,
            alpha=False
        )

        image = QImage(
            pixmap.samples,
            pixmap.width,
            pixmap.height,
            pixmap.stride,
            QImage.Format.Format_RGB888
        ).copy()

        qt_pixmap = QPixmap.fromImage(
            image
        )

        self.render_cache.put(
            cache_key,
            qt_pixmap
        )

        return qt_pixmap

    # ==================================================
    # RENDER NEARBY
    # ==================================================

    def _render_nearby_pages(
        self,
        center_page
    ):

        start = max(
            0,
            center_page
            - self.render_radius
        )

        end = min(
            len(self.page_rects),
            center_page
            + self.render_radius
            + 1
        )

        for page_number in range(
            start,
            end
        ):

            self._ensure_page_rendered(
                page_number
            )

    # ==================================================
    # ENSURE RENDERED
    # ==================================================

    def _ensure_page_rendered(
        self,
        page_number
    ):

        if not (
            0 <= page_number
            < len(self.page_rects)
        ):

            return

        if self.page_items[
            page_number
        ] is not None:

            return

        pixmap = self._render_page(
            page_number
        )

        if pixmap is None:
            return

        x, y, width, height = (
            self.page_rects[
                page_number
            ]
        )

        item = QGraphicsPixmapItem(
            pixmap
        )

        item.setPos(
            x,
            y
        )

        item.setZValue(
            0
        )

        self.scene.addItem(
            item
        )

        self.page_items[
            page_number
        ] = item

        placeholder = (
            self.placeholder_items[
                page_number
            ]
        )

        if placeholder:

            self.scene.removeItem(
                placeholder
            )

            self.placeholder_items[
                page_number
            ] = None

    # ==================================================
    # REMOVE DISTANT PAGES
    # ==================================================

    def _remove_distant_pages(
        self,
        center_page
    ):

        minimum = max(
            0,
            center_page
            - self.render_radius
            - 1
        )

        maximum = min(
            len(self.page_items),
            center_page
            + self.render_radius
            + 2
        )

        for page_number, item in enumerate(
            self.page_items
        ):

            if item is None:
                continue

            if (
                minimum
                <= page_number
                <= maximum
            ):

                continue

            self.scene.removeItem(
                item
            )

            self.page_items[
                page_number
            ] = None

    # ==================================================
    # PAGE
    # ==================================================

    def go_to_page(
        self,
        page_number,
        emit_signal=True
    ):

        if not self.pdf_document:
            return

        if not self.pdf_document.is_open:
            return

        if not (
            0 <= page_number
            < self.pdf_document.page_count
        ):

            return

        self.current_page = (
            page_number
        )

        self._render_nearby_pages(
            page_number
        )

        self._remove_distant_pages(
            page_number
        )

        x, y, width, height = (
            self.page_rects[
                page_number
            ]
        )

        self._updating_page = True

        self.centerOn(
            x + width / 2,
            y + height / 2
        )

        self._updating_page = False

        if emit_signal:

            self.page_changed.emit(
                page_number
            )

        self.setFocus()

    # ==================================================
    # PAGE NAVIGATION
    # ==================================================

    def next_page(
        self
    ):

        if (
            self.pdf_document
            and self.current_page
            < self.pdf_document.page_count - 1
        ):

            self.go_to_page(
                self.current_page + 1
            )

    # ==================================================

    def previous_page(
        self
    ):

        if self.current_page > 0:

            self.go_to_page(
                self.current_page - 1
            )

    # ==================================================

    def first_page(
        self
    ):

        if self.pdf_document:

            self.go_to_page(
                0
            )

    # ==================================================

    def last_page(
        self
    ):

        if self.pdf_document:

            self.go_to_page(
                self.pdf_document.page_count - 1
            )

    # ==================================================
    # SCROLL
    # ==================================================

    def _scroll_changed(
        self,
        value
    ):

        if self._updating_page:
            return

        if not self.page_rects:
            return

        viewport_center = (
            self.mapToScene(
                self.viewport()
                .rect()
                .center()
            )
        )

        best_page = self.current_page

        best_distance = float(
            "inf"
        )

        for index, rect_data in enumerate(
            self.page_rects
        ):

            x, y, width, height = (
                rect_data
            )

            center_y = (
                y + height / 2
            )

            distance = abs(
                center_y
                - viewport_center.y()
            )

            if distance < best_distance:

                best_distance = distance

                best_page = index

        if (
            best_page
            != self.current_page
        ):

            self.current_page = (
                best_page
            )

            self._render_nearby_pages(
                best_page
            )

            self.page_changed.emit(
                best_page
            )

    # ==================================================
    # MOUSE PRESS
    # ==================================================

    def mousePressEvent(
        self,
        event
    ):

        if (
            event.button()
            == Qt.MouseButton.LeftButton
        ):

            scene_pos = self.mapToScene(
                event.position().toPoint()
            )

            page_number = (
                self._page_at_scene_position(
                    scene_pos
                )
            )

            if page_number is not None:

                pdf_point = (
                    self._scene_to_pdf(
                        scene_pos,
                        page_number
                    )
                )

                if pdf_point:

                    word = (
                        self.text_layout.word_at(
                            page_number,
                            pdf_point[0],
                            pdf_point[1]
                        )
                    )

                    if word:

                        self.selecting = True

                        self.selection_start_page = (
                            page_number
                        )

                        self.selection_start_word = (
                            word
                        )

                        self.text_selection.clear()

                        self.viewport().setCursor(
                            Qt.CursorShape.IBeamCursor
                        )

                        event.accept()

                        return

        super().mousePressEvent(
            event
        )

    # ==================================================
    # MOUSE MOVE
    # ==================================================

    def mouseMoveEvent(
        self,
        event
    ):

        if (
            self.selecting
            and self.selection_start_word
        ):

            scene_pos = self.mapToScene(
                event.position().toPoint()
            )

            page_number = (
                self._page_at_scene_position(
                    scene_pos
                )
            )

            if page_number is not None:

                pdf_point = (
                    self._scene_to_pdf(
                        scene_pos,
                        page_number
                    )
                )

                if pdf_point:

                    word = (
                        self.text_layout.word_at(
                            page_number,
                            pdf_point[0],
                            pdf_point[1]
                        )
                    )

                    if word:

                        words = (
                            self.text_layout.select_between(
                                self.selection_start_page,
                                self.selection_start_word,
                                page_number,
                                word
                            )
                        )

                        self.text_selection.set_selection(
                            self.selection_start_page,
                            self.selection_start_word,
                            page_number,
                            word,
                            words,
                            self.page_rects,
                            self.zoom_factor
                        )

                        self.selection_changed.emit()

                        event.accept()

                        return

        super().mouseMoveEvent(
            event
        )

    # ==================================================
    # MOUSE RELEASE
    # ==================================================

    def mouseReleaseEvent(
        self,
        event
    ):

        if (
            event.button()
            == Qt.MouseButton.LeftButton
            and self.selecting
        ):

            self.selecting = False

            self.viewport().setCursor(
                Qt.CursorShape.ArrowCursor
            )

            event.accept()

            return

        super().mouseReleaseEvent(
            event
        )

    # ==================================================
    # PAGE AT POSITION
    # ==================================================

    def _page_at_scene_position(
        self,
        scene_pos
    ):

        for index, rect_data in enumerate(
            self.page_rects
        ):

            x, y, width, height = (
                rect_data
            )

            if (
                x <= scene_pos.x()
                <= x + width
                and
                y <= scene_pos.y()
                <= y + height
            ):

                return index

        return None

    # ==================================================
    # SCENE -> PDF
    # ==================================================

    def _scene_to_pdf(
        self,
        scene_pos,
        page_number
    ):

        if not (
            0 <= page_number
            < len(self.page_rects)
        ):

            return None

        page_x, page_y, _, _ = (
            self.page_rects[
                page_number
            ]
        )

        x = (
            scene_pos.x()
            - page_x
        ) / self.zoom_factor

        y = (
            scene_pos.y()
            - page_y
        ) / self.zoom_factor

        return (
            x,
            y
        )

    # ==================================================
    # COPY
    # ==================================================

    def copy_selected_text(
        self
    ):

        if not self.text_selection.has_selection:
            return

        text = (
            self.text_selection.selected_text(
                self.text_layout
            )
        )

        if not text:
            return

        clipboard = (
            QApplication.clipboard()
        )

        clipboard.setText(
            text
        )

    # ==================================================
    # SELECT ALL
    # ==================================================

    def select_all_text(
        self
    ):

        if not self.pdf_document:
            return

        if not self.pdf_document.is_open:
            return

        words = (
            self.text_layout.get_all_words()
        )

        if not words:
            return

        first = words[0]

        last = words[-1]

        selected = (
            self.text_layout.select_between(
                first.page_number,
                first,
                last.page_number,
                last
            )
        )

        self.text_selection.set_selection(
            first.page_number,
            first,
            last.page_number,
            last,
            selected,
            self.page_rects,
            self.zoom_factor
        )

        self.selection_changed.emit()

    # ==================================================
    # CLEAR SELECTION
    # ==================================================

    def clear_text_selection(
        self
    ):

        self.text_selection.clear()

        self.selection_changed.emit()

    # ==================================================
    # HIGHLIGHT CURRENT SELECTION
    # ==================================================

    def highlight_selection(
        self
    ):

        if not self.text_selection.has_selection:

            return None

        words = (
            self.text_selection.selected_words
        )

        if not words:

            return None

        text = (
            self.text_layout.words_to_text(
                words
            )
        )

        annotation = (
            self.annotation_manager.create_highlight(
                words,
                text
            )
        )

        if annotation is None:

            return None

        # --------------------------------------------------
        # Clear temporary text selection.
        #
        # The permanent annotation remains.
        # --------------------------------------------------

        self.clear_text_selection()

        self.annotation_added.emit(
            annotation
        )

        return annotation

    # ==================================================
    # REMOVE ANNOTATION
    # ==================================================

    def remove_annotation(
        self,
        annotation_id
    ):

        self.annotation_manager.remove_annotation(
            annotation_id
        )

    # ==================================================
    # CLEAR ALL ANNOTATIONS
    # ==================================================

    def clear_annotations(
        self
    ):

        self.annotation_manager.clear()

    # ==================================================
    # GET ANNOTATIONS
    # ==================================================

    def get_annotations(
        self
    ):

        return (
            self.annotation_manager.all_annotations()
        )

    # ==================================================
    # KEYBOARD
    # ==================================================

    def keyPressEvent(
        self,
        event
    ):

        key = event.key()

        modifiers = event.modifiers()

        if key == Qt.Key.Key_Escape:

            self.clear_text_selection()

            event.accept()

            return

        # --------------------------------------------------
        # Ctrl shortcuts
        # --------------------------------------------------

        if (
            modifiers
            & Qt.KeyboardModifier.ControlModifier
        ):

            if key == Qt.Key.Key_C:

                self.copy_selected_text()

                event.accept()

                return

            if key == Qt.Key.Key_A:

                self.select_all_text()

                event.accept()

                return

            if key in (
                Qt.Key.Key_Plus,
                Qt.Key.Key_Equal
            ):

                self.zoom_in()

                event.accept()

                return

            if key == Qt.Key.Key_Minus:

                self.zoom_out()

                event.accept()

                return

            # --------------------------------------------------
            # Ctrl + Shift + H
            #
            # Quick highlight shortcut.
            # --------------------------------------------------

            if (
                key == Qt.Key.Key_H
                and
                modifiers
                & Qt.KeyboardModifier.ShiftModifier
            ):

                self.highlight_selection()

                event.accept()

                return

        # --------------------------------------------------
        # Page navigation
        # --------------------------------------------------

        if key == Qt.Key.Key_Left:

            self.previous_page()

            event.accept()

            return

        if key == Qt.Key.Key_Right:

            self.next_page()

            event.accept()

            return

        if key == Qt.Key.Key_PageUp:

            self.previous_page()

            event.accept()

            return

        if key == Qt.Key.Key_PageDown:

            self.next_page()

            event.accept()

            return

        if key == Qt.Key.Key_Home:

            self.first_page()

            event.accept()

            return

        if key == Qt.Key.Key_End:

            self.last_page()

            event.accept()

            return

        super().keyPressEvent(
            event
        )

    # ==================================================
    # WHEEL
    # ==================================================

    def wheelEvent(
        self,
        event
    ):

        modifiers = event.modifiers()

        if (
            modifiers
            & Qt.KeyboardModifier.ControlModifier
        ):

            if event.angleDelta().y() > 0:

                self.zoom_in()

            else:

                self.zoom_out()

            event.accept()

            return

        super().wheelEvent(
            event
        )

    # ==================================================
    # ZOOM IN
    # ==================================================

    def zoom_in(
        self
    ):

        self.zoom_factor *= 1.2

        self.zoom_factor = min(
            self.zoom_factor,
            5.0
        )

        self._rebuild()

    # ==================================================
    # ZOOM OUT
    # ==================================================

    def zoom_out(
        self
    ):

        self.zoom_factor /= 1.2

        self.zoom_factor = max(
            self.zoom_factor,
            0.25
        )

        self._rebuild()

    # ==================================================
    # ACTUAL SIZE
    # ==================================================

    def actual_size(
        self
    ):

        self.zoom_factor = 1.0

        self._rebuild()

    # ==================================================
    # FIT PAGE
    # ==================================================

    def fit_page(
        self
    ):

        if not self.pdf_document:
            return

        if not self.pdf_document.is_open:
            return

        page = (
            self.pdf_document.get_page(
                self.current_page
            )
        )

        width = page.rect.width

        height = page.rect.height

        if self.rotation in (
            90,
            270
        ):

            width, height = (
                height,
                width
            )

        viewport_width = (
            self.viewport().width()
            - 30
        )

        viewport_height = (
            self.viewport().height()
            - 30
        )

        if (
            width <= 0
            or height <= 0
        ):

            return

        self.zoom_factor = min(
            viewport_width / width,
            viewport_height / height
        )

        self._rebuild()

    # ==================================================
    # FIT WIDTH
    # ==================================================

    def fit_width(
        self
    ):

        if not self.pdf_document:
            return

        if not self.pdf_document.is_open:
            return

        page = (
            self.pdf_document.get_page(
                self.current_page
            )
        )

        width = page.rect.width

        if self.rotation in (
            90,
            270
        ):

            width = page.rect.height

        if width <= 0:
            return

        self.zoom_factor = (
            (
                self.viewport().width()
                - 30
            )
            / width
        )

        self._rebuild()

    # ==================================================
    # ROTATE
    # ==================================================

    def rotate_clockwise(
        self
    ):

        self.rotation = (
            self.rotation + 90
        ) % 360

        current = (
            self.current_page
        )

        self.render_cache.clear()

        self._build_page_layout()

        if self.page_rects:

            self.go_to_page(
                current
            )

    # ==================================================
    # REBUILD
    # ==================================================

    def _rebuild(
        self
    ):

        if self._rebuilding:
            return

        self._rebuilding = True

        current = (
            self.current_page
        )

        self.render_cache.clear()

        # --------------------------------------------------
        # Temporary selection should disappear during
        # rebuild, but saved annotations remain.
        # --------------------------------------------------

        self.text_selection.clear()

        self._build_page_layout()

        if self.page_rects:

            self.go_to_page(
                min(
                    current,
                    len(
                        self.page_rects
                    ) - 1
                )
            )

        self._rebuilding = False

    # ==================================================
    # SEARCH RESULTS
    # ==================================================

    def set_search_results(
        self,
        results
    ):

        self.search_highlighter.highlight(
            results,
            self.page_rects,
            self.zoom_factor,
            self.rotation
        )

    # ==================================================

    def clear_search_results(
        self
    ):

        self.search_highlighter.clear()

    # ==================================================

    def show_search_result(
        self,
        result
    ):

        if result is None:
            return

        page_number = (
            result.page_number
        )

        self.go_to_page(
            page_number
        )

        page_x, page_y, _, _ = (
            self.page_rects[
                page_number
            ]
        )

        x = (
            page_x
            + result.rect.x0
            * self.zoom_factor
        )

        y = (
            page_y
            + result.rect.y0
            * self.zoom_factor
        )

        self.centerOn(
            x,
            y
        )

    # ==================================================
    # RESIZE
    # ==================================================

    def resizeEvent(
        self,
        event
    ):

        super().resizeEvent(
            event
        )

        # --------------------------------------------------
        # Do not rebuild automatically while a document
        # is closed.
        # --------------------------------------------------

        if not self.pdf_document:
            return

        if not self.pdf_document.is_open:
            return

        # --------------------------------------------------
        # Keep page positioning correct after the window
        # or sidebar changes size.
        # --------------------------------------------------

        current = (
            self.current_page
        )

        self._build_page_layout()

        if self.page_rects:

            self.go_to_page(
                min(
                    current,
                    len(
                        self.page_rects
                    ) - 1
                ),
                emit_signal=False
            )