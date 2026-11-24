"""Speech-to-text with faster-whisper (CPU, int8 by default). Configure with env vars:
WHISPER_MODEL (tiny/base/small), WHISPER_DEVICE (cpu/cuda), WHISPER_COMPUTE (int8/float16),
WHISPER_LANGUAGE (en, or 'auto' to detect)."""
import os
import threading
import wave
from pathlib import Path

import numpy as np

MODEL_NAME = os.getenv("WHISPER_MODEL", "base")
DEVICE = os.getenv("WHISPER_DEVICE", "cpu")
COMPUTE = os.getenv("WHISPER_COMPUTE", "int8")
LANGUAGE = os.getenv("WHISPER_LANGUAGE", "en")

_model = None
_model_lock = threading.Lock()
_one_at_a_time = threading.Semaphore(1)   # a CPU Space cannot run two transcriptions at once


def get_model():
    global _model
    with _model_lock:
        if _model is None:
            from faster_whisper import WhisperModel
            _model = WhisperModel(MODEL_NAME, device=DEVICE, compute_type=COMPUTE)
    return _model


def load_wav(path) -> np.ndarray:
    """Read the 16 kHz mono WAV produced by audio.extract_audio (no PyAV needed)."""
    with wave.open(str(path), "rb") as w:
        assert w.getframerate() == 16000 and w.getnchannels() == 1, "expected 16 kHz mono WAV"
        raw = w.readframes(w.getnframes())
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0


def fmt(t: float) -> str:
    return f"{int(t // 3600):02d}:{int(t % 3600 // 60):02d}:{int(t % 60):02d}"


def group(segs, window: float = 30.0) -> list[str]:
    """Merge short Whisper segments into ~30 s lines: '[HH:MM:SS] text'."""
    lines, start, buf = [], None, []
    for s, e, text in segs:
        if start is None:
            start = s
        buf.append(text)
        if e - start >= window:
            lines.append(f"[{fmt(start)}] {' '.join(buf)}")
            start, buf = None, []
    if buf:
        lines.append(f"[{fmt(start)}] {' '.join(buf)}")
    return lines


def transcribe_file(path, progress=None):
    """Returns (lines, segments). progress(p) is called with p in 0..1 as segments arrive."""
    audio = load_wav(path)
    total = len(audio) / 16000
    with _one_at_a_time:
        segments, _ = get_model().transcribe(
            audio, beam_size=5, vad_filter=True,
            language=None if LANGUAGE == "auto" else LANGUAGE)
        segs = []
        for s in segments:                      # the generator does the real work
            segs.append((s.start, s.end, s.text.strip()))
            if progress and total:
                progress(min(0.99, s.end / total))
    return group(segs), [{"start": a, "end": b, "text": t} for a, b, t in segs]
