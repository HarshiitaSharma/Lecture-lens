"""Upload validation and audio extraction with FFmpeg."""
import json
import subprocess
from pathlib import Path

ALLOWED_EXT = {".mp4", ".mkv", ".webm", ".mp3", ".wav", ".m4a"}
MAX_SECONDS = 15 * 60  # MVP limit; show a clear error above this


def probe_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(json.loads(out.stdout)["format"]["duration"])


def extract_audio(src: Path, dst: Path) -> Path:
    """Convert any input to 16 kHz mono WAV, the format Whisper expects."""
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(src), "-vn", "-ac", "1", "-ar", "16000", str(dst)],
        capture_output=True, check=True,
    )
    return dst
