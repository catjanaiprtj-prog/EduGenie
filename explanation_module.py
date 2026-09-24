from gemini_client import generate_text


def explain_topic(
    topic: str,
    level: str = "beginner"
) -> str:

    prompt = f"""
You are EduGenie, an educational tutor.

Explain this topic to a {level} student.

Topic:
{topic}

Requirements:

1. Start with a simple definition.
2. Explain the main idea.
3. Break difficult ideas into small steps.
4. Give an example.
5. End with a short recap.

Use clear student-friendly language.
"""

    return generate_text(prompt)