from dataclasses import dataclass


@dataclass
class PDFWord:
    text: str

    x0: float
    y0: float
    x1: float
    y1: float

    block_no: int
    line_no: int
    word_no: int

    page_number: int

    @property
    def width(self):
        return self.x1 - self.x0

    @property
    def height(self):
        return self.y1 - self.y0


class PDFTextLayout:

    def __init__(self, document=None):

        self.document = document

        self._cache = {}

    # ==================================================
    # DOCUMENT
    # ==================================================

    def set_document(self, document):

        self.document = document

        self.clear()

    # ==================================================
    # CLEAR
    # ==================================================

    def clear(self):

        self._cache.clear()

    # ==================================================
    # GET PAGE WORDS
    # ==================================================

    def get_words(self, page_number):

        if not self.document:
            return []

        if not self.document.is_open:
            return []

        if page_number in self._cache:

            return self._cache[
                page_number
            ]

        page = self.document.get_page(
            page_number
        )

        raw_words = page.get_text(
            "words"
        )

        words = []

        for item in raw_words:

            if len(item) < 8:
                continue

            (
                x0,
                y0,
                x1,
                y1,
                text,
                block_no,
                line_no,
                word_no
            ) = item[:8]

            if not text.strip():
                continue

            word = PDFWord(
                text=text,

                x0=x0,
                y0=y0,
                x1=x1,
                y1=y1,

                block_no=block_no,
                line_no=line_no,
                word_no=word_no,

                page_number=page_number
            )

            words.append(word)

        self._cache[
            page_number
        ] = words

        return words

    # ==================================================
    # ALL WORDS
    # ==================================================

    def get_all_words(self):

        if not self.document:
            return []

        if not self.document.is_open:
            return []

        words = []

        for page_number in range(
            self.document.page_count
        ):

            words.extend(
                self.get_words(
                    page_number
                )
            )

        return words

    # ==================================================
    # WORD AT POSITION
    # ==================================================

    def word_at(
        self,
        page_number,
        x,
        y
    ):

        words = self.get_words(
            page_number
        )

        for word in words:

            if (
                word.x0 <= x <= word.x1
                and
                word.y0 <= y <= word.y1
            ):

                return word

        # If the click is between words,
        # find the closest word.

        closest = None
        closest_distance = float("inf")

        for word in words:

            center_x = (
                word.x0 + word.x1
            ) / 2

            center_y = (
                word.y0 + word.y1
            ) / 2

            distance = (
                (center_x - x) ** 2
                +
                (center_y - y) ** 2
            )

            if distance < closest_distance:

                closest_distance = distance

                closest = word

        if closest_distance < 400:

            return closest

        return None

    # ==================================================
    # WORD INDEX
    # ==================================================

    def word_index(
        self,
        page_number,
        target
    ):

        words = self.get_words(
            page_number
        )

        for index, word in enumerate(
            words
        ):

            if word is target:

                return index

        return -1

    # ==================================================
    # ORDERED WORDS
    # ==================================================

    def get_ordered_words(
        self,
        page_number
    ):

        words = self.get_words(
            page_number
        )

        return sorted(
            words,
            key=lambda word: (
                word.block_no,
                word.line_no,
                word.word_no
            )
        )

    # ==================================================
    # SELECT BETWEEN WORDS
    # ==================================================

    def select_between(
        self,
        start_page,
        start_word,
        end_page,
        end_word
    ):

        selected = []

        if (
            start_page > end_page
        ):

            start_page, end_page = (
                end_page,
                start_page
            )

            start_word, end_word = (
                end_word,
                start_word
            )

        for page_number in range(
            start_page,
            end_page + 1
        ):

            words = self.get_ordered_words(
                page_number
            )

            if not words:
                continue

            if start_page == end_page:

                start_index = (
                    self.word_index(
                        page_number,
                        start_word
                    )
                )

                end_index = (
                    self.word_index(
                        page_number,
                        end_word
                    )
                )

                if start_index > end_index:

                    start_index, end_index = (
                        end_index,
                        start_index
                    )

                selected.extend(
                    words[
                        start_index:
                        end_index + 1
                    ]
                )

            elif page_number == start_page:

                start_index = (
                    self.word_index(
                        page_number,
                        start_word
                    )
                )

                if start_index >= 0:

                    selected.extend(
                        words[
                            start_index:
                        ]
                    )

            elif page_number == end_page:

                end_index = (
                    self.word_index(
                        page_number,
                        end_word
                    )
                )

                if end_index >= 0:

                    selected.extend(
                        words[
                            :end_index + 1
                        ]
                    )

            else:

                selected.extend(
                    words
                )

        return selected

    # ==================================================
    # WORDS TO TEXT
    # ==================================================

    def words_to_text(
        self,
        words
    ):

        if not words:
            return ""

        result = []

        previous = None

        for word in words:

            if previous is None:

                result.append(
                    word.text
                )

            elif (
                word.page_number
                != previous.page_number
            ):

                result.append(
                    "\n\n"
                )

                result.append(
                    word.text
                )

            elif (
                word.block_no
                != previous.block_no
            ):

                result.append(
                    "\n\n"
                )

                result.append(
                    word.text
                )

            elif (
                word.line_no
                != previous.line_no
            ):

                result.append(
                    "\n"
                )

                result.append(
                    word.text
                )

            else:

                result.append(
                    " "
                )

                result.append(
                    word.text
                )

            previous = word

        return "".join(
            result
        ).strip()