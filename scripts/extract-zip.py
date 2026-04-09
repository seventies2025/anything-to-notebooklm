#!/usr/bin/env python3
"""
ZIP archive extractor for anything-to-notebooklm skill.
Extracts all files and returns their content summaries.
Usage: python3 extract-zip.py <path> [--output-dir DIR]
"""
import sys
import os
import zipfile
import tempfile
import subprocess

def extract_zip(zip_path, output_dir=None):
    if output_dir is None:
        output_dir = tempfile.mkdtemp(prefix="extracted_")

    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(output_dir)

    return output_dir

def process_extracted_dir(base_dir):
    """Walk extracted directory, convert each file, return combined text."""
    results = []
    supported = {".pdf", ".docx", ".doc", ".pptx", ".ppt", ".xlsx", ".xls",
                 ".epub", ".md", ".txt", ".csv", ".json", ".xml",
                 ".jpg", ".jpeg", ".png", ".gif", ".tiff",
                 ".wav", ".mp3", ".m4a", ".flac"}

    skill_dir = os.path.dirname(os.path.abspath(__file__))
    web_fetch = os.path.join(skill_dir, "web-fetch.py")
    youtube_transcript = os.path.join(skill_dir, "youtube-transcript.py")
    convert_file = os.path.join(skill_dir, "convert-file.py")
    ocr_image = os.path.join(skill_dir, "ocr-image.py")
    transcribe = os.path.join(skill_dir, "transcribe-audio.py")

    for root, dirs, files in os.walk(base_dir):
        for fname in files:
            fpath = os.path.join(root, fname)
            ext = os.path.splitext(fname)[1].lower()
            rel = os.path.relpath(fpath, base_dir)

            if ext == ".zip":
                sub_dir = extract_zip(fpath)
                sub_text = process_extracted_dir(sub_dir)
                results.append(f"\n=== {rel} (nested zip) ===\n{sub_text}")
                continue

            if ext in [".jpg", ".jpeg", ".png", ".gif", ".tiff"]:
                try:
                    r = subprocess.run(
                        [sys.executable, ocr_image, fpath],
                        capture_output=True, text=True, timeout=60
                    )
                    text = r.stdout.strip() if r.returncode == 0 else f"[OCR failed for {rel}]"
                except Exception:
                    text = f"[OCR skipped for {rel}]"
                results.append(f"\n=== {rel} ===\n{text}")
                continue

            if ext in [".wav", ".mp3", ".m4a", ".flac"]:
                results.append(f"\n=== {rel} ===\n[Audio file - use transcribe-audio.py: {fname}]")
                continue

            if ext == ".url":
                results.append(f"\n=== {rel} ===\n[Bookmark file - skipped]")
                continue

            if ext not in supported:
                continue

            try:
                if ext in [".md", ".txt", ".csv", ".json", ".xml"]:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                        text = f.read()
                else:
                    r = subprocess.run(
                        [sys.executable, convert_file, fpath],
                        capture_output=True, text=True, timeout=60
                    )
                    text = r.stdout if r.returncode == 0 else f"[Conversion failed for {rel}]"
            except Exception as e:
                text = f"[Error processing {rel}: {e}]"

            results.append(f"\n=== {rel} ===\n{text[:50000]}")  # Cap per file

    return "\n".join(results)

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]

    zip_path = args[0] if args else None
    if not zip_path or not os.path.exists(zip_path):
        print(f"ZIP file not found: {zip_path}", file=sys.stderr)
        sys.exit(1)

    output_dir = None
    for i, f in enumerate(flags):
        if f == "--output-dir" and i + 1 < len(args):
            output_dir = args[i + 1]

    extract_dir = extract_zip(zip_path, output_dir)
    print(f"Extracted to: {extract_dir}", file=sys.stderr)

    combined = process_extracted_dir(extract_dir)
    print(combined)

if __name__ == "__main__":
    main()
