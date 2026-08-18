from pathlib import Path

import pymupdf

from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QAction,
    QImage,
    QPainter,
)
from PySide6.QtPrintSupport import (
    QPrinter,
    QPrintDialog,
    QPrintPreviewDialog,
)
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QDockWidget,
    QLineEdit,
    QToolBar,
    QWidget,
    QHBoxLayout,
    QDialog,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QInputDialog,
    QDialogButtonBox,
)

from src.pdf.document import PDFDocument
from src.pdf.text_search import PDFTextSearch

from src.viewer.pdf_viewer import PDFViewer

from src.navigation.history import NavigationHistory

from src.ui.sidebar.sidebar import Sidebar

from src.ui.right_panel.right_panel import RightPanel


class MainWindow(QMainWindow):

    def __init__(
        self
    ):

        super().__init__()

        # ==================================================
        # CORE
        # ==================================================

        self.pdf_document = PDFDocument()

        self.viewer = PDFViewer()

        self.history = NavigationHistory()

        self.text_search = PDFTextSearch()

        # ==================================================
        # SEARCH STATE
        # ==================================================

        self.search_results = []

        self.search_index = -1

        # ==================================================
        # WINDOW
        # ==================================================

        self.setWindowTitle(
            "MYpdf Reader"
        )

        self.resize(
            1300,
            850
        )

        # ==================================================
        # MAIN VIEW
        # ==================================================

        self.create_main_view()

        # ==================================================
        # SIDEBAR
        # ==================================================

        self.create_sidebar()

        # ==================================================
        # MENU
        # ==================================================

        self.create_menu()

        # ==================================================
        # TOOLBAR
        # ==================================================

        self.create_toolbar()

        # ==================================================
        # SEARCH
        # ==================================================

        self.create_search_bar()

        # ==================================================
        # STATUS BAR
        # ==================================================

        self.create_status_bar()

        # ==================================================
        # RIGHT PANEL
        # ==================================================

        self.connect_right_panel()

        # ==================================================
        # PAGE SIGNAL
        # ==================================================

        self.viewer.page_changed.connect(
            self.on_page_changed
        )

        # ==================================================
        # DRAG & DROP
        # ==================================================

        self.setAcceptDrops(
            True
        )

        # ==================================================
        # INITIAL STATE
        # ==================================================

        self.update_history_buttons()

        self.update_page_input()

    # ======================================================
    # MAIN VIEW
    # ======================================================

    def create_main_view(
        self
    ):

        self.main_container = QWidget()

        self.main_layout = QHBoxLayout(
            self.main_container
        )

        self.main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.main_layout.setSpacing(
            0
        )

        # --------------------------------------------------
        # PDF VIEWER
        # --------------------------------------------------

        self.main_layout.addWidget(
            self.viewer,
            1
        )

        # --------------------------------------------------
        # RIGHT PANEL
        # --------------------------------------------------

        self.right_panel = RightPanel()

        self.main_layout.addWidget(
            self.right_panel,
            0
        )

        # --------------------------------------------------
        # CENTRAL WIDGET
        # --------------------------------------------------

        self.setCentralWidget(
            self.main_container
        )

    # ======================================================
    # SIDEBAR
    # ======================================================

    def create_sidebar(
        self
    ):

        self.sidebar = Sidebar()

        self.sidebar_dock = QDockWidget(
            "Navigation",
            self
        )

        self.sidebar_dock.setWidget(
            self.sidebar
        )

        self.sidebar_dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea
        )

        self.addDockWidget(
            Qt.DockWidgetArea.LeftDockWidgetArea,
            self.sidebar_dock
        )

        self.sidebar.thumbnails.page_selected.connect(
            self.go_to_page
        )

        self.sidebar.outline.page_selected.connect(
            self.go_to_page
        )

    # ======================================================
    # SEARCH BAR
    # ======================================================

    def create_search_bar(
        self
    ):

        self.search_toolbar = QToolBar(
            "Search",
            self
        )

        self.search_toolbar.setMovable(
            False
        )

        self.search_toolbar.setVisible(
            False
        )

        self.addToolBar(
            Qt.ToolBarArea.TopToolBarArea,
            self.search_toolbar
        )

        # --------------------------------------------------
        # SEARCH INPUT
        # --------------------------------------------------

        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "Search in PDF..."
        )

        self.search_input.setFixedWidth(
            300
        )

        self.search_input.textChanged.connect(
            self.perform_search
        )

        self.search_input.returnPressed.connect(
            self.next_search_result
        )

        self.search_toolbar.addWidget(
            self.search_input
        )

        # --------------------------------------------------
        # PREVIOUS
        # --------------------------------------------------

        previous_search = QAction(
            "↑",
            self
        )

        previous_search.setToolTip(
            "Previous Result"
        )

        previous_search.triggered.connect(
            self.previous_search_result
        )

        self.search_toolbar.addAction(
            previous_search
        )

        # --------------------------------------------------
        # NEXT
        # --------------------------------------------------

        next_search = QAction(
            "↓",
            self
        )

        next_search.setToolTip(
            "Next Result"
        )

        next_search.triggered.connect(
            self.next_search_result
        )

        self.search_toolbar.addAction(
            next_search
        )

        # --------------------------------------------------
        # RESULT LABEL
        # --------------------------------------------------

        self.search_result_label = QLabel(
            ""
        )

        self.search_toolbar.addWidget(
            self.search_result_label
        )

        # --------------------------------------------------
        # CLOSE
        # --------------------------------------------------

        close_search = QAction(
            "✕",
            self
        )

        close_search.setToolTip(
            "Close Search"
        )

        close_search.triggered.connect(
            self.close_search
        )

        self.search_toolbar.addAction(
            close_search
        )

    # ======================================================
    # MENU
    # ======================================================

    def create_menu(
        self
    ):

        # ==================================================
        # FILE
        # ==================================================

        file_menu = self.menuBar().addMenu(
            "File"
        )

        open_action = QAction(
            "Open PDF",
            self
        )

        open_action.setShortcut(
            "Ctrl+O"
        )

        open_action.triggered.connect(
            self.open_pdf
        )

        file_menu.addAction(
            open_action
        )

        save_as_action = QAction(
            "Save As",
            self
        )

        save_as_action.setShortcut(
            "Ctrl+Shift+S"
        )

        save_as_action.triggered.connect(
            self.save_as
        )

        file_menu.addAction(
            save_as_action
        )

        file_menu.addSeparator()

        close_action = QAction(
            "Close",
            self
        )

        close_action.setShortcut(
            "Ctrl+W"
        )

        close_action.triggered.connect(
            self.close_pdf
        )

        file_menu.addAction(
            close_action
        )

        file_menu.addSeparator()

        exit_action = QAction(
            "Exit",
            self
        )

        exit_action.setShortcut(
            "Ctrl+Q"
        )

        exit_action.triggered.connect(
            self.close
        )

        file_menu.addAction(
            exit_action
        )

        # ==================================================
        # EDIT
        # ==================================================

        edit_menu = self.menuBar().addMenu(
            "Edit"
        )

        copy_action = QAction(
            "Copy",
            self
        )

        copy_action.setShortcut(
            "Ctrl+C"
        )

        copy_action.triggered.connect(
            self.viewer.copy_selected_text
        )

        edit_menu.addAction(
            copy_action
        )

        select_all_action = QAction(
            "Select All",
            self
        )

        select_all_action.setShortcut(
            "Ctrl+A"
        )

        select_all_action.triggered.connect(
            self.viewer.select_all_text
        )

        edit_menu.addAction(
            select_all_action
        )

        clear_selection_action = QAction(
            "Clear Selection",
            self
        )

        clear_selection_action.setShortcut(
            "Esc"
        )

        clear_selection_action.triggered.connect(
            self.viewer.clear_text_selection
        )

        edit_menu.addAction(
            clear_selection_action
        )

        edit_menu.addSeparator()

        search_action = QAction(
            "Find",
            self
        )

        search_action.setShortcut(
            "Ctrl+F"
        )

        search_action.triggered.connect(
            self.open_search
        )

        edit_menu.addAction(
            search_action
        )

        # ==================================================
        # VIEW
        # ==================================================

        view_menu = self.menuBar().addMenu(
            "View"
        )

        sidebar_action = (
            self.sidebar_dock.toggleViewAction()
        )

        sidebar_action.setText(
            "Navigation Sidebar"
        )

        view_menu.addAction(
            sidebar_action
        )

        view_menu.addSeparator()

        # --------------------------------------------------
        # PAGE NAVIGATION
        # --------------------------------------------------

        first_action = QAction(
            "First Page",
            self
        )

        first_action.setShortcut(
            "Home"
        )

        first_action.triggered.connect(
            self.go_first_page
        )

        view_menu.addAction(
            first_action
        )

        previous_action = QAction(
            "Previous Page",
            self
        )

        previous_action.setShortcut(
            "Left"
        )

        previous_action.triggered.connect(
            self.previous_page
        )

        view_menu.addAction(
            previous_action
        )

        next_action = QAction(
            "Next Page",
            self
        )

        next_action.setShortcut(
            "Right"
        )

        next_action.triggered.connect(
            self.next_page
        )

        view_menu.addAction(
            next_action
        )

        last_action = QAction(
            "Last Page",
            self
        )

        last_action.setShortcut(
            "End"
        )

        last_action.triggered.connect(
            self.go_last_page
        )

        view_menu.addAction(
            last_action
        )

        view_menu.addSeparator()

        # --------------------------------------------------
        # FIT
        # --------------------------------------------------

        fit_page = QAction(
            "Fit Page",
            self
        )

        fit_page.triggered.connect(
            self.viewer.fit_page
        )

        view_menu.addAction(
            fit_page
        )

        fit_width = QAction(
            "Fit Width",
            self
        )

        fit_width.triggered.connect(
            self.viewer.fit_width
        )

        view_menu.addAction(
            fit_width
        )

        actual_size = QAction(
            "Actual Size",
            self
        )

        actual_size.setShortcut(
            "Ctrl+1"
        )

        actual_size.triggered.connect(
            self.viewer.actual_size
        )

        view_menu.addAction(
            actual_size
        )

        view_menu.addSeparator()

        # --------------------------------------------------
        # ZOOM
        # --------------------------------------------------

        zoom_in = QAction(
            "Zoom In",
            self
        )

        zoom_in.setShortcut(
            "Ctrl++"
        )

        zoom_in.triggered.connect(
            self.viewer.zoom_in
        )

        view_menu.addAction(
            zoom_in
        )

        zoom_out = QAction(
            "Zoom Out",
            self
        )

        zoom_out.setShortcut(
            "Ctrl+-"
        )

        zoom_out.triggered.connect(
            self.viewer.zoom_out
        )

        view_menu.addAction(
            zoom_out
        )

        view_menu.addSeparator()

        # --------------------------------------------------
        # ROTATE
        # --------------------------------------------------

        rotate = QAction(
            "Rotate Clockwise",
            self
        )

        rotate.triggered.connect(
            self.viewer.rotate_clockwise
        )

        view_menu.addAction(
            rotate
        )

        # ==================================================
        # DOCUMENT
        # ==================================================

        document_menu = self.menuBar().addMenu(
            "Document"
        )

        bookmark_action = QAction(
            "Bookmarks",
            self
        )

        bookmark_action.triggered.connect(
            self.show_bookmarks
        )

        document_menu.addAction(
            bookmark_action
        )

        annotation_action = QAction(
            "Annotations",
            self
        )

        annotation_action.triggered.connect(
            self.show_annotations
        )

        document_menu.addAction(
            annotation_action
        )

        document_menu.addSeparator()

        print_action = QAction(
            "Print",
            self
        )

        print_action.setShortcut(
            "Ctrl+P"
        )

        print_action.triggered.connect(
            self.print_pdf
        )

        document_menu.addAction(
            print_action
        )

        info_action = QAction(
            "Document Information",
            self
        )

        info_action.triggered.connect(
            self.show_document_info
        )

        document_menu.addAction(
            info_action
        )

    # ======================================================
    # RIGHT PANEL
    # ======================================================

    def connect_right_panel(
        self
    ):

        self.right_panel.search_button.clicked.connect(
            self.open_search
        )

        self.right_panel.bookmark_button.clicked.connect(
            self.show_bookmarks
        )

        self.right_panel.annotation_button.clicked.connect(
            self.show_annotations
        )

        self.right_panel.download_button.clicked.connect(
            self.save_as
        )

        self.right_panel.print_button.clicked.connect(
            self.print_pdf
        )

        self.right_panel.info_button.clicked.connect(
            self.show_document_info
        )

    # ======================================================
    # TOOLBAR
    # ======================================================

    def create_toolbar(
        self
    ):

        toolbar = QToolBar(
            "Navigation",
            self
        )

        toolbar.setMovable(
            False
        )

        self.addToolBar(
            toolbar
        )

        # --------------------------------------------------
        # BACK
        # --------------------------------------------------

        self.back_action = QAction(
            "←",
            self
        )

        self.back_action.setToolTip(
            "Back"
        )

        self.back_action.triggered.connect(
            self.go_back
        )

        toolbar.addAction(
            self.back_action
        )

        # --------------------------------------------------
        # FORWARD
        # --------------------------------------------------

        self.forward_action = QAction(
            "→",
            self
        )

        self.forward_action.setToolTip(
            "Forward"
        )

        self.forward_action.triggered.connect(
            self.go_forward
        )

        toolbar.addAction(
            self.forward_action
        )

        toolbar.addSeparator()

        # --------------------------------------------------
        # FIRST
        # --------------------------------------------------

        first = QAction(
            "First",
            self
        )

        first.triggered.connect(
            self.go_first_page
        )

        toolbar.addAction(
            first
        )

        # --------------------------------------------------
        # PREVIOUS
        # --------------------------------------------------

        previous = QAction(
            "Previous",
            self
        )

        previous.triggered.connect(
            self.previous_page
        )

        toolbar.addAction(
            previous
        )

        # --------------------------------------------------
        # PAGE INPUT
        # --------------------------------------------------

        self.page_input = QLineEdit()

        self.page_input.setFixedWidth(
            60
        )

        self.page_input.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.page_input.setPlaceholderText(
            "Page"
        )

        self.page_input.returnPressed.connect(
            self.page_input_changed
        )

        toolbar.addWidget(
            self.page_input
        )

        # --------------------------------------------------
        # PAGE COUNT
        # --------------------------------------------------

        self.page_count_label = QLabel(
            "/ 0"
        )

        toolbar.addWidget(
            self.page_count_label
        )

        # --------------------------------------------------
        # NEXT
        # --------------------------------------------------

        next_action = QAction(
            "Next",
            self
        )

        next_action.triggered.connect(
            self.next_page
        )

        toolbar.addAction(
            next_action
        )

        # --------------------------------------------------
        # LAST
        # --------------------------------------------------

        last = QAction(
            "Last",
            self
        )

        last.triggered.connect(
            self.go_last_page
        )

        toolbar.addAction(
            last
        )

        toolbar.addSeparator()

        # --------------------------------------------------
        # ZOOM IN
        # --------------------------------------------------

        zoom_in = QAction(
            "Zoom +",
            self
        )

        zoom_in.triggered.connect(
            self.viewer.zoom_in
        )

        toolbar.addAction(
            zoom_in
        )

        # --------------------------------------------------
        # ZOOM OUT
        # --------------------------------------------------

        zoom_out = QAction(
            "Zoom -",
            self
        )

        zoom_out.triggered.connect(
            self.viewer.zoom_out
        )

        toolbar.addAction(
            zoom_out
        )

        # --------------------------------------------------
        # ACTUAL SIZE
        # --------------------------------------------------

        actual = QAction(
            "100%",
            self
        )

        actual.triggered.connect(
            self.viewer.actual_size
        )

        toolbar.addAction(
            actual
        )

        # --------------------------------------------------
        # FIT PAGE
        # --------------------------------------------------

        fit_page = QAction(
            "Fit Page",
            self
        )

        fit_page.triggered.connect(
            self.viewer.fit_page
        )

        toolbar.addAction(
            fit_page
        )

        # --------------------------------------------------
        # FIT WIDTH
        # --------------------------------------------------

        fit_width = QAction(
            "Fit Width",
            self
        )

        fit_width.triggered.connect(
            self.viewer.fit_width
        )

        toolbar.addAction(
            fit_width
        )

        toolbar.addSeparator()

        # --------------------------------------------------
        # ROTATE
        # --------------------------------------------------

        rotate = QAction(
            "Rotate",
            self
        )

        rotate.triggered.connect(
            self.viewer.rotate_clockwise
        )

        toolbar.addAction(
            rotate
        )

    # ======================================================
    # STATUS BAR
    # ======================================================

    def create_status_bar(
        self
    ):

        self.status_label = QLabel(
            "No document open"
        )

        self.statusBar().addPermanentWidget(
            self.status_label
        )

    # ======================================================
    # OPEN PDF
    # ======================================================

    def open_pdf(
        self
    ):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open PDF",
            "",
            "PDF Files (*.pdf)"
        )

        if file_path:

            self.load_pdf(
                file_path
            )

    # ======================================================
    # LOAD PDF
    # ======================================================

    def load_pdf(
        self,
        file_path
    ):

        try:

            if self.pdf_document.is_open:

                self.pdf_document.close()

            self.pdf_document.open(
                file_path
            )

            self.viewer.set_document(
                self.pdf_document
            )

            self.sidebar.set_document(
                self.pdf_document
            )

            self.text_search.set_document(
                self.pdf_document
            )

            # ------------------------------------------------
            # SEARCH RESET
            # ------------------------------------------------

            self.search_results.clear()

            self.search_index = -1

            self.close_search(
                update_only=True
            )

            # ------------------------------------------------
            # HISTORY RESET
            # ------------------------------------------------

            self.history.clear()

            self.history.push(
                0
            )

            # ------------------------------------------------
            # UI
            # ------------------------------------------------

            self.update_document_ui()

        except PermissionError as exc:

            QMessageBox.warning(
                self,
                "Password Protected",
                str(exc)
            )

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Unable to Open PDF",
                str(exc)
            )

    # ======================================================
    # SAVE AS
    # ======================================================

    def save_as(
        self
    ):

        if not self.pdf_document.is_open:

            QMessageBox.information(
                self,
                "No PDF",
                "Open a PDF first."
            )

            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF As",
            "",
            "PDF Files (*.pdf)"
        )

        if not file_path:

            return

        try:

            if not file_path.lower().endswith(
                ".pdf"
            ):

                file_path += ".pdf"

            self.pdf_document.save_as(
                file_path
            )

            QMessageBox.information(
                self,
                "Saved",
                "PDF saved successfully."
            )

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Save Error",
                str(exc)
            )

    # ======================================================
    # SEARCH
    # ======================================================

    def open_search(
        self
    ):

        if not self.pdf_document.is_open:

            return

        self.search_toolbar.setVisible(
            True
        )

        self.search_input.setFocus()

        self.search_input.selectAll()

    # ======================================================

    def close_search(
        self,
        update_only=False
    ):

        self.search_results.clear()

        self.search_index = -1

        if hasattr(
            self,
            "viewer"
        ):

            self.viewer.clear_search_results()

        if hasattr(
            self,
            "search_result_label"
        ):

            self.search_result_label.setText(
                ""
            )

        if hasattr(
            self,
            "search_input"
        ):

            self.search_input.clear()

        if not update_only:

            self.search_toolbar.setVisible(
                False
            )

            self.viewer.setFocus()

    # ======================================================
    # PERFORM SEARCH
    # ======================================================

    def perform_search(
        self,
        text
    ):

        text = text.strip()

        if not text:

            self.search_results.clear()

            self.search_index = -1

            self.viewer.clear_search_results()

            self.search_result_label.setText(
                ""
            )

            return

        if not self.pdf_document.is_open:

            return

        self.search_results = (
            self.text_search.search(
                text
            )
        )

        self.search_index = -1

        self.viewer.set_search_results(
            self.search_results
        )

        count = len(
            self.search_results
        )

        if count == 0:

            self.search_result_label.setText(
                "No results"
            )

            return

        self.search_result_label.setText(
            f"{count} result"
            f"{'s' if count != 1 else ''}"
        )

        self.next_search_result()

    # ======================================================
    # NEXT SEARCH RESULT
    # ======================================================

    def next_search_result(
        self
    ):

        if not self.search_results:

            return

        self.search_index += 1

        if (
            self.search_index
            >= len(self.search_results)
        ):

            self.search_index = 0

        result = (
            self.search_results[
                self.search_index
            ]
        )

        self.viewer.show_search_result(
            result
        )

        self.search_result_label.setText(
            f"{self.search_index + 1}"
            f" / "
            f"{len(self.search_results)}"
        )

    # ======================================================
    # PREVIOUS SEARCH RESULT
    # ======================================================

    def previous_search_result(
        self
    ):

        if not self.search_results:

            return

        self.search_index -= 1

        if self.search_index < 0:

            self.search_index = (
                len(self.search_results)
                - 1
            )

        result = (
            self.search_results[
                self.search_index
            ]
        )

        self.viewer.show_search_result(
            result
        )

        self.search_result_label.setText(
            f"{self.search_index + 1}"
            f" / "
            f"{len(self.search_results)}"
        )
            # ======================================================
    # RAW PDF DOCUMENT
    # ======================================================

    def _get_raw_document(self):

        if not self.pdf_document.is_open:
            return None

        return self.pdf_document.doc

    # ======================================================
    # SAVE CURRENT DOCUMENT CHANGES
    # ======================================================

    def _save_current_document_changes(
        self
    ):

        """
        Try to persist modifications directly.

        Preferred:
            PyMuPDF incremental save.

        Fallback:
            Ask the user for a new PDF path.
        """

        raw_document = (
            self._get_raw_document()
        )

        if raw_document is None:

            return False

        # --------------------------------------------------
        # TRY INCREMENTAL SAVE
        # --------------------------------------------------

        if hasattr(
            raw_document,
            "saveIncr"
        ):

            try:

                raw_document.saveIncr()

                return True

            except Exception:

                pass

        # --------------------------------------------------
        # FALLBACK TO SAVE AS
        # --------------------------------------------------

        file_path, _ = (
            QFileDialog.getSaveFileName(
                self,
                "Save Modified PDF",
                "",
                "PDF Files (*.pdf)"
            )
        )

        if not file_path:

            return False

        if not file_path.lower().endswith(
            ".pdf"
        ):

            file_path += ".pdf"

        try:

            if hasattr(
                raw_document,
                "save"
            ):

                raw_document.save(
                    file_path,
                    garbage=3,
                    deflate=True
                )

                return True

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Save Error",
                str(exc)
            )

        return False

    # ======================================================
    # REFRESH VIEWER AFTER PDF MODIFICATION
    # ======================================================

    def _refresh_viewer_after_document_change(
        self
    ):

        """
        Re-render the current PDF after bookmarks or
        annotations have changed the underlying document.
        """

        current_page = (
            self.viewer.current_page
        )

        try:

            if hasattr(
                self.viewer,
                "render_cache"
            ):

                self.viewer.render_cache.clear()

            if hasattr(
                self.viewer,
                "_rebuild"
            ):

                self.viewer._rebuild()

            else:

                self.viewer.set_document(
                    self.pdf_document
                )

            if (
                self.pdf_document.is_open
                and
                0 <= current_page
                < self.pdf_document.page_count
            ):

                self.viewer.go_to_page(
                    current_page
                )

        except Exception as exc:

            QMessageBox.warning(
                self,
                "Refresh Warning",
                f"The PDF was modified, but the viewer "
                f"could not be refreshed automatically.\n\n"
                f"{exc}"
            )

    # ======================================================
    # BOOKMARKS
    # ======================================================

    def show_bookmarks(
        self
    ):

        if not self.pdf_document.is_open:

            QMessageBox.information(
                self,
                "Bookmarks",
                "Open a PDF first."
            )

            return

        raw_document = (
            self._get_raw_document()
        )

        if raw_document is None:

            QMessageBox.warning(
                self,
                "Bookmarks",
                "The underlying PDF document is not "
                "available."
            )

            return

        try:

            toc = raw_document.get_toc(
                False
            )

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Bookmarks",
                f"Unable to read PDF bookmarks.\n\n"
                f"{exc}"
            )

            return

        dialog = QDialog(
            self
        )

        dialog.setWindowTitle(
            "Bookmarks"
        )

        dialog.resize(
            520,
            500
        )

        layout = QVBoxLayout(
            dialog
        )

        # --------------------------------------------------
        # TITLE
        # --------------------------------------------------

        title = QLabel(
            "PDF Bookmarks"
        )

        title.setStyleSheet(
            """
            QLabel {
                font-size: 16px;
                font-weight: bold;
            }
            """
        )

        layout.addWidget(
            title
        )

        # --------------------------------------------------
        # LIST
        # --------------------------------------------------

        bookmark_list = QListWidget()

        layout.addWidget(
            bookmark_list
        )

        # --------------------------------------------------
        # POPULATE
        # --------------------------------------------------

        bookmark_entries = []

        for index, entry in enumerate(
            toc
        ):

            if len(entry) < 3:
                continue

            level = int(
                entry[0]
            )

            bookmark_title = str(
                entry[1]
            )

            page_number = int(
                entry[2]
            )

            item = QListWidgetItem(
                bookmark_title
            )

            item.setData(
                Qt.ItemDataRole.UserRole,
                page_number
            )

            # Indent according to bookmark level.
            item.setText(
                (
                    "    "
                    * max(
                        0,
                        level - 1
                    )
                )
                + bookmark_title
            )

            bookmark_list.addItem(
                item
            )

            bookmark_entries.append(
                (
                    index,
                    level,
                    bookmark_title,
                    page_number
                )
            )

        if not bookmark_entries:

            empty_item = QListWidgetItem(
                "No bookmarks in this PDF."
            )

            empty_item.setFlags(
                Qt.ItemFlag.NoItemFlags
            )

            bookmark_list.addItem(
                empty_item
            )

        # --------------------------------------------------
        # NAVIGATION
        # --------------------------------------------------

        def open_selected_bookmark():

            item = (
                bookmark_list.currentItem()
            )

            if item is None:
                return

            page_number = item.data(
                Qt.ItemDataRole.UserRole
            )

            if page_number is None:
                return

            try:

                page_index = (
                    int(page_number) - 1
                )

            except (
                TypeError,
                ValueError
            ):

                return

            dialog.accept()

            self.go_to_page(
                page_index
            )

        bookmark_list.itemDoubleClicked.connect(
            lambda item:
            open_selected_bookmark()
        )

        # --------------------------------------------------
        # BUTTONS
        # --------------------------------------------------

        button_layout = QHBoxLayout()

        add_button = QPushButton(
            "+ Add Current Page"
        )

        add_button.setToolTip(
            "Create a bookmark for the current page"
        )

        add_button.clicked.connect(
            lambda:
            self._add_current_page_bookmark(
                dialog,
                bookmark_list
            )
        )

        button_layout.addWidget(
            add_button
        )

        open_button = QPushButton(
            "Open"
        )

        open_button.clicked.connect(
            open_selected_bookmark
        )

        button_layout.addWidget(
            open_button
        )

        close_button = QPushButton(
            "Close"
        )

        close_button.clicked.connect(
            dialog.reject
        )

        button_layout.addWidget(
            close_button
        )

        layout.addLayout(
            button_layout
        )

        dialog.exec()

    # ======================================================
    # ADD CURRENT PAGE BOOKMARK
    # ======================================================

    def _add_current_page_bookmark(
        self,
        dialog=None,
        bookmark_list=None
    ):

        if not self.pdf_document.is_open:

            return

        raw_document = (
            self._get_raw_document()
        )

        if raw_document is None:

            QMessageBox.warning(
                self,
                "Bookmark",
                "The underlying PDF document is "
                "not available."
            )

            return

        current_page = (
            self.viewer.current_page
        )

        page_number = (
            current_page + 1
        )

        title, accepted = (
            QInputDialog.getText(
                self,
                "Add Bookmark",
                "Bookmark name:",
                text=(
                    f"Page {page_number}"
                )
            )
        )

        if not accepted:

            return

        title = title.strip()

        if not title:

            title = (
                f"Page {page_number}"
            )

        try:

            toc = raw_document.get_toc(
                False
            )

            # Add a top-level bookmark.
            toc.append(
                [
                    1,
                    title,
                    page_number
                ]
            )

            raw_document.set_toc(
                toc
            )

            saved = (
                self._save_current_document_changes()
            )

            if not saved:

                QMessageBox.information(
                    self,
                    "Bookmark Added",
                    "The bookmark was added to the "
                    "current document session.\n\n"
                    "Save the PDF to keep the change."
                )

            else:

                QMessageBox.information(
                    self,
                    "Bookmark Added",
                    f"Bookmark '{title}' added "
                    f"for page {page_number}."
                )

            # Refresh bookmark list.
            if dialog is not None:

                dialog.accept()

                self.show_bookmarks()

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Bookmark Error",
                str(exc)
            )

    # ======================================================
    # ANNOTATIONS
    # ======================================================

    def show_annotations(
        self
    ):

        if not self.pdf_document.is_open:

            QMessageBox.information(
                self,
                "Annotations",
                "Open a PDF first."
            )

            return

        raw_document = (
            self._get_raw_document()
        )

        if raw_document is None:

            QMessageBox.warning(
                self,
                "Annotations",
                "The underlying PDF document is "
                "not available."
            )

            return

        # --------------------------------------------------
        # CHECK CURRENT SELECTION
        # --------------------------------------------------

        selection = getattr(
            self.viewer,
            "text_selection",
            None
        )

        selected_words = []

        if selection is not None:

            selected_words = list(
                getattr(
                    selection,
                    "selected_words",
                    []
                )
            )

        # --------------------------------------------------
        # COUNT EXISTING ANNOTATIONS
        # --------------------------------------------------

        annotation_count = 0

        try:

            for page_number in range(
                raw_document.page_count
            ):

                page = raw_document.load_page(
                    page_number
                )

                annotations = page.annots()

                if annotations:

                    for _ in annotations:

                        annotation_count += 1

        except Exception:

            annotation_count = 0

        # --------------------------------------------------
        # IF NO SELECTION
        # --------------------------------------------------

        if not selected_words:

            QMessageBox.information(
                self,
                "Annotations",
                f"Existing annotations: "
                f"{annotation_count}\n\n"
                "To create a highlight annotation:\n"
                "1. Select text in the PDF.\n"
                "2. Click the Annotation button again."
            )

            return

        # --------------------------------------------------
        # CREATE HIGHLIGHTS
        # --------------------------------------------------

        try:

            grouped_words = {}

            for word in selected_words:

                page_number = int(
                    word.page_number
                )

                grouped_words.setdefault(
                    page_number,
                    []
                ).append(
                    word
                )

            created_count = 0

            for page_number, words in (
                grouped_words.items()
            ):

                if not (
                    0 <= page_number
                    < raw_document.page_count
                ):

                    continue

                page = raw_document.load_page(
                    page_number
                )

                rectangles = []

                for word in words:

                    rect = pymupdf.Rect(
                        float(word.x0),
                        float(word.y0),
                        float(
                            word.x0
                            + word.width
                        ),
                        float(
                            word.y0
                            + word.height
                        )
                    )

                    if (
                        rect.is_empty
                        or rect.is_infinite
                    ):

                        continue

                    rectangles.append(
                        rect
                    )

                if not rectangles:

                    continue

                # PyMuPDF supports multiple rectangles
                # for a single highlight annotation.
                annotation = (
                    page.add_highlight_annot(
                        rectangles
                    )
                )

                if annotation is not None:

                    try:

                        annotation.set_colors(
                            stroke=(
                                1.0,
                                1.0,
                                0.0
                            )
                        )

                        annotation.update()

                    except Exception:

                        pass

                    created_count += 1

            if created_count == 0:

                QMessageBox.warning(
                    self,
                    "Annotations",
                    "No valid annotation area was found."
                )

                return

            # ------------------------------------------------
            # SAVE
            # ------------------------------------------------

            saved = (
                self._save_current_document_changes()
            )

            # ------------------------------------------------
            # REFRESH
            # ------------------------------------------------

            self._refresh_viewer_after_document_change()

            # Clear text selection after annotation.
            try:

                self.viewer.clear_text_selection()

            except Exception:

                pass

            if saved:

                QMessageBox.information(
                    self,
                    "Annotation Added",
                    f"{created_count} highlight "
                    f"annotation(s) added and saved."
                )

            else:

                QMessageBox.information(
                    self,
                    "Annotation Added",
                    f"{created_count} highlight "
                    f"annotation(s) added.\n\n"
                    "The changes are currently in memory. "
                    "Use Save As to permanently save them."
                )

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Annotation Error",
                str(exc)
            )

    # ======================================================
    # PRINT
    # ======================================================

    def print_pdf(
        self
    ):

        if not self.pdf_document.is_open:

            QMessageBox.information(
                self,
                "No PDF",
                "Open a PDF first."
            )

            return

        raw_document = (
            self._get_raw_document()
        )

        if raw_document is None:

            QMessageBox.warning(
                self,
                "Print",
                "The underlying PDF document "
                "is not available."
            )

            return

        printer = QPrinter(
            QPrinter.PrinterMode.HighResolution
        )

        printer.setDocName(
            Path(
                self.pdf_document.file_path
            ).stem
        )

        dialog = QPrintDialog(
            printer,
            self
        )

        dialog.setWindowTitle(
            "Print PDF"
        )

        if (
            dialog.exec()
            != QDialog.DialogCode.Accepted
        ):

            return

        try:

            self._print_document(
                printer,
                raw_document
            )

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Print Error",
                str(exc)
            )

    # ======================================================
    # PRINT DOCUMENT
    # ======================================================

    def _print_document(
        self,
        printer,
        raw_document
    ):

        painter = QPainter()

        if not painter.begin(
            printer
        ):

            raise RuntimeError(
                "Unable to start the printer."
            )

        try:

            page_count = (
                raw_document.page_count
            )

            for page_number in range(
                page_count
            ):

                page = raw_document.load_page(
                    page_number
                )

                page_rect = page.rect

                # ------------------------------------------------
                # PRINT RESOLUTION
                # ------------------------------------------------

                dpi = 150

                scale = (
                    dpi / 72.0
                )

                matrix = pymupdf.Matrix(
                    scale,
                    scale
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

                # ------------------------------------------------
                # PRINTER AREA
                # ------------------------------------------------

                target_rect = (
                    printer.pageRect(
                        QPrinter.Unit.DevicePixel
                    )
                )

                if (
                    page_rect.width
                    > page_rect.height
                ):

                    painter.setViewport(
                        target_rect.x(),
                        target_rect.y(),
                        target_rect.height(),
                        target_rect.width()
                    )

                else:

                    painter.setViewport(
                        target_rect.x(),
                        target_rect.y(),
                        target_rect.width(),
                        target_rect.height()
                    )

                painter.setWindow(
                    0,
                    0,
                    image.width(),
                    image.height()
                )

                painter.drawImage(
                    0,
                    0,
                    image
                )

                if (
                    page_number
                    < page_count - 1
                ):

                    printer.newPage()

        finally:

            painter.end()

    # ======================================================
    # PRINT PREVIEW
    # ======================================================

    def print_preview(
        self
    ):

        if not self.pdf_document.is_open:

            QMessageBox.information(
                self,
                "No PDF",
                "Open a PDF first."
            )

            return

        raw_document = (
            self._get_raw_document()
        )

        if raw_document is None:

            return

        printer = QPrinter(
            QPrinter.PrinterMode.HighResolution
        )

        preview = QPrintPreviewDialog(
            printer,
            self
        )

        preview.setWindowTitle(
            "MYpdf Reader - Print Preview"
        )

        preview.paintRequested.connect(
            lambda printer:
            self._print_document(
                printer,
                raw_document
            )
        )

        preview.exec()

    # ======================================================
    # DOCUMENT INFORMATION
    # ======================================================

    def show_document_info(
        self
    ):

        if not self.pdf_document.is_open:

            QMessageBox.information(
                self,
                "Document Information",
                "Open a PDF first."
            )

            return

        filename = Path(
            self.pdf_document.file_path
        ).name

        page_count = (
            self.pdf_document.page_count
        )

        raw_document = (
            self._get_raw_document()
        )

        annotation_count = 0

        bookmark_count = 0

        if raw_document is not None:

            try:

                toc = raw_document.get_toc(
                    False
                )

                bookmark_count = len(
                    toc
                )

            except Exception:

                pass

            try:

                for page_number in range(
                    raw_document.page_count
                ):

                    page = raw_document.load_page(
                        page_number
                    )

                    annotations = page.annots()

                    if annotations:

                        for _ in annotations:

                            annotation_count += 1

            except Exception:

                pass

        QMessageBox.information(
            self,
            "Document Information",
            f"File: {filename}\n\n"
            f"Pages: {page_count}\n"
            f"Bookmarks: {bookmark_count}\n"
            f"Annotations: {annotation_count}"
        )

            # ======================================================
    # PAGE NAVIGATION
    # ======================================================

    def go_to_page(
        self,
        page_number
    ):

        if not self.pdf_document.is_open:

            return

        if not (
            0 <= page_number
            < self.pdf_document.page_count
        ):

            return

        current = (
            self.viewer.current_page
        )

        if page_number == current:

            return

        self.history.push(
            page_number
        )

        self.viewer.go_to_page(
            page_number
        )

    # ======================================================

    def previous_page(
        self
    ):

        if not self.pdf_document.is_open:

            return

        current = (
            self.viewer.current_page
        )

        if current <= 0:

            return

        page = current - 1

        self.history.push(
            page
        )

        self.viewer.go_to_page(
            page
        )

    # ======================================================

    def next_page(
        self
    ):

        if not self.pdf_document.is_open:

            return

        current = (
            self.viewer.current_page
        )

        last_page = (
            self.pdf_document.page_count
            - 1
        )

        if current >= last_page:

            return

        page = current + 1

        self.history.push(
            page
        )

        self.viewer.go_to_page(
            page
        )

    # ======================================================

    def go_first_page(
        self
    ):

        if not self.pdf_document.is_open:

            return

        if self.viewer.current_page == 0:

            return

        self.history.push(
            0
        )

        self.viewer.go_to_page(
            0
        )

    # ======================================================

    def go_last_page(
        self
    ):

        if not self.pdf_document.is_open:

            return

        last_page = (
            self.pdf_document.page_count
            - 1
        )

        if (
            self.viewer.current_page
            == last_page
        ):

            return

        self.history.push(
            last_page
        )

        self.viewer.go_to_page(
            last_page
        )

    # ======================================================
    # PAGE INPUT
    # ======================================================

    def page_input_changed(
        self
    ):

        if not self.pdf_document.is_open:

            return

        try:

            page = int(
                self.page_input.text()
            )

        except ValueError:

            self.update_page_input()

            return

        page_index = (
            page - 1
        )

        if (
            0 <= page_index
            < self.pdf_document.page_count
        ):

            self.go_to_page(
                page_index
            )

        else:

            self.update_page_input()

    # ======================================================
    # HISTORY
    # ======================================================

    def go_back(
        self
    ):

        page = self.history.back()

        if page is None:

            return

        self.viewer.go_to_page(
            page
        )

    # ======================================================

    def go_forward(
        self
    ):

        page = self.history.forward()

        if page is None:

            return

        self.viewer.go_to_page(
            page
        )

    # ======================================================
    # PAGE CHANGED
    # ======================================================

    def on_page_changed(
        self,
        page_number
    ):

        self.update_page_input()

        if self.pdf_document.is_open:

            self.sidebar.select_page(
                page_number
            )

            self.status_label.setText(
                f"Page {page_number + 1}"
                f" / "
                f"{self.pdf_document.page_count}"
            )

        self.update_history_buttons()

    # ======================================================
    # PAGE INPUT UPDATE
    # ======================================================

    def update_page_input(
        self
    ):

        if self.pdf_document.is_open:

            self.page_input.setText(
                str(
                    self.viewer.current_page
                    + 1
                )
            )

            self.page_count_label.setText(
                f"/ "
                f"{self.pdf_document.page_count}"
            )

        else:

            self.page_input.clear()

            self.page_count_label.setText(
                "/ 0"
            )

    # ======================================================
    # HISTORY BUTTONS
    # ======================================================

    def update_history_buttons(
        self
    ):

        self.back_action.setEnabled(
            self.history.can_go_back
        )

        self.forward_action.setEnabled(
            self.history.can_go_forward
        )

    # ======================================================
    # DOCUMENT UI
    # ======================================================

    def update_document_ui(
        self
    ):

        if not self.pdf_document.is_open:

            return

        filename = Path(
            self.pdf_document.file_path
        ).name

        self.setWindowTitle(
            f"{filename} - MYpdf Reader"
        )

        self.update_page_input()

        self.update_history_buttons()

        self.status_label.setText(
            f"Page 1 / "
            f"{self.pdf_document.page_count}"
        )

    # ======================================================
    # CLOSE PDF
    # ======================================================

    def close_pdf(
        self
    ):

        self.pdf_document.close()

        self.viewer.clear()

        self.sidebar.set_document(
            None
        )

        self.text_search.set_document(
            None
        )

        self.search_results.clear()

        self.search_index = -1

        self.history.clear()

        self.setWindowTitle(
            "MYpdf Reader"
        )

        self.update_page_input()

        self.update_history_buttons()

        self.status_label.setText(
            "No document open"
        )

        self.close_search()

    # ======================================================
    # DRAG ENTER
    # ======================================================

    def dragEnterEvent(
        self,
        event
    ):

        if event.mimeData().hasUrls():

            for url in event.mimeData().urls():

                if url.toLocalFile().lower().endswith(
                    ".pdf"
                ):

                    event.acceptProposedAction()

                    return

        event.ignore()

    # ======================================================
    # DROP
    # ======================================================

    def dropEvent(
        self,
        event
    ):

        for url in event.mimeData().urls():

            path = url.toLocalFile()

            if path.lower().endswith(
                ".pdf"
            ):

                self.load_pdf(
                    path
                )

                event.acceptProposedAction()

                return

        event.ignore()

    # ======================================================
    # CLOSE APPLICATION
    # ======================================================

    def closeEvent(
        self,
        event
    ):

        try:

            self.pdf_document.close()

        except Exception:

            pass

        event.accept()