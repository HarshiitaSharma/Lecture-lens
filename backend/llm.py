"""Gemini wrapper: summaries, concepts, quiz. Model name comes from GEMINI_MODEL."""
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

from . import prompts
from .chunking import fixed_chunks

load_dotenv()
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
_client = None


class Concept(BaseModel):
    term: str
    definition: str
    timestamp: str


class ConceptList(BaseModel):
    concepts: list[Concept]


class MCQ(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    answer_index: int = Field(ge=0, le=3)
    difficulty: str
    explanation: str
    timestamp: str


class Quiz(BaseModel):
    questions: list[MCQ]


def _get_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    return _client


def _generate(prompt: str, schema=None, retries: int = 3):
    kwargs = {"temperature": 0.3}
    if schema is not None:
        kwargs.update(response_mime_type="application/json", response_schema=schema)
    config = types.GenerateContentConfig(**kwargs)
    for attempt in range(retries):
        try:
            return _get_client().models.generate_content(
                model=MODEL, contents=prompt, config=config
            )
        except Exception:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** (attempt + 1))  # back off on rate limits


def summarise_chunked(transcript: str) -> str:
    """Map-reduce summary: summarise each chunk, then combine."""
    parts = [
        _generate(prompts.CHUNK_SUMMARY.format(chunk=c)).text
        for c in fixed_chunks(transcript)
    ]
    return _generate(prompts.COMBINE_SUMMARY.format(parts="\n\n".join(parts))).text


def summarise_single_pass(transcript: str) -> str:
    """Baseline for evaluation: one call with the whole transcript."""
    return _generate(prompts.SINGLE_PASS_SUMMARY.format(transcript=transcript)).text


def extract_concepts(transcript: str) -> list[dict]:
    r = _generate(prompts.CONCEPTS.format(transcript=transcript), schema=ConceptList)
    return [c.model_dump() for c in r.parsed.concepts]


def generate_quiz(transcript: str, n: int = 8) -> list[dict]:
    r = _generate(prompts.QUIZ.format(transcript=transcript, n=n), schema=Quiz)
    return [q.model_dump() for q in r.parsed.questions]
