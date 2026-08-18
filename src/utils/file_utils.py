from pathlib import Path


PDF_FILTER = "PDF Files (*.pdf)"


def is_pdf_file(file_path: str) -> bool:
    return Path(file_path).suffix.lower() == ".pdf"


def get_file_name(file_path: str) -> str:
    return Path(file_path).name