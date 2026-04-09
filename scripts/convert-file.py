#!/usr/bin/env python3
"""
File converter for anything-to-notebooklm skill.
Supports: PDF, DOCX, PPTX, XLSX, EPUB via markitdown.
Usage: python3 convert-file.py <path> [--output FILE]
"""
import sys
import os
import subprocess
import tempfile

MARKITDOWN_CMD = "markitdown"

def convert_with_markitdown(path):
    """Use Microsoft markitdown to convert office/docs to markdown."""
    try:
        result = subprocess.run(
            [MARKITDOWN_CMD, path],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            return result.stdout
    except FileNotFoundError:
        pass
    return None

def convert_pdf_fallback(path):
    """Fallback for PDF: extract text with pdftotext."""
    try:
        result = subprocess.run(
            ["pdftotext", "-enc", "UTF-8", path, "-"],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout
    except FileNotFoundError:
        pass
    return None

def detect_and_convert(path):
    ext = os.path.splitext(path)[1].lower()

    if ext in [".pdf", ".docx", ".doc", ".pptx", ".ppt", ".xlsx", ".xls", ".epub", ".odt"]:
        content = convert_with_markitdown(path)
        if content:
            return content

    if ext == ".pdf":
        content = convert_pdf_fallback(path)
        if content:
            return content
        return "PDF text extraction failed. File may be scanned (use OCR)."

    if ext in [".md", ".txt", ".csv", ".json", ".xml"]:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    return f"Unsupported file type: {ext}"

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]

    filepath = args[0] if args else None
    if not filepath or not os.path.exists(filepath):
        print(f"File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    output_file = None
    for i, f in enumerate(flags):
        if f == "--output" and i + 1 < len(args):
            output_file = args[i + 1]

    content = detect_and_convert(filepath)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)

    print(content)

if __name__ == "__main__":
    main()
