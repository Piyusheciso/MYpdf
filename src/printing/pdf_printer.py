from PySide6.QtCore import QMarginsF
from PySide6.QtGui import QPageLayout, QPageSize, QPainter
from PySide6.QtPrintSupport import QPrinter, QPrintDialog


class PDFPrinter:

    def print_pdf(
        self,
        parent,
        pdf_document
    ):

        if not pdf_document.is_open:

            return False

        printer = QPrinter(
            QPrinter.PrinterMode.HighResolution
        )

        printer.setPageSize(
            QPageSize(
                QPageSize.PageSizeId.A4
            )
        )

        printer.setPageMargins(
            QMarginsF(
                10,
                10,
                10,
                10
            ),
            QPageLayout.Unit.Millimeter
        )

        dialog = QPrintDialog(
            printer,
            parent
        )

        dialog.setWindowTitle(
            "Print PDF"
        )

        result = dialog.exec()

        if result != QPrintDialog.DialogCode.Accepted:

            return False

        painter = QPainter()

        if not painter.begin(printer):

            return False

        try:

            page_count = (
                pdf_document.page_count
            )

            first_page = 0
            last_page = page_count - 1

            for page_number in range(
                first_page,
                last_page + 1
            ):

                page = pdf_document.document[
                    page_number
                ]

                rect = printer.pageRect(
                    QPrinter.Unit.DevicePixel
                )

                page_width = rect.width()
                page_height = rect.height()

                pixmap = page.get_pixmap(
                    matrix=page.get_pixmap(
                        matrix=None
                    ).matrix
                    if False
                    else None
                )

                # Render at a reasonable resolution.
                pixmap = page.get_pixmap(
                    dpi=150,
                    alpha=False
                )

                from PySide6.QtGui import QImage

                image = QImage(
                    pixmap.samples,
                    pixmap.width,
                    pixmap.height,
                    pixmap.stride,
                    QImage.Format.Format_RGB888
                )

                scaled = image.scaled(
                    page_width,
                    page_height,
                    aspectRatioMode=1,
                    transformMode=1
                )

                painter.drawImage(
                    0,
                    0,
                    scaled
                )

                if page_number < last_page:

                    printer.newPage()

        finally:

            painter.end()

        return True