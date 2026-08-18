from dataclasses import dataclass


@dataclass
class Bookmark:
    title: str
    page: int
    level: int = 1

    @property
    def page_number(self):
        return self.page + 1