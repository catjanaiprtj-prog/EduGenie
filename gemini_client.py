import json

from google import genai
from google.genai import types
from google.genai.errors import ServerError

from config import GEMINI_API_KEY, GEMINI_MODEL


def get_client():

    if not GEMINI_API_KEY:
        return None

    return genai.Client(
        api_key=GEMINI_API_KEY
    )


def generate_text(
    prompt: str,
    temperature: float = 0.4
) -> str:

    client = get_client()

    if client is None:
        return demo_text_response(prompt)

    try:

        print("Gemini request started...")
        print("Model:", GEMINI_MODEL)

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=temperature
            )
        )

        if response.text:

            print("Gemini response received.")

            return response.text

        return demo_text_response(prompt)

    except ServerError as exc:

        print("Gemini Server Error:", exc)
        print("Using EduGenie demo response.")

        return demo_text_response(prompt)

    except Exception as exc:

        print("Gemini Error:", exc)
        print("Using EduGenie demo response.")

        return demo_text_response(prompt)


def generate_structured(
    prompt: str,
    response_schema=None
) -> str:

    client = get_client()

    if client is None:
        return demo_structured_response(prompt)

    try:

        print("Gemini structured request started...")
        print("Model:", GEMINI_MODEL)

        config_kwargs = {
            "temperature": 0.3,
            "response_mime_type": "application/json"
        }

        if response_schema is not None:

            config_kwargs["response_schema"] = (
                response_schema
            )

        response = client.models.generate_content(

            model=GEMINI_MODEL,

            contents=prompt,

            config=types.GenerateContentConfig(
                **config_kwargs
            )

        )

        if response.text:

            print("Gemini structured response received.")

            return response.text

        return demo_structured_response(prompt)

    except Exception as exc:

        print("Gemini Structured Error:", exc)
        print("Using EduGenie demo structured response.")

        return demo_structured_response(prompt)


def generate_json(prompt: str) -> str:

    return generate_structured(
        prompt,
        None
    )


def demo_text_response(prompt: str) -> str:

    prompt_lower = prompt.lower()

    if "python" in prompt_lower:

        return """
Python is a high-level programming language known for its
simple and readable syntax.

It is widely used for:

• Web development
• Data analysis
• Artificial Intelligence
• Machine Learning
• Automation

Example:

print("Hello World")

This Python program displays Hello World on the screen.

In simple words, Python helps us give instructions to a
computer using easy-to-understand code.
"""


    if "machine learning" in prompt_lower:

        return """
Machine Learning is a branch of Artificial Intelligence.

It allows computers to learn patterns from data and make
predictions or decisions without being explicitly programmed
for every situation.

Example:

An email system can learn from previous emails and identify
whether a new email is spam or not spam.

In simple words:

Data → Learning → Prediction
"""


    if "artificial intelligence" in prompt_lower:

        return """
Artificial Intelligence, or AI, is the field of creating
computer systems that can perform tasks that normally require
human intelligence.

Examples include:

• Understanding language
• Recognizing images
• Making predictions
• Answering questions
• Recommending content

Chatbots are one example of AI applications.
"""


    return """
EduGenie Demo Response

Your EduGenie application is working correctly.

Gemini AI is temporarily unavailable, so EduGenie is using
its safe demonstration mode.

You can still test the application features including:

• Question & Answer
• Topic Explanation
• Quiz Generation
• Text Summarization
• Learning Recommendations

Once Gemini becomes available, the application can use the
Gemini-generated response automatically.
"""


def demo_structured_response(prompt: str) -> str:

    prompt_lower = prompt.lower()


    # ==========================================
    # QUIZ
    # ==========================================

    if (
        "quiz" in prompt_lower
        or "multiple-choice" in prompt_lower
    ):

        return json.dumps({

            "title": "Python Practice Quiz",

            "questions": [

                {
                    "question": "What is Python?",

                    "options": [
                        "A programming language",
                        "A web browser",
                        "An operating system",
                        "A database"
                    ],

                    "answer":
                        "A programming language",

                    "explanation":
                        "Python is a popular high-level programming language."
                },

                {
                    "question":
                        "Which symbol starts a comment in Python?",

                    "options": [
                        "#",
                        "//",
                        "/* */",
                        "<!-- -->"
                    ],

                    "answer": "#",

                    "explanation":
                        "Python uses # for single-line comments."
                },

                {
                    "question":
                        "Which function displays output in Python?",

                    "options": [
                        "print()",
                        "display()",
                        "show()",
                        "output()"
                    ],

                    "answer": "print()",

                    "explanation":
                        "The print() function displays output."
                },

                {
                    "question":
                        "Which value represents a Boolean?",

                    "options": [
                        "True",
                        "Hello",
                        "25",
                        "[1, 2, 3]"
                    ],

                    "answer": "True",

                    "explanation":
                        "True and False are Boolean values."
                },

                {
                    "question":
                        "Which keyword defines a function in Python?",

                    "options": [
                        "def",
                        "function",
                        "fun",
                        "define"
                    ],

                    "answer": "def",

                    "explanation":
                        "The def keyword is used to define a function."
                }

            ]

        })


    # ==========================================
    # LEARNING PATH
    # ==========================================

    return json.dumps({

        "title": "Personalized Learning Path",

        "overview":
            "A simple step-by-step learning journey.",

        "weeks": [

            {
                "week": 1,
                "topic": "Fundamentals",
                "goals": [
                    "Understand the basic concepts",
                    "Learn important terminology"
                ],
                "activities": [
                    "Read beginner material",
                    "Practice basic examples"
                ],
                "resource_types": [
                    "textbook",
                    "video",
                    "practice"
                ]
            },

            {
                "week": 2,
                "topic": "Core Concepts",
                "goals": [
                    "Understand important concepts",
                    "Solve simple problems"
                ],
                "activities": [
                    "Practice examples",
                    "Complete exercises"
                ],
                "resource_types": [
                    "documentation",
                    "practice",
                    "quiz"
                ]
            },

            {
                "week": 3,
                "topic": "Practical Application",
                "goals": [
                    "Apply the concepts",
                    "Build a small project"
                ],
                "activities": [
                    "Create a mini project",
                    "Practice problem solving"
                ],
                "resource_types": [
                    "project",
                    "practice"
                ]
            },

            {
                "week": 4,
                "topic": "Revision and Project",
                "goals": [
                    "Review important concepts",
                    "Complete a final project"
                ],
                "activities": [
                    "Take a quiz",
                    "Build a final mini project"
                ],
                "resource_types": [
                    "quiz",
                    "project",
                    "article"
                ]
            }

        ]

    })