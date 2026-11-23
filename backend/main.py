import uuid
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from . import audio, llm

app = FastAPI(title="Lecture AI")
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


class TranscriptIn(BaseModel):
    transcript: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    ext = Path(file.filename or "").suffix.lower()
    if ext not in audio.ALLOWED_EXT:
        raise HTTPException(400, f"Unsupported file type '{ext}'. Use: {sorted(audio.ALLOWED_EXT)}")
    job_id = uuid.uuid4().hex[:8]
    src = UPLOAD_DIR / f"{job_id}{ext}"
    src.write_bytes(await file.read())
    try:
        duration = audio.probe_duration(src)
    except Exception:
        src.unlink(missing_ok=True)
        raise HTTPException(400, "Could not read this file. It may be corrupted.")
    if duration > audio.MAX_SECONDS:
        src.unlink(missing_ok=True)
        raise HTTPException(400, f"File is {duration/60:.1f} min; the limit is {audio.MAX_SECONDS//60} min.")
    wav = audio.extract_audio(src, UPLOAD_DIR / f"{job_id}.wav")
    # Day 2: add POST /transcribe/{job_id} using faster-whisper
    return {"job_id": job_id, "duration_sec": round(duration, 1), "audio": wav.name}


@app.post("/summary")
def summary(body: TranscriptIn, mode: str = "chunked"):
    fn = llm.summarise_chunked if mode == "chunked" else llm.summarise_single_pass
    return {"summary": fn(body.transcript)}


@app.post("/concepts")
def concepts(body: TranscriptIn):
    return {"concepts": llm.extract_concepts(body.transcript)}


@app.post("/quiz")
def quiz(body: TranscriptIn, n: int = 8):
    return {"questions": llm.generate_quiz(body.transcript, n)}
