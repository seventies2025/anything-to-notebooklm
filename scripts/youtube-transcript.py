#!/usr/bin/env python3
"""
YouTube transcript extractor for anything-to-notebooklm skill.
Usage: python3 youtube-transcript.py <url> [--lang zh_Hans] [--output FILE]
"""
import sys
import os
import subprocess
import json
import re

def get_video_id(url):
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'^([0-9A-Za-z_-]{11})$'
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return None

def has_subtitles(yt_dlp_path="yt-dlp"):
    try:
        subprocess.run([yt_dlp_path, "--version"], capture_output=True, timeout=5)
        return True
    except Exception:
        return False

def extract_transcript(url, lang="zh_Hans", output_file=None):
    vid = get_video_id(url)
    if not vid:
        print(f"Could not parse video ID from: {url}", file=sys.stderr)
        sys.exit(1)

    # Try to get subtitles with yt-dlp
    cmd = [
        "yt-dlp",
        "--write-subs", "--write-auto-subs",
        "--sub-langs", lang,
        "--skip-download",
        "--convert-subs", "vtt",
        "-o", "/tmp/youtube_extract",
        f"https://www.youtube.com/watch?v={vid}"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except Exception as e:
        print(f"yt-dlp failed: {e}", file=sys.stderr)
        return None

    # Find the VTT file
    vtt_files = [f for f in os.listdir("/tmp") if f.startswith("youtube_extract") and f.endswith(".vtt")]
    if not vtt_files:
        # Try to get description as fallback
        try:
            desc_cmd = ["yt-dlp", "--get-description", f"https://www.youtube.com/watch?v={vid}"]
            desc_result = subprocess.run(desc_cmd, capture_output=True, text=True, timeout=30)
            if desc_result.returncode == 0 and desc_result.stdout.strip():
                text = desc_result.stdout.strip()
                if output_file:
                    with open(output_file, "w") as f:
                        f.write(text)
                print(text)
                return
        except Exception:
            pass
        print("No subtitles found and description fallback failed.", file=sys.stderr)
        sys.exit(1)

    vtt_path = f"/tmp/{vtt_files[0]}"
    with open(vtt_path, "r", encoding="utf-8") as f:
        vtt_content = f.read()

    # Parse VTT → plain text
    lines = vtt_content.split("\n")
    text_lines = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:"):
            continue
        if "-->" in line:
            continue
        text_lines.append(line)

    text = "\n".join(text_lines)
    text = re.sub(r"\s+", " ", text).strip()

    # Clean up temp files
    for f in os.listdir("/tmp"):
        if f.startswith("youtube_extract"):
            os.remove(f"/tmp/{f}")

    if output_file:
        with open(output_file, "w") as f:
            f.write(text)

    print(text)

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]

    url = args[0] if args else None
    if not url:
        print("Usage: youtube-transcript.py <url> [--lang LANG] [--output FILE]", file=sys.stderr)
        sys.exit(1)

    lang = "zh_Hans"
    output = None

    for f in flags:
        if f.startswith("--lang="):
            lang = f.split("=")[1]
        elif f == "--output":
            idx = flags.index(f)
            if idx + 1 < len(args):
                output = args[idx + 1]

    if not has_subtitles():
        print("yt-dlp not found. Install with: pip3 install yt-dlp", file=sys.stderr)
        sys.exit(1)

    extract_transcript(url, lang, output)

if __name__ == "__main__":
    main()
