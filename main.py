from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="EduGenie")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


LANGUAGES = {
    "Python": {
        "extension": ".py",
        "example": 'print("Hello World")',
        "description": "Python is a high-level, interpreted programming language known for simple syntax."
    },
    "Java": {
        "extension": ".java",
        "example": 'System.out.println("Hello World");',
        "description": "Java is an object-oriented programming language designed for portability."
    },
    "C": {
        "extension": ".c",
        "example": 'printf("Hello World");',
        "description": "C is a powerful procedural programming language commonly used for systems programming."
    },
    "C++": {
        "extension": ".cpp",
        "example": 'cout << "Hello World";',
        "description": "C++ is a general-purpose language that supports object-oriented and generic programming."
    },
    "JavaScript": {
        "extension": ".js",
        "example": 'console.log("Hello World");',
        "description": "JavaScript is widely used for interactive web applications."
    },
    "TypeScript": {
        "extension": ".ts",
        "example": 'console.log("Hello World");',
        "description": "TypeScript is a typed superset of JavaScript."
    },
    "HTML": {
        "extension": ".html",
        "example": '<h1>Hello World</h1>',
        "description": "HTML is the standard markup language used to structure web pages."
    },
    "CSS": {
        "extension": ".css",
        "example": 'body { color: blue; }',
        "description": "CSS is used to style and design web pages."
    },
    "SQL": {
        "extension": ".sql",
        "example": 'SELECT * FROM students;',
        "description": "SQL is used to manage and query relational databases."
    },
    "C#": {
        "extension": ".cs",
        "example": 'Console.WriteLine("Hello World");',
        "description": "C# is a modern object-oriented language developed for the .NET platform."
    },
    "PHP": {
        "extension": ".php",
        "example": 'echo "Hello World";',
        "description": "PHP is a server-side scripting language commonly used for web development."
    },
    "Go": {
        "extension": ".go",
        "example": 'fmt.Println("Hello World")',
        "description": "Go is a statically typed language designed for simplicity and efficient software."
    },
    "Rust": {
        "extension": ".rs",
        "example": 'println!("Hello World");',
        "description": "Rust focuses on performance, memory safety, and concurrency."
    },
    "Kotlin": {
        "extension": ".kt",
        "example": 'println("Hello World")',
        "description": "Kotlin is a modern language widely used for Android development."
    },
    "Swift": {
        "extension": ".swift",
        "example": 'print("Hello World")',
        "description": "Swift is a programming language developed by Apple for its platforms."
    }
}


class QuestionRequest(BaseModel):
    language: str
    question: str
    difficulty: str = "Beginner"


class ExplanationRequest(BaseModel):
    language: str
    topic: str
    difficulty: str = "Beginner"


class QuizRequest(BaseModel):
    language: str
    topic: str
    difficulty: str = "Beginner"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "languages": list(LANGUAGES.keys())
        }
    )


@app.get("/languages")
async def get_languages():
    return {
        "languages": list(LANGUAGES.keys())
    }


@app.post("/qa")
async def question_answer(data: QuestionRequest):

    language = data.language
    question = data.question

    if language not in LANGUAGES:
        language = "Python"

    info = LANGUAGES[language]

    answer = f"""
<b>{language}</b> is a programming language.

<b>Your Question:</b>
{question}

<b>About {language}:</b>
{info["description"]}

<b>Example:</b>
<pre><code>{info["example"]}</code></pre>

<b>Difficulty:</b> {data.difficulty}

<b>Learning Tip:</b>
Start with variables, data types, conditions, loops, functions,
and then move to object-oriented programming and projects.
"""

    return {
        "success": True,
        "language": language,
        "answer": answer
    }


@app.post("/explain")
async def explain_topic(data: ExplanationRequest):

    language = data.language
    topic = data.topic

    if language not in LANGUAGES:
        language = "Python"

    info = LANGUAGES[language]

    explanation = f"""
<h3>{topic}</h3>

<p>
<b>{topic}</b> is an important concept when learning
<b>{language}</b>.
</p>

<p>
For <b>{data.difficulty}</b> level learning, understand the concept
step-by-step and practice it with small programs.
</p>

<h4>Language Information</h4>

<p>{info["description"]}</p>

<h4>Example</h4>

<pre><code>{info["example"]}</code></pre>

<h4>Practice</h4>

<p>
Create a small program using <b>{topic}</b>, test it,
find errors, and improve the program.
</p>
"""

    return {
        "success": True,
        "language": language,
        "explanation": explanation
    }


@app.post("/quiz")
async def generate_quiz(data: QuizRequest):

    language = data.language
    topic = data.topic

    questions = [
        {
            "question": f"What is the main purpose of {topic} in {language}?",
            "options": [
                "To solve programming problems",
                "To shut down the computer",
                "To remove the operating system",
                "None of these"
            ],
            "answer": 0
        },
        {
            "question": f"Which concept is commonly used while learning {language}?",
            "options": [
                "Variables",
                "Loops",
                "Functions",
                "All of the above"
            ],
            "answer": 3
        },
        {
            "question": f"Which approach is useful for learning {language}?",
            "options": [
                "Only reading",
                "Only watching videos",
                "Writing and practicing programs",
                "Avoiding practice"
            ],
            "answer": 2
        }
    ]

    return {
        "success": True,
        "language": language,
        "topic": topic,
        "difficulty": data.difficulty,
        "questions": questions
    }


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "message": "EduGenie is running successfully"
    }