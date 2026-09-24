import json

from gemini_client import generate_structured


def generate_quiz(
    topic: str,
    number_of_questions: int = 5,
    level: str = "beginner"
):

    prompt = f"""
Create an educational multiple-choice quiz.

Topic:
{topic}

Student level:
{level}

Number of questions:
{number_of_questions}

Return valid JSON only.

Each question must contain:

question
options
answer
explanation

Each question must have exactly four options.
The answer must match one of the options.
"""

    try:

        json_text = generate_structured(
            prompt,
            None
        )

        data = json.loads(
            json_text
        )

        questions = data.get(
            "questions",
            []
        )

        if not questions:

            raise ValueError(
                "No quiz questions returned."
            )


        # Make sure requested number exists

        questions = questions[
            :number_of_questions
        ]


        # Validate each question

        valid_questions = []

        for question in questions:

            options = question.get(
                "options",
                []
            )

            answer = question.get(
                "answer",
                ""
            )

            if len(options) != 4:
                continue

            if answer not in options:
                continue

            valid_questions.append({

                "question":
                    question.get(
                        "question",
                        "Question"
                    ),

                "options":
                    options,

                "answer":
                    answer,

                "explanation":
                    question.get(
                        "explanation",
                        ""
                    )

            })


        if not valid_questions:

            raise ValueError(
                "Quiz response was invalid."
            )


        return {

            "title":
                data.get(
                    "title",
                    f"{topic.title()} Quiz"
                ),

            "questions":
                valid_questions

        }


    except Exception as exc:

        print(
            "Quiz error:",
            exc
        )

        # Safe fallback

        fallback = [

            {
                "question":
                    "What is Python?",

                "options": [
                    "A programming language",
                    "A web browser",
                    "An operating system",
                    "A database"
                ],

                "answer":
                    "A programming language",

                "explanation":
                    "Python is a programming language."
            },

            {
                "question":
                    "Which symbol starts a Python comment?",

                "options": [
                    "#",
                    "//",
                    "/* */",
                    "<!-- -->"
                ],

                "answer":
                    "#",

                "explanation":
                    "Python uses # for comments."
            },

            {
                "question":
                    "Which function prints output?",

                "options": [
                    "print()",
                    "show()",
                    "display()",
                    "output()"
                ],

                "answer":
                    "print()",

                "explanation":
                    "print() displays output."
            },

            {
                "question":
                    "Which is a Boolean value?",

                "options": [
                    "True",
                    "Python",
                    "100",
                    "Hello"
                ],

                "answer":
                    "True",

                "explanation":
                    "True is a Boolean value."
            },

            {
                "question":
                    "Which keyword defines a function?",

                "options": [
                    "def",
                    "function",
                    "fun",
                    "define"
                ],

                "answer":
                    "def",

                "explanation":
                    "def is used to define functions."
            }

        ]

        return {

            "title":
                f"{topic.title()} - Practice Quiz",

            "questions":
                fallback[
                    :number_of_questions
                ]

        }