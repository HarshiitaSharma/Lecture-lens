import uuid
from pathlib import Path

from fastapi import BackgroundTasks, FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from . import audio, llm, transcribe

app = FastAPI(title="Lecture AI")
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# In-memory job table (fine for one worker on a demo Space; resets on restart).
JOBS: dict[str, dict] = {}


class TranscriptIn(BaseModel):
    transcript: str


@app.get("/health")
def health():
    return {"status": "ok", "whisper_model": transcribe.MODEL_NAME, "gemini_model": llm.MODEL}


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
    try:
        wav = audio.extract_audio(src, UPLOAD_DIR / f"{job_id}.wav")
    except Exception:
        raise HTTPException(400, "Could not extract audio from this file.")
    finally:
        src.unlink(missing_ok=True)          # keep only the small WAV, save disk space
    return {"job_id": job_id, "duration_sec": round(duration, 1)}


def _run_transcription(job_id: str, wav: Path):
    try:
        def progress(p):
            JOBS[job_id]["progress"] = round(p, 3)
        lines, segs = transcribe.transcribe_file(wav, progress=progress)
        JOBS[job_id].update(status="done", progress=1.0, transcript="\n".join(lines), segments=segs)
    except Exception as e:                    # report instead of hanging the UI
        JOBS[job_id].update(status="error", error=str(e))


@app.post("/transcribe/{job_id}")
def start_transcription(job_id: str, background: BackgroundTasks):
    wav = UPLOAD_DIR / f"{job_id}.wav"
    if not wav.exists():
        raise HTTPException(404, "Unknown job. Upload the file first.")
    if JOBS.get(job_id, {}).get("status") == "running":
        return {"job_id": job_id, "status": "running"}
    JOBS[job_id] = {"status": "running", "progress": 0.0, "transcript": None, "error": None}
    background.add_task(_run_transcription, job_id, wav)
    return {"job_id": job_id, "status": "running"}


@app.get("/jobs/{job_id}")
def job_status(job_id: str):
    if job_id not in JOBS:
        raise HTTPException(404, "Unknown job.")
    return JOBS[job_id]


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
