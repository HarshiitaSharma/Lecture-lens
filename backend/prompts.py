CHUNK_SUMMARY = """You are summarising one part of a lecture transcript. Lines start with [HH:MM:SS] timestamps.
Write 3-5 concise bullet points covering only what the speaker actually said. Do not add outside facts.
Begin with the timestamp range in the form (HH:MM:SS - HH:MM:SS).

TRANSCRIPT PART:
{chunk}
"""

COMBINE_SUMMARY = """Below are summaries of consecutive parts of one lecture.
Combine them into structured study notes in Markdown with: a 2-3 sentence overview, then
section headings (with timestamp ranges) and bullet points, then a short list of key takeaways.
Use only the content provided.

PART SUMMARIES:
{parts}
"""

SINGLE_PASS_SUMMARY = """Summarise the following lecture transcript into structured study notes in Markdown:
a 2-3 sentence overview, section headings with timestamp ranges, bullet points, and key takeaways.
Use only the transcript content.

TRANSCRIPT:
{transcript}
"""

CONCEPTS = """Extract the 6-10 most important concepts from this lecture transcript.
For each give: term, a one-sentence definition based on the transcript, and the timestamp (HH:MM:SS)
where it is first explained. Use only the transcript.

TRANSCRIPT:
{transcript}
"""

QUIZ = """Create {n} multiple-choice questions that test understanding of this lecture transcript.
Rules:
- Each question has exactly 4 options and exactly one correct option (answer_index is 0-3).
- Questions must be answerable from the transcript alone.
- Mix difficulty: easy, medium, hard.
- Give a one-sentence explanation referencing the lecture, and the timestamp of the relevant passage.

TRANSCRIPT:
{transcript}
"""
