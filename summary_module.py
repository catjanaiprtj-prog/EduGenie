from gemini_client import generate_text


def summarize_text(
    text: str,
    number_of_sentences: int = 5
) -> str:

    prompt = f"""
Summarize the following text in approximately
{number_of_sentences} sentences.

Text:

{text}

Requirements:

- Keep the important points.
- Remove unnecessary details.
- Use simple language.
- Do not invent information.
"""

    return generate_text(prompt)