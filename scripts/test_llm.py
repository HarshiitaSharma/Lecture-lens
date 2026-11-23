"""Day 1 check: run the Gemini pipeline on the sample transcript (no backend needed).
Run from the repo root:  python -m scripts.test_llm
"""
import json
from pathlib import Path

from backend import llm

t = Path("data/sample_transcript.txt").read_text()
print("MODEL:", llm.MODEL)
print("\n--- SUMMARY (chunked) ---\n", llm.summarise_chunked(t))
print("\n--- CONCEPTS ---\n", json.dumps(llm.extract_concepts(t), indent=2))
print("\n--- QUIZ ---\n", json.dumps(llm.generate_quiz(t, 5), indent=2))
