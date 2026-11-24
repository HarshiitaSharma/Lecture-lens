import os
import time

import requests
import streamlit as st

BACKEND = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
st.set_page_config(page_title="Lecture AI", layout="wide")
ss = st.session_state
for k in ("transcript", "summary", "concepts", "quiz"):
    ss.setdefault(k, None)


def post(path, **kw):
    r = requests.post(f"{BACKEND}{path}", timeout=kw.pop("timeout", 300), **kw)
    if not r.ok:
        try:
            msg = r.json().get("detail", r.text)
        except Exception:
            msg = r.text
        raise RuntimeError(msg)
    return r.json()


def transcribe_upload(up):
    info = post("/upload", files={"file": (up.name, up.getvalue())})
    post(f"/transcribe/{info['job_id']}")
    bar = st.progress(0.0, text="Transcribing...")
    start = time.time()
    while time.time() - start < 20 * 60:
        job = requests.get(f"{BACKEND}/jobs/{info['job_id']}", timeout=30).json()
        if job["status"] == "done":
            bar.progress(1.0, text="Done")
            return job["transcript"]
        if job["status"] == "error":
            raise RuntimeError(job["error"])
        bar.progress(float(job.get("progress", 0)), text=f"Transcribing... {int(job.get('progress', 0) * 100)}%")
        time.sleep(2)
    raise RuntimeError("Transcription timed out.")


st.title("Lecture AI")
st.caption("Turn a lecture into a transcript, summary, key concepts and a quiz.")

up = st.file_uploader("Upload a lecture (MP4, MP3, WAV, M4A; max 15 minutes)",
                      type=["mp4", "mkv", "webm", "mp3", "wav", "m4a"])
if up and st.button("Upload and transcribe", type="primary"):
    ss.summary = ss.concepts = ss.quiz = None
    try:
        ss.transcript = transcribe_upload(up)
    except Exception as e:
        st.error(f"Transcription failed: {e}")

with st.expander("Or paste a transcript instead (testing)"):
    pasted = st.text_area("Transcript with [HH:MM:SS] lines", height=150)
    if st.button("Use pasted transcript") and pasted.strip():
        ss.transcript, ss.summary, ss.concepts, ss.quiz = pasted.strip(), None, None, None

if ss.transcript:
    if st.button("Generate study material", type="primary"):
        try:
            with st.spinner("Summarising..."):
                ss.summary = post("/summary", json={"transcript": ss.transcript})["summary"]
            with st.spinner("Extracting key concepts..."):
                ss.concepts = post("/concepts", json={"transcript": ss.transcript})["concepts"]
            with st.spinner("Writing quiz questions..."):
                ss.quiz = post("/quiz", json={"transcript": ss.transcript})["questions"]
        except Exception as e:
            st.error(f"Generation failed: {e}")

    t_tr, t_sum, t_con, t_quiz = st.tabs(["Transcript", "Summary", "Key concepts", "Quiz"])
    with t_tr:
        st.text(ss.transcript)
    with t_sum:
        st.markdown(ss.summary or "_Click 'Generate study material'._")
    with t_con:
        for c in ss.concepts or []:
            st.markdown(f"**{c['term']}** ({c['timestamp']}): {c['definition']}")
        if not ss.concepts:
            st.markdown("_Not generated yet._")
    with t_quiz:
        for i, q in enumerate(ss.quiz or [], 1):
            st.markdown(f"**Q{i}. {q['question']}** _({q['difficulty']})_")
            for j, o in enumerate(q["options"]):
                st.write(f"{'ABCD'[j]}. {o}")
            with st.expander("Show answer"):
                st.write(f"**{'ABCD'[q['answer_index']]}**: {q['explanation']} ({q['timestamp']})")
        if not ss.quiz:
            st.markdown("_Not generated yet._")

    if ss.summary:
        notes = f"# Lecture notes\n\n{ss.summary}\n\n## Key concepts\n" + "\n".join(
            f"- **{c['term']}** ({c['timestamp']}): {c['definition']}" for c in (ss.concepts or []))
        st.download_button("Download notes (.md)", notes, file_name="lecture_notes.md")
