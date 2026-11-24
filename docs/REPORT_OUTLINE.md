# Report, slides and viva outline

## A. Technical report (about 6-8 pages)
1. **Title page:** project title, team members with IDs, live URL, GitHub URL.
2. **Problem statement and users** (half page): why lecture revision is slow; who benefits; what the system outputs.
3. **Requirements:** upload validation, transcript, summary, concepts, quiz, deployment, free-tier constraints.
4. **System architecture:** insert `docs/architecture.png`; describe the five-step workflow (see README section 3).
5. **AI components and why they were chosen:**
   - Whisper (speech recognition): what it is, why a pretrained model, why faster-whisper on CPU.
   - Gemini (summary, concepts, quiz): why an LLM, why map-reduce chunking, why JSON-schema output.
   - Explain why this is more than an API wrapper: ASR pipeline, chunking, validation, evaluation.
6. **Data and licences:** MIT OCW lectures and transcripts (CC BY-NC-SA), model licences, privacy handling.
7. **Evaluation:**
   - 7.1 Whisper model comparison: methodology (PDF alignment), table, chart (`whisper_wer.png` from Drive), chosen model, error examples.
   - 7.2 Summarisation: single-pass vs chunked, ROUGE/BERTScore and human rubric.
   - 7.3 Quiz: JSON validity, structural validity, manual answerability.
   - 7.4 Backend tests: processing time for 10 minutes, error handling.
8. **Results discussion and error analysis:** which technical terms failed; where summaries missed or added things; failure cases.
9. **Limitations and responsible use:** see README section 7; hallucination, bias, privacy.
10. **Deployment:** Docker, Hugging Face Space, secrets handling.
11. **Team contributions and AI assistance disclosure.**
12. **Conclusion and future work:** longer lectures, topic navigation, retrieval-based chatbot, speaker labels, better quiz verification.

## B. Slides (8-10)
1. Title and team
2. Problem and users
3. Demo of the final product (screenshot of tabs)
4. Architecture diagram
5. Speech recognition: model choice and WER table
6. Summarisation approach and results
7. Quiz generation and validation results
8. Deployment and engineering (Docker, API, jobs, secrets)
9. Limitations and honest failure cases
10. Contributions, AI-assistant disclosure and what we learned

## C. Demo video (3-4 minutes) script
1. 15 s: problem and what the app does.
2. 30 s: upload a 2-3 minute lecture clip; show validation (try a wrong file type first).
3. 60 s: transcription progress, then the transcript tab.
4. 60 s: summary, key concepts and quiz tabs; reveal one quiz answer.
5. 20 s: download notes.
6. 20 s: mention the evaluation results and limitations.

## D. Viva preparation (each of you must be able to answer all of these)
**Whole system**
- Draw and explain the pipeline end to end.
- Why Whisper plus an LLM instead of sending the video to an LLM directly?
- Why is this not just an API wrapper?

**Speech recognition (Harshita should lead)**
- What is WER and how is it computed? (substitutions + deletions + insertions over reference words)
- What is RTF? Why did we measure CPU as well as GPU?
- Why did we pick `base` and not `small`?
- How did you get a reference transcript from a PDF with no timestamps? (ends-free alignment; the largest model is used only to locate the clip, then all models are scored against the same fixed text)
- What are int8 quantisation and VAD filtering?
- What limits does the PDF reference have?

**Generation and evaluation (Diksha should lead)**
- Why chunk the transcript? What is map-reduce summarisation?
- What do ROUGE and BERTScore measure and why are they weak here? Why did you add a human rubric, and why blind?
- How is JSON output enforced? What happens if it is invalid?
- How do you check that a quiz question is supported by the lecture? What are the limits of that check?
- What are the main failure cases you saw?

**Engineering**
- Why a background job with polling for transcription?
- How are API keys protected? What is stored on the server and for how long?
- What breaks if two users upload at once? (single worker, one transcription at a time; others wait)
- What would you improve next?

## E. Final submission checklist (from the guidelines)
- [ ] Title, team members, problem statement
- [ ] Public URL tested on a fresh browser
- [ ] GitHub repo with commits from both of you
- [ ] README: overview, features, stack, setup, deployment
- [ ] Architecture diagram and workflow description
- [ ] Dataset/model details, licences, preprocessing
- [ ] Evaluation methodology, examples, results, limitations
- [ ] Short technical report and slides
- [ ] Demo video
- [ ] Team contributions and AI-assistant disclosure
