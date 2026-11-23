"""Transcript chunking.

Day 1: simple fixed-size chunking (baseline).
Day 3: add embedding-based topic segmentation and compare the two in your evaluation.
"""


def fixed_chunks(transcript: str, max_words: int = 250) -> list[str]:
    """Split transcript lines into chunks of roughly max_words words."""
    chunks, current, count = [], [], 0
    for line in transcript.splitlines():
        line = line.strip()
        if not line:
            continue
        n = len(line.split())
        if current and count + n > max_words:
            chunks.append("\n".join(current))
            current, count = [], 0
        current.append(line)
        count += n
    if current:
        chunks.append("\n".join(current))
    return chunks
