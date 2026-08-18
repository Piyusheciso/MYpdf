from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Annotation:
    """
    Represents a PDF annotation.

    Currently supports text highlights.

    Coordinates are stored in PDF coordinates,
    not screen/scene coordinates.

    This makes annotations independent of:
        - zoom level
        - window size
        - scrolling
        - rotation
    """

    annotation_type: str = "highlight"

    page_number: int = 0

    # --------------------------------------------------
    # Highlight rectangles
    #
    # Each rectangle is stored as:
    #
    # (x0, y0, x1, y1)
    #
    # in PDF coordinates.
    # --------------------------------------------------

    rects: List[tuple] = field(
        default_factory=list
    )

    # --------------------------------------------------
    # Optional text associated with annotation
    # --------------------------------------------------

    text: str = ""

    # --------------------------------------------------
    # Annotation color
    #
    # Stored as RGBA.
    # --------------------------------------------------

    color: tuple = (
        255,
        235,
        59,
        110
    )

    # --------------------------------------------------
    # Optional identifier
    # --------------------------------------------------

    annotation_id: Optional[int] = None

    # ==================================================
    # ADD RECTANGLE
    # ==================================================

    def add_rect(
        self,
        x0,
        y0,
        x1,
        y1
    ):

        self.rects.append(
            (
                float(x0),
                float(y0),
                float(x1),
                float(y1)
            )
        )

    # ==================================================
    # HAS RECTANGLES
    # ==================================================

    @property
    def has_rects(
        self
    ):

        return bool(
            self.rects
        )

    # ==================================================
    # SET TEXT
    # ==================================================

    def set_text(
        self,
        text
    ):

        self.text = (
            text
            or ""
        )

    # ==================================================
    # SERIALIZE
    # ==================================================

    def to_dict(
        self
    ):

        return {
            "annotation_type":
                self.annotation_type,

            "page_number":
                self.page_number,

            "rects":
                [
                    list(rect)
                    for rect in self.rects
                ],

            "text":
                self.text,

            "color":
                list(self.color),

            "annotation_id":
                self.annotation_id,
        }

    # ==================================================
    # DESERIALIZE
    # ==================================================

    @classmethod
    def from_dict(
        cls,
        data
    ):

        annotation = cls(
            annotation_type=data.get(
                "annotation_type",
                "highlight"
            ),

            page_number=int(
                data.get(
                    "page_number",
                    0
                )
            ),

            text=data.get(
                "text",
                ""
            ),

            color=tuple(
                data.get(
                    "color",
                    (
                        255,
                        235,
                        59,
                        110
                    )
                )
            ),

            annotation_id=data.get(
                "annotation_id"
            )
        )

        for rect in data.get(
            "rects",
            []
        ):

            if len(rect) != 4:
                continue

            annotation.add_rect(
                rect[0],
                rect[1],
                rect[2],
                rect[3]
            )

        return annotation