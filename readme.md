# MYpdf Reader

A lightweight desktop PDF reader built with **Python**, **PySide6**, and **PyMuPDF**.

MYpdf Reader is designed as a modular PDF application with a Qt-based user interface, PDF document management, page rendering and navigation, search, bookmarks, annotations, printing, and document information.

---

## Features

### PDF Document Management

- Open PDF files
- Close the current PDF
- Drag and drop PDF files
- Validate selected PDF files
- Detect missing files
- Detect password-protected PDFs
- Track the currently opened document

### PDF Viewer

- Display PDF pages
- Previous / Next page
- First / Last page
- Direct page navigation
- Page number input
- Page count display
- Navigation history
- Back / Forward navigation

### Search

- Search text inside PDFs
- Navigate through search results
- Track the current search result
- Close the search interface

### Bookmarks

- Read existing PDF bookmarks
- Display the PDF table of contents
- Navigate to bookmarked pages
- Add a bookmark for the current page
- Save bookmark changes

### Annotations

- Select text inside the PDF
- Create highlight annotations
- Detect existing annotations
- Save annotation changes
- Refresh the viewer after annotation changes


### Save / Download

- Save modified PDF documents
- Incremental saving where supported
- Save As fallback
- Preserve PDF modifications

### Printing

- Print PDF documents
- Print preview
- Render PDF pages for printing

### Document Information

Displays information including:

- File name
- Number of pages
- Number of bookmarks
- Number of annotations

---

# Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| GUI Framework | PySide6 |
| PDF Engine | PyMuPDF |
| PDF Rendering | PyMuPDF |
| PDF Annotations | PyMuPDF |
| PDF Bookmarks | PyMuPDF |
| Printing | Qt / PySide6 |
| Environment | Python `venv` |

---

# Project Structure

```text
MYpdf Reader/
│
├── src/
│   ├── __init__.py
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── right_panel.py
│   │   └── icons/
│   │
│   ├── pdf/
│   │   ├── __init__.py
│   │   └── document.py
│   │
│   ├── viewer/
│   │   ├── __init__.py
│   │   └── ...
│   │
│   └── utils/
│       ├── __init__.py
│       └── ...
│
├── venv/
│
├── requirements.txt
│
├── main.py
│
└── README.md