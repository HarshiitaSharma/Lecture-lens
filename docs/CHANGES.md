# What changed since the earlier zips (replace everything with this zip)

If you already uploaded or edited files, just **replace the whole project with this version**. Files that changed or are new:

| File | Status | What changed |
|---|---|---|
| `backend/main.py` | updated | Fixed WAV upload bug (source and output had the same filename); background transcription jobs |
| `backend/transcribe.py` | new | faster-whisper on CPU, reads WAV directly, timestamped lines |
| `backend/llm.py`, `prompts.py`, `chunking.py`, `audio.py` | unchanged logic | Gemini wrapper, prompts, fixed chunking, FFmpeg helpers |
| `frontend/app.py` | updated | Upload, progress bar, tabs, notes download |
| `requirements.txt` | updated | adds faster-whisper, numpy |
| `Dockerfile`, `start.sh`, `.dockerignore` | new | Docker deployment on Hugging Face |
| `notebooks/01_whisper_evaluation.ipynb` | updated | PDF alignment, CUDA 12 fix, GPU fallback |
| `notebooks/02_summary_quiz_evaluation.ipynb` | updated | Colab-only setup, reference summaries step |
| `notebooks/03_backend_test_and_deploy.ipynb` | new | Backend tests and Hugging Face deploy |
| `README.md` | rewritten | Matches the submission checklist; fill in the marked placeholders |
| `docs/` | new | architecture diagram, work plan, report outline |

After replacing the zip in Drive: use **Runtime > Restart session** in Colab before re-running notebooks.

## Latest fix: notebook 02 timeouts
| File | What changed |
|---|---|
| `backend/llm.py` | 90 s timeout per Gemini request; retries 429/503/timeouts using the delay Gemini asks for; wrong model names or bad keys fail immediately with a clear message |
| `backend/chunking.py` | default chunk size 250 -> 500 words (about half the API calls) |
| `notebooks/02_summary_quiz_evaluation.ipynb` | every Gemini answer cached in Drive so re-runs resume; topic chunking off by default (`RUN_TOPIC_CHUNKS`); progress dots |
