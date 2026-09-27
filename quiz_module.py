import json
from gemini_client import generate_structured


def generate_quiz(
    topic: str,
    number_of_questions: int = 5,
    level: str = "beginner"
):
    topic = topic.strip()

    prompt = f"""
Create an educational multiple-choice quiz.

IMPORTANT:
The quiz MUST be ONLY about the exact topic provided below.

EXACT USER TOPIC:
{topic}

STUDENT LEVEL:
{level}

NUMBER OF QUESTIONS:
{number_of_questions}

STRICT RULES:
1. Every question must be directly related to "{topic}".
2. Do NOT change the topic.
3. Do NOT replace the topic with Python.
4. Do NOT replace the topic with Java.
5. Do NOT replace the topic with AI.
6. If the topic is Java, create Java questions.
7. If the topic is Python, create Python questions.
8. If the topic is C, create C questions.
9. If the topic is C++, create C++ questions.
10. If the topic is JavaScript, create JavaScript questions.
11. If the topic is SQL, create SQL questions.
12. If the topic is HTML, create HTML questions.
13. If the topic is CSS, create CSS questions.
14. If the topic is AI, create Artificial Intelligence questions.
15. For any other programming language, create questions specifically about that language.
16. Never use unrelated programming languages.
17. Generate exactly {number_of_questions} questions.
18. Each question must have exactly 4 options.
19. The answer must exactly match one of the options.
20. Include a short explanation for every answer.

Return valid JSON only.

JSON format:

{{
    "title": "{topic} Practice Quiz",
    "questions": [
        {{
            "question": "Question here",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "answer": "Correct option",
            "explanation": "Short explanation"
        }}
    ]
}}
"""

    try:
        json_text = generate_structured(
            prompt,
            None
        )

        data = json.loads(json_text)

        questions = data.get("questions", [])

        if not questions:
            raise ValueError("No quiz questions returned.")

        valid_questions = []

        for question in questions[:number_of_questions]:

            options = question.get("options", [])
            answer = question.get("answer", "")

            if len(options) != 4:
                continue

            if answer not in options:
                continue

            valid_questions.append({
                "question": question.get(
                    "question",
                    "Question"
                ),
                "options": options,
                "answer": answer,
                "explanation": question.get(
                    "explanation",
                    ""
                )
            })

        if not valid_questions:
            raise ValueError(
                "Quiz response was invalid."
            )

        return {
            "title": data.get(
                "title",
                f"{topic.title()} Practice Quiz"
            ),
            "questions": valid_questions
        }

    except Exception as exc:

        print("Quiz error:", exc)

        # Do NOT return a Python quiz here.
        # Returning a Python fallback was causing
        # AI / Java / C++ topics to show Python questions.

        raise ValueError(
            f"Unable to generate a quiz for '{topic}'. "
            "Please try again."
        )