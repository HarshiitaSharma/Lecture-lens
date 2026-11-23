import os

import requests
import streamlit as st

BACKEND = os.getenv("BACKEND_URL", "http://localhost:8000")
st.set_page_config(page_title="Lecture AI", layout="wide")
st.title("Lecture AI")
st.caption("Turn a lecture into a transcript, summary, key concepts and a quiz.")


def call(path: str, transcript: str):
    r = requests.post(f"{BACKEND}{path}", json={"transcript": transcript}, timeout=180)
    r.raise_for_status()
    return r.json()


up = st.file_uploader("Upload a lecture (MP4, MP3, WAV, max 15 min)", type=["mp4", "mp3", "wav", "m4a"])
if up and st.button("Upload"):
    r = requests.post(f"{BACKEND}/upload", files={"file": (up.name, up.getvalue())}, timeout=300)
    if r.ok:
        st.success(f"Uploaded ({r.json()['duration_sec']} s). Transcription arrives on Day 2.")
    else:
        st.error(r.json().get("detail", "Upload failed"))

st.subheader("Or paste a transcript (Day 1 testing)")
transcript = st.text_area("Transcript", height=180)

if transcript and st.button("Generate study material"):
    t_sum, t_con, t_quiz = st.tabs(["Summary", "Key concepts", "Quiz"])
    try:
        with t_sum:
            with st.spinner("Summarising..."):
                st.markdown(call("/summary", transcript)["summary"])
        with t_con:
            for c in call("/concepts", transcript)["concepts"]:
                st.markdown(f"**{c['term']}** ({c['timestamp']}): {c['definition']}")
        with t_quiz:
            for i, q in enumerate(call("/quiz", transcript)["questions"], 1):
                st.markdown(f"**Q{i}. {q['question']}** _({q['difficulty']})_")
                for j, o in enumerate(q["options"]):
                    st.write(f"{'ABCD'[j]}. {o}")
                with st.expander("Answer"):
                    st.write(f"{'ABCD'[q['answer_index']]}: {q['explanation']} ({q['timestamp']})")
    except Exception as e:
        st.error(f"Something went wrong: {e}")
