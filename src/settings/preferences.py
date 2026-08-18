from PySide6.QtCore import QSettings


class Preferences:

    def __init__(self):

        self.settings = QSettings(
            "PDFReader",
            "PDFReader"
        )

    # --------------------------------------------
    # Window
    # --------------------------------------------

    def save_window_geometry(
        self,
        window
    ):

        self.settings.setValue(
            "window/geometry",
            window.saveGeometry()
        )

        self.settings.setValue(
            "window/state",
            window.saveState()
        )

    # --------------------------------------------

    def restore_window_geometry(
        self,
        window
    ):

        geometry = self.settings.value(
            "window/geometry"
        )

        state = self.settings.value(
            "window/state"
        )

        if geometry:

            window.restoreGeometry(
                geometry
            )

        if state:

            window.restoreState(
                state
            )

    # --------------------------------------------
    # Recent files
    # --------------------------------------------

    def get_recent_files(self):

        files = self.settings.value(
            "recent/files",
            []
        )

        if isinstance(files, str):

            files = [files]

        return files

    # --------------------------------------------

    def add_recent_file(
        self,
        file_path
    ):

        files = self.get_recent_files()

        if file_path in files:

            files.remove(
                file_path
            )

        files.insert(
            0,
            file_path
        )

        files = files[:10]

        self.settings.setValue(
            "recent/files",
            files
        )

    # --------------------------------------------

    def clear_recent_files(self):

        self.settings.setValue(
            "recent/files",
            []
        )