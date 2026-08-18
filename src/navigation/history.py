class NavigationHistory:
    """
    Manages page navigation history.
    """

    def __init__(self):

        self._history = []
        self._position = -1

    def clear(self):

        self._history.clear()
        self._position = -1

    @property
    def can_go_back(self):

        return self._position > 0

    @property
    def can_go_forward(self):

        return (
            self._position >= 0
            and self._position
            < len(self._history) - 1
        )

    def push(self, page_number: int):

        # Don't add duplicate consecutive pages.
        if (
            self._history
            and self._history[self._position]
            == page_number
        ):
            return

        # Remove forward history.
        if self._position < len(self._history) - 1:

            self._history = (
                self._history[:self._position + 1]
            )

        self._history.append(
            page_number
        )

        self._position = (
            len(self._history) - 1
        )

    def back(self):

        if not self.can_go_back:
            return None

        self._position -= 1

        return self._history[
            self._position
        ]

    def forward(self):

        if not self.can_go_forward:
            return None

        self._position += 1

        return self._history[
            self._position
        ]

    @property
    def current(self):

        if (
            self._position < 0
            or not self._history
        ):
            return None

        return self._history[
            self._position
        ]