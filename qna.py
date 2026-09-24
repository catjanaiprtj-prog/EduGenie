from gemini_client import generate_text


def answer_question(
    question: str
) -> str:

    prompt = f"""
You are EduGenie, an educational AI tutor.

Answer the student's question clearly.

Question:
{question}

Instructions:

- Give a direct answer first.
- Explain the concept simply.
- Give an example when useful.
- Use student-friendly language.
- Avoid unnecessary technical words.
"""

    return generate_text(prompt)