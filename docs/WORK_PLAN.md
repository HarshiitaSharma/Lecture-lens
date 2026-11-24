# Work plan (lean version)

Priorities: **Must** = needed for marks; **Should** = improves quality; **Skip** = not worth the time.
Time estimates are for one person.

## Harshita (pipeline, backend, deployment)
| Priority | Task | Where | Time |
|---|---|---|---|
| Done | Whisper evaluation (tiny/base/small, GPU and CPU) | notebook 01 | - |
| Must | Run backend tests A, B, C and note the 10-minute transcription time | notebook 03 | 60 min |
| Must | Deploy to a Hugging Face Space and test a real upload on the live URL | notebook 03 (last cell) | 40 min + build |
| Must | Create the GitHub repo, upload files, add Diksha as collaborator, commit from your own account | github.com | 20 min |
| Must | Write the transcription part of the report (use the README table) | docs/REPORT_OUTLINE.md | 55 min |
| Should | Optional: add `small` to `CPU_MODELS` and re-run notebook 01 to see CPU speed | notebook 01 | 20 min |
| Should | Record the demo video (screen recording of a full run) | - | 50 min |

## Diksha (generation, frontend, evaluation)
| Priority | Task | Where | Time |
|---|---|---|---|
| Must | Add Gemini key to Colab Secrets, run notebook 02 Step A, write 3 reference summaries in your own words | notebook 02 | 60 min |
| Must | Run the summary experiment and score the blind rubric | notebook 02 | 45 min |
| Must | Run the quiz experiment, then the manual answerability check on 30 questions (or 15 if short on time) | notebook 02 | 45 min |
| Must | Write the summarisation and quiz parts of the report | docs/REPORT_OUTLINE.md | 60 min |
| Should | Test the live app end to end and note any UI problems | Space URL | 30 min |
| Skip | Topic-based chunking comparison if time is short (single-pass vs fixed is enough for two configurations) | - | - |

## Together
| Priority | Task |
|---|---|
| Must | Fill in README sections 6.2, 6.3, 6.4, the live URL and the team contributions |
| Must | Test the public URL on a fresh browser before submission |
| Must | Prepare 8-10 slides (outline in docs/REPORT_OUTLINE.md) |
| Must | Practise the viva: each of you explains the whole pipeline, then your own part |
| Should | Keep a cached example (transcript + results) ready in case the Gemini API or Space is slow during the demo |
| Skip | Chatbot, user accounts, extra export formats, long-lecture support |

## Order that avoids blockers
1. Harshita: notebook 03 tests. Diksha: notebook 02 Step A (reference summaries).
2. Harshita: deploy. Diksha: run notebook 02 experiments.
3. Both: scoring sheets, README results, report.
4. Both: slides, demo video, viva practice, final test of the public URL.

## Do not do
- Do not paste API keys into notebooks, the README or GitHub. Use Colab Secrets and Space secrets.
- Do not invent or round results; copy them from the notebook outputs.
- Do not use an AI to write your reference summaries or rubric scores, or the evaluation is meaningless.
