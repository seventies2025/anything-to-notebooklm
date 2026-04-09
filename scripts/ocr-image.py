#!/usr/bin/env python3
"""
OCR for images (JPEG/PNG/GIF/TIFF) using tesseract.
Usage: python3 ocr-image.py <path> [--lang chi_sim+eng] [--output FILE]
"""
import sys
import os
import subprocess

TESSERACT_CMD = "tesseract"

def has_tesseract():
    try:
        subprocess.run([TESSERACT_CMD, "--version"], capture_output=True, timeout=5)
        return True
    except FileNotFoundError:
        return False

def ocr_image(path, lang="chi_sim+eng", output_file=None):
    cmd = [TESSERACT_CMD, path, "stdout", "-l", lang]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            text = result.stdout.strip()
            if output_file:
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(text)
            print(text)
            return
    except Exception as e:
        print(f"Tesseract OCR failed: {e}", file=sys.stderr)
    sys.exit(1)

def main():
    if not has_tesseract():
        print("tesseract not found. Install: brew install tesseract tesseract-lang (macOS) or apt install tesseract-ocr tesseract-ocr-chi-sim (Linux)", file=sys.stderr)
        sys.exit(1)

    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]

    filepath = args[0] if args else None
    if not filepath or not os.path.exists(filepath):
        print(f"Image file not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    lang = "chi_sim+eng"
    output = None

    for f in flags:
        if f.startswith("--lang="):
            lang = f.split("=")[1]
        elif f == "--output" and flags.index(f) + 1 < len(args):
            output = args[flags.index(f) + 1]

    ocr_image(filepath, lang, output)

if __name__ == "__main__":
    main()
