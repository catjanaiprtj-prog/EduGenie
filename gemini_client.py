import json
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from google import genai
except ImportError:
    genai = None


_client = None


def get_client():
    global _client

    if _client is not None:
        return _client

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    if genai is None:
        raise RuntimeError(
            "Google GenAI package is not installed."
        )

    _client = genai.Client(api_key=api_key)
    return _client


def generate_text(prompt: str) -> str:
    client = get_client()

    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    if not response or not response.text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return response.text.strip()


def generate_structured(prompt: str, schema=None) -> str:
    try:
        client = get_client()

        model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

        response = client.models.generate_content(
            model=model,
            contents=prompt
        )

        if not response or not response.text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        text = response.text.strip()

        if text.startswith("```json"):
            text = text[len("```json"):].strip()

        elif text.startswith("```"):
            text = text[len("```"):].strip()

        if text.endswith("```"):
            text = text[:-3].strip()

        json.loads(text)
        return text

    except Exception as exc:
        print("Gemini structured response error:", exc)
        return demo_structured_response(prompt)


def demo_structured_response(prompt: str) -> str:
    """
    Fallback structured response when Gemini is unavailable.
    Generates a quiz based on the requested topic.
    """

    import json
    import re

    # Get topic from the prompt
    topic = "General Programming"

    topic_match = re.search(
        r"Topic:\s*(.+?)(?:\n|$)",
        prompt,
        re.IGNORECASE
    )

    if topic_match:
        topic = topic_match.group(1).strip()

    if not topic:
        topic = "General Programming"

    topic_lower = topic.lower()

    # =========================================================
    # JAVA
    # =========================================================
    if "java" in topic_lower and "javascript" not in topic_lower:

        questions = [
            {
                "question": "Which keyword is used to define a class in Java?",
                "options": [
                    "class",
                    "struct",
                    "define",
                    "object"
                ],
                "answer": "class",
                "explanation": "The class keyword is used to define a class in Java."
            },
            {
                "question": "Which method is the entry point of a Java application?",
                "options": [
                    "start()",
                    "main()",
                    "run()",
                    "execute()"
                ],
                "answer": "main()",
                "explanation": "The main() method is the usual entry point of a Java application."
            },
            {
                "question": "Which symbol ends most Java statements?",
                "options": [
                    ".",
                    ";",
                    ":",
                    ","
                ],
                "answer": ";",
                "explanation": "Most Java statements end with a semicolon."
            },
            {
                "question": "Which keyword is used to create an object in Java?",
                "options": [
                    "new",
                    "create",
                    "object",
                    "make"
                ],
                "answer": "new",
                "explanation": "The new keyword is used to create an object."
            },
            {
                "question": "Which Java data type stores true or false?",
                "options": [
                    "boolean",
                    "bool",
                    "bit",
                    "logical"
                ],
                "answer": "boolean",
                "explanation": "boolean stores true or false values in Java."
            }
        ]

    # =========================================================
    # JAVASCRIPT
    # =========================================================
    elif "javascript" in topic_lower:

        questions = [
            {
                "question": "Which keyword can be used to declare a variable in JavaScript?",
                "options": [
                    "let",
                    "define",
                    "variable",
                    "declare"
                ],
                "answer": "let",
                "explanation": "let is used to declare a block-scoped variable."
            },
            {
                "question": "Which symbol starts a single-line comment in JavaScript?",
                "options": [
                    "//",
                    "#",
                    "<!--",
                    "**"
                ],
                "answer": "//",
                "explanation": "// starts a single-line comment in JavaScript."
            },
            {
                "question": "Which method prints output to the browser console?",
                "options": [
                    "console.log()",
                    "print()",
                    "echo()",
                    "display()"
                ],
                "answer": "console.log()",
                "explanation": "console.log() is commonly used to print messages to the console."
            },
            {
                "question": "Which keyword declares a constant in JavaScript?",
                "options": [
                    "const",
                    "constant",
                    "fixed",
                    "static"
                ],
                "answer": "const",
                "explanation": "const declares a variable that cannot be reassigned."
            },
            {
                "question": "Which file extension is commonly used for JavaScript?",
                "options": [
                    ".js",
                    ".java",
                    ".script",
                    ".javascript"
                ],
                "answer": ".js",
                "explanation": "JavaScript source files commonly use the .js extension."
            }
        ]

    # =========================================================
    # C++
    # =========================================================
    elif "c++" in topic_lower or "cpp" in topic_lower:

        questions = [
            {
                "question": "Which function is the usual entry point of a C++ program?",
                "options": [
                    "start()",
                    "main()",
                    "run()",
                    "begin()"
                ],
                "answer": "main()",
                "explanation": "A standard C++ program normally begins execution from main()."
            },
            {
                "question": "Which symbol ends most C++ statements?",
                "options": [
                    ";",
                    ".",
                    ":",
                    ","
                ],
                "answer": ";",
                "explanation": "Most C++ statements end with a semicolon."
            },
            {
                "question": "Which header provides standard input and output streams in C++?",
                "options": [
                    "<iostream>",
                    "<stdio>",
                    "<input>",
                    "<stream>"
                ],
                "answer": "<iostream>",
                "explanation": "<iostream> provides C++ input and output stream functionality."
            },
            {
                "question": "Which operator is used with cout to output data?",
                "options": [
                    ">>",
                    "<<",
                    "==",
                    "&&"
                ],
                "answer": "<<",
                "explanation": "The << operator inserts data into an output stream such as cout."
            },
            {
                "question": "Which keyword is used to define a class in C++?",
                "options": [
                    "class",
                    "object",
                    "define",
                    "type"
                ],
                "answer": "class",
                "explanation": "The class keyword is used to define a class."
            }
        ]

    # =========================================================
    # C
    # =========================================================
    elif topic_lower == "c" or "c programming" in topic_lower:

        questions = [
            {
                "question": "Which function is the usual entry point of a C program?",
                "options": [
                    "start()",
                    "main()",
                    "run()",
                    "begin()"
                ],
                "answer": "main()",
                "explanation": "Execution of a C program normally begins with main()."
            },
            {
                "question": "Which symbol ends most C statements?",
                "options": [
                    ";",
                    ".",
                    ":",
                    ","
                ],
                "answer": ";",
                "explanation": "Most C statements end with a semicolon."
            },
            {
                "question": "Which function is commonly used to print output in C?",
                "options": [
                    "printf()",
                    "print()",
                    "console.log()",
                    "display()"
                ],
                "answer": "printf()",
                "explanation": "printf() is commonly used for formatted output in C."
            },
            {
                "question": "Which header is commonly used with printf()?",
                "options": [
                    "<stdio.h>",
                    "<iostream>",
                    "<string>",
                    "<output.h>"
                ],
                "answer": "<stdio.h>",
                "explanation": "<stdio.h> declares standard input and output functions."
            },
            {
                "question": "Which operator gets the address of a variable in C?",
                "options": [
                    "&",
                    "*",
                    "#",
                    "%"
                ],
                "answer": "&",
                "explanation": "The & operator is the address-of operator."
            }
        ]

    # =========================================================
    # PYTHON
    # =========================================================
    elif "python" in topic_lower:

        questions = [
            {
                "question": "Which keyword is used to define a function in Python?",
                "options": [
                    "def",
                    "function",
                    "func",
                    "define"
                ],
                "answer": "def",
                "explanation": "The def keyword is used to define a function."
            },
            {
                "question": "Which symbol starts a single-line comment in Python?",
                "options": [
                    "#",
                    "//",
                    "--",
                    "/*"
                ],
                "answer": "#",
                "explanation": "Python uses # for single-line comments."
            },
            {
                "question": "Which function displays output in Python?",
                "options": [
                    "print()",
                    "display()",
                    "echo()",
                    "show()"
                ],
                "answer": "print()",
                "explanation": "The print() function displays output."
            },
            {
                "question": "Which of these is a Boolean value in Python?",
                "options": [
                    "True",
                    "TRUE_VALUE",
                    "Yes",
                    "Boolean"
                ],
                "answer": "True",
                "explanation": "True and False are Python Boolean values."
            },
            {
                "question": "Which extension is commonly used for Python files?",
                "options": [
                    ".py",
                    ".python",
                    ".pt",
                    ".p"
                ],
                "answer": ".py",
                "explanation": "Python source files commonly use the .py extension."
            }
        ]

    # =========================================================
    # HTML
    # =========================================================
    elif "html" in topic_lower:

        questions = [
            {
                "question": "What does HTML stand for?",
                "options": [
                    "HyperText Markup Language",
                    "HighText Machine Language",
                    "Hyperlink Text Management Language",
                    "Home Tool Markup Language"
                ],
                "answer": "HyperText Markup Language",
                "explanation": "HTML stands for HyperText Markup Language."
            },
            {
                "question": "Which tag creates the largest heading in HTML?",
                "options": [
                    "<h1>",
                    "<h6>",
                    "<heading>",
                    "<head>"
                ],
                "answer": "<h1>",
                "explanation": "<h1> represents the highest-level heading."
            },
            {
                "question": "Which HTML tag creates a hyperlink?",
                "options": [
                    "<a>",
                    "<link>",
                    "<href>",
                    "<url>"
                ],
                "answer": "<a>",
                "explanation": "The <a> tag is used to create hyperlinks."
            },
            {
                "question": "Which HTML tag displays an image?",
                "options": [
                    "<img>",
                    "<image>",
                    "<picture>",
                    "<src>"
                ],
                "answer": "<img>",
                "explanation": "The <img> element embeds an image."
            },
            {
                "question": "Which declaration specifies HTML5?",
                "options": [
                    "<!DOCTYPE html>",
                    "<HTML5>",
                    "<DOCTYPE HTML5>",
                    "<html5>"
                ],
                "answer": "<!DOCTYPE html>",
                "explanation": "<!DOCTYPE html> declares an HTML5 document."
            }
        ]

    # =========================================================
    # SQL
    # =========================================================
    elif "sql" in topic_lower:

        questions = [
            {
                "question": "Which SQL command retrieves data from a table?",
                "options": [
                    "SELECT",
                    "GET",
                    "FETCH",
                    "READ"
                ],
                "answer": "SELECT",
                "explanation": "SELECT is used to retrieve data from a database."
            },
            {
                "question": "Which SQL command adds new rows?",
                "options": [
                    "INSERT",
                    "ADD",
                    "CREATE",
                    "APPEND"
                ],
                "answer": "INSERT",
                "explanation": "INSERT adds new rows to a table."
            },
            {
                "question": "Which clause filters rows?",
                "options": [
                    "WHERE",
                    "FILTER",
                    "CHECK",
                    "HAVINGONLY"
                ],
                "answer": "WHERE",
                "explanation": "WHERE filters rows according to a condition."
            },
            {
                "question": "Which command modifies existing rows?",
                "options": [
                    "UPDATE",
                    "CHANGE",
                    "MODIFY",
                    "EDIT"
                ],
                "answer": "UPDATE",
                "explanation": "UPDATE modifies existing records."
            },
            {
                "question": "Which command removes rows from a table?",
                "options": [
                    "DELETE",
                    "REMOVE",
                    "CLEAR",
                    "ERASE"
                ],
                "answer": "DELETE",
                "explanation": "DELETE removes rows from a table."
            }
        ]

    # =========================================================
    # AI / ARTIFICIAL INTELLIGENCE
    # =========================================================
    elif (
        topic_lower == "ai"
        or "artificial intelligence" in topic_lower
        or "machine learning" in topic_lower
    ):

        questions = [
            {
                "question": "What is a primary goal of Artificial Intelligence?",
                "options": [
                    "Enable machines to perform tasks requiring human-like intelligence",
                    "Only store files",
                    "Only increase internet speed",
                    "Only design hardware"
                ],
                "answer": "Enable machines to perform tasks requiring human-like intelligence",
                "explanation": "AI focuses on systems performing tasks associated with intelligent behavior."
            },
            {
                "question": "Which field is a major area of Artificial Intelligence?",
                "options": [
                    "Machine Learning",
                    "Word Processing",
                    "Disk Formatting",
                    "File Compression"
                ],
                "answer": "Machine Learning",
                "explanation": "Machine Learning is a major area of AI."
            },
            {
                "question": "What does a machine learning model learn from?",
                "options": [
                    "Data",
                    "Only electricity",
                    "Only screen pixels",
                    "Only keyboard input"
                ],
                "answer": "Data",
                "explanation": "Machine learning models learn patterns from data."
            },
            {
                "question": "Which field focuses on understanding human language?",
                "options": [
                    "Natural Language Processing",
                    "Disk Partitioning",
                    "File Compression",
                    "Hardware Design"
                ],
                "answer": "Natural Language Processing",
                "explanation": "Natural Language Processing deals with human language."
            },
            {
                "question": "What is model training in machine learning?",
                "options": [
                    "Learning patterns from data",
                    "Deleting data",
                    "Formatting a disk",
                    "Installing an operating system"
                ],
                "answer": "Learning patterns from data",
                "explanation": "Training allows a model to learn patterns from data."
            }
        ]

    # =========================================================
    # GENERIC TOPIC
    # =========================================================
    else:

        questions = [
            {
                "question": f"What is an important part of learning {topic}?",
                "options": [
                    f"Understanding the concepts of {topic}",
                    "Ignoring the subject",
                    "Avoiding practice",
                    "Deleting learning materials"
                ],
                "answer": f"Understanding the concepts of {topic}",
                "explanation": f"Understanding the concepts is important when learning {topic}."
            },
            {
                "question": f"Which activity can improve knowledge of {topic}?",
                "options": [
                    f"Practicing {topic}",
                    "Avoiding examples",
                    "Skipping concepts",
                    "Ignoring feedback"
                ],
                "answer": f"Practicing {topic}",
                "explanation": f"Practice helps improve knowledge of {topic}."
            },
            {
                "question": f"What can help a learner understand {topic} better?",
                "options": [
                    "Examples and practice",
                    "No practice",
                    "Skipping explanations",
                    "Avoiding questions"
                ],
                "answer": "Examples and practice",
                "explanation": "Examples and practice help learners understand a subject."
            },
            {
                "question": f"Which approach is useful when studying {topic}?",
                "options": [
                    "Learn concepts and apply them",
                    "Memorize without understanding",
                    "Avoid practical work",
                    "Skip the basics"
                ],
                "answer": "Learn concepts and apply them",
                "explanation": "Learning concepts and applying them helps develop understanding."
            },
            {
                "question": f"Why can quizzes be useful when learning {topic}?",
                "options": [
                    "They check understanding",
                    "They remove the need to study",
                    "They prevent practice",
                    "They replace every explanation"
                ],
                "answer": "They check understanding",
                "explanation": "Quizzes can help check understanding."
            }
        ]

    # =========================================================
    # FINAL JSON RESPONSE
    # =========================================================
    return json.dumps({
        "title": f"{topic} Practice Quiz",
        "questions": questions
    })