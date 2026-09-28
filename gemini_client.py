import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

_client = None

if API_KEY:
    try:
        _client = genai.Client(api_key=API_KEY)
    except Exception:
        _client = None


# ---------------------------------------------------------
# Programming language detection
# ---------------------------------------------------------
LANGUAGES = [
    "python",
    "java",
    "javascript",
    "typescript",
    "c++",
    "c#",
    "c",
    "go",
    "golang",
    "rust",
    "php",
    "kotlin",
    "swift",
    "sql",
    "html",
    "css",
    "dart",
    "ruby",
    "scala",
    "r programming",
    "matlab",
    "perl",
    "lua",
    "bash",
    "shell",
    "assembly",
]


def detect_language(text: str) -> str:
    text_lower = text.lower()

    for language in LANGUAGES:
        if language in text_lower:
            return language.title()

    return "Programming"


# ---------------------------------------------------------
# Gemini text generation
# ---------------------------------------------------------
def generate_text(prompt: str, temperature: float = 0.4) -> str:

    if _client:
        try:
            response = _client.models.generate_content(
                model=MODEL,
                contents=prompt,
            )

            if response and response.text:
                return response.text.strip()

        except Exception:
            pass

    return demo_text_response(prompt)


# ---------------------------------------------------------
# Beautiful fallback/demo response
# ---------------------------------------------------------
def demo_text_response(prompt: str) -> str:

    language = detect_language(prompt)

    prompt_lower = prompt.lower()

    # Explanation
    if "explain" in prompt_lower:
        return f"""
✨ {language} — Easy Explanation

📌 What is {language}?

{language} is a programming technology used to create software,
applications, websites, automation systems, or data solutions.

💡 Main Idea

A programmer writes instructions using the syntax of {language}.
The computer processes those instructions and produces the required
result.

🔹 Important concepts

• Variables
• Data types
• Operators
• Conditions
• Loops
• Functions
• Error handling
• Data structures

🧩 Simple Example

A basic program normally follows this flow:

Input → Processing → Output

🚀 Real-world Uses

{language} can be used in software development, automation,
web applications, data processing, and many other technical projects.

🎯 Quick Recap

Learn the syntax first, then practice variables, conditions,
loops, functions, and small projects.
"""

    # Summary
    if "summar" in prompt_lower:
        return f"""
📝 {language} Summary

• {language} is used for programming and software development.
• Programs are created using instructions and logical operations.
• Important concepts include variables, conditions, loops and functions.
• Regular coding practice helps improve programming skills.
• Small projects are useful for understanding real-world programming.
"""

    # Learning recommendations
    if "learning" in prompt_lower or "learning path" in prompt_lower:
        return f"""
🎓 {language} Learning Roadmap

Week 1 — Fundamentals
• Syntax
• Variables
• Data types
• Basic input/output

Week 2 — Core Programming
• Conditions
• Loops
• Functions
• Error handling

Week 3 — Data & Problem Solving
• Arrays / Lists
• Collections
• Algorithms
• Debugging

Week 4 — Project
• Build a mini project
• Test the application
• Fix errors
• Improve the project

🚀 Next Step

After completing the basics, move to frameworks, libraries,
APIs and real-world projects related to {language}.
"""

    # Default Q&A
    return f"""
✨ EduGenie Answer

Programming Language: {language}

📚 Answer

{language} is a programming technology used to solve problems
by giving the computer a sequence of logical instructions.

🔹 Core concepts

1. Variables
2. Data Types
3. Operators
4. Conditions
5. Loops
6. Functions
7. Data Structures

💡 Example

Most programming problems follow:

Input
   ↓
Processing
   ↓
Output

🎯 Learning Tip

Start with simple programs and gradually build small projects.
Practice is the best way to improve programming skills.
"""


# ---------------------------------------------------------
# Structured response
# Used by Quiz + Learning Path
# ---------------------------------------------------------
def generate_structured(prompt: str, response_schema=None):

    prompt_lower = prompt.lower()
    language = detect_language(prompt)

    # -----------------------------------------------------
    # LEARNING PATH
    # -----------------------------------------------------
    if (
        "learning path" in prompt_lower
        or "personalized educational" in prompt_lower
        or "learning recommendations" in prompt_lower
    ):

        data = {
            "title": f"{language} Learning Roadmap",
            "overview": (
                f"A structured 4-week learning plan for "
                f"learning {language} from fundamentals to a mini project."
            ),
            "weeks": [
                {
                    "week": 1,
                    "topic": f"{language} Fundamentals",
                    "goals": [
                        "Understand basic syntax",
                        "Learn variables and data types",
                    ],
                    "activities": [
                        "Study basic syntax",
                        "Write simple programs",
                        "Practice input and output",
                    ],
                    "resource_types": [
                        "documentation",
                        "practice",
                        "quiz",
                    ],
                },
                {
                    "week": 2,
                    "topic": "Control Flow and Functions",
                    "goals": [
                        "Understand conditions",
                        "Learn loops and functions",
                    ],
                    "activities": [
                        "Practice if/else",
                        "Write loop programs",
                        "Create reusable functions",
                    ],
                    "resource_types": [
                        "video",
                        "practice",
                        "documentation",
                    ],
                },
                {
                    "week": 3,
                    "topic": "Data Structures",
                    "goals": [
                        "Understand common data structures",
                        "Improve problem solving",
                    ],
                    "activities": [
                        "Practice arrays or lists",
                        "Work with collections",
                        "Solve coding problems",
                    ],
                    "resource_types": [
                        "practice",
                        "article",
                        "quiz",
                    ],
                },
                {
                    "week": 4,
                    "topic": f"{language} Mini Project",
                    "goals": [
                        "Apply programming concepts",
                        "Build a working project",
                    ],
                    "activities": [
                        "Choose a mini project",
                        "Implement the project",
                        "Test and debug the project",
                    ],
                    "resource_types": [
                        "project",
                        "practice",
                        "documentation",
                    ],
                },
            ],
        }

        return json.dumps(data)

    # -----------------------------------------------------
    # QUIZ
    # -----------------------------------------------------

    questions = [
        {
            "question": f"What is {language} mainly used for?",
            "options": [
                "Programming and software development",
                "Only drawing pictures",
                "Only playing music",
                "Only sending emails",
            ],
            "answer": "Programming and software development",
            "explanation": (
                f"{language} can be used to create programs "
                f"and solve computational problems."
            ),
        },
        {
            "question": f"Which is important when learning {language}?",
            "options": [
                "Understanding syntax and logic",
                "Only memorizing colors",
                "Avoiding practice",
                "Never testing code",
            ],
            "answer": "Understanding syntax and logic",
            "explanation": (
                "Programming requires both language syntax "
                "and logical problem solving."
            ),
        },
        {
            "question": f"What helps improve {language} programming skills?",
            "options": [
                "Building projects",
                "Never writing code",
                "Only reading theory",
                "Avoiding debugging",
            ],
            "answer": "Building projects",
            "explanation": (
                "Projects provide practical experience and "
                "help improve programming skills."
            ),
        },
    ]

    return json.dumps(
        {
            "title": f"{language} Programming Quiz",
            "questions": questions,
        }
    )