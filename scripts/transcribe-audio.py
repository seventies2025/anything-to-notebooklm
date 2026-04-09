#!/usr/bin/env python3
"""
Audio transcription using Whisper (openai-whisper).
Usage: python3 transcribe-audio.py <path> [--model base] [--output FILE]
"""
import sys
import os
import subprocess

def has_whisper():
    try:
        import whisper
        return True
    except ImportError:
        return False

def transcribe(path, model="base", output_file=None):
    cmd = [
        sys.executable, "-c",
        f"""
import whisper
model = whisper.load_model('{model}')
result = model.transcribe('{path}', language='zh')
print(result['text'])
"""
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0 and result.stdout.strip():
            text = result.stdout.strip()
            if output_file:
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(text)
            print(text)
            return
    except Exception as e:
        print(f"Whisper transcription failed: {e}", file=sys.stderr)
    sys.exit(1)

def transcribe_ffmpeg(path, output_file=None):
    """Fallback: use ffmpeg + whisper via base64 temp file approach."""
    # Convert audio to mp3 if needed
    wav_path = "/tmp/audio_transcribe.wav"
    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", path,
            "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le",
            wav_path
        ], capture_output=True, timeout=120)
    except FileNotFoundError:
        print("ffmpeg not found. Install with: brew install ffmpeg", file=sys.stderr)
        sys.exit(1)

    return transcribe(wav_path, output_file=output_file)

def main():
    if not has_whisper():
        print("whisper not installed. Install with: pip3 install openai-whisper", file=sys.stderr)
        sys.exit(1)

    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]

    filepath = args[0] if args else None
    if not filepath or not os.path.exists(filepath):
        print(f"Audio file not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    model = "base"
    output = None

    for f in flags:
        if f.startswith("--model="):
            model = f.split("=")[1]
        elif f == "--output" and flags.index(f) + 1 < len(args):
            output = args[flags.index(f) + 1]

    transcribe(filepath, model, output)

if __name__ == "__main__":
    main()
