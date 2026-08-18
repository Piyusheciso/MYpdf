"""
Annotation package for MYpdf Reader.

This package contains the annotation data model
and annotation management functionality.
"""

from .annotation import Annotation
from .annotation_manager import AnnotationManager

__all__ = [
    "Annotation",
    "AnnotationManager",
]