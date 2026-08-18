from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QTreeWidget,
    QTreeWidgetItem,
)


class OutlinePanel(QTreeWidget):

    page_selected = Signal(int)

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setHeaderLabel(
            "Document Outline"
        )

        self.itemClicked.connect(
            self._item_clicked
        )

    def set_document(self, document):

        self.clear()

        if (
            not document
            or not document.is_open
        ):
            return

        toc = document.get_toc()

        if not toc:
            return

        stack = []

        for level, title, page in toc:

            item = QTreeWidgetItem()

            item.setText(
                0,
                title
            )

            item.setData(
                0,
                Qt.ItemDataRole.UserRole,
                page - 1
            )

            if level == 1:

                self.addTopLevelItem(
                    item
                )

                stack = [item]

            else:

                while len(stack) >= level:

                    stack.pop()

                if stack:

                    stack[-1].addChild(
                        item
                    )

                else:

                    self.addTopLevelItem(
                        item
                    )

                stack.append(item)

        self.expandAll()

    def _item_clicked(
        self,
        item,
        column
    ):

        page = item.data(
            0,
            Qt.ItemDataRole.UserRole
        )

        if page is not None:

            self.page_selected.emit(
                page
            )