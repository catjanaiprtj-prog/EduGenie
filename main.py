from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


# =========================================================
# APP
# =========================================================

app = FastAPI(
    title="EduGenie",
    description="Programming Learning Assistant",
    version="1.0.0"
)


# =========================================================
# TEMPLATES
# =========================================================

templates = Jinja2Templates(directory="templates")


# =========================================================
# STATIC FILES
# =========================================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# =========================================================
# SUPPORTED PROGRAMMING LANGUAGES
# =========================================================

LANGUAGES = [
    "Python",
    "Java",
    "C",
    "C++",
    "JavaScript",
    "TypeScript",
    "HTML",
    "CSS",
    "SQL",
    "C#",
    "PHP",
    "Go",
    "Rust",
    "Kotlin",
    "Swift"
]


# =========================================================
# LANGUAGE DATA
# =========================================================

LANGUAGE_INFO = {

    "Python": {
        "extension": "python",
        "description": (
            "Python is a high-level, interpreted programming "
            "language known for its simple and readable syntax."
        ),
        "code": '''name = "EduGenie"

print("Hello,", name)

age = 20
print("Age:", age)'''
    },

    "Java": {
        "extension": "java",
        "description": (
            "Java is an object-oriented programming language "
            "used for applications, web systems and enterprise software."
        ),
        "code": '''public class Main {

    public static void main(String[] args) {

        String name = "EduGenie";

        System.out.println("Hello, " + name);
    }
}'''
    },

    "C": {
        "extension": "c",
        "description": (
            "C is a procedural programming language widely used "
            "for system programming and embedded systems."
        ),
        "code": '''#include <stdio.h>

int main() {

    char name[] = "EduGenie";

    printf("Hello, %s!", name);

    return 0;
}'''
    },

    "C++": {
        "extension": "cpp",
        "description": (
            "C++ is a powerful general-purpose programming language "
            "that supports object-oriented and generic programming."
        ),
        "code": '''#include <iostream>

using namespace std;

int main() {

    string name = "EduGenie";

    cout << "Hello, " << name << "!";

    return 0;
}'''
    },

    "JavaScript": {
        "extension": "javascript",
        "description": (
            "JavaScript is a programming language commonly used "
            "to create interactive and dynamic web applications."
        ),
        "code": '''const name = "EduGenie";

console.log("Hello, " + name);

let age = 20;

console.log("Age:", age);'''
    },

    "TypeScript": {
        "extension": "typescript",
        "description": (
            "TypeScript is a typed superset of JavaScript "
            "that provides static typing."
        ),
        "code": '''let name: string = "EduGenie";

let age: number = 20;

console.log("Hello, " + name);

console.log("Age:", age);'''
    },

    "HTML": {
        "extension": "html",
        "description": (
            "HTML is the standard markup language used "
            "to create and structure web pages."
        ),
        "code": '''<!DOCTYPE html>

<html>

<head>

    <title>EduGenie</title>

</head>

<body>

    <h1>Hello, EduGenie!</h1>

    <p>Welcome to programming.</p>

</body>

</html>'''
    },

    "CSS": {
        "extension": "css",
        "description": (
            "CSS is used to style HTML pages and control "
            "layout, colors, fonts and animations."
        ),
        "code": '''body {

    background: #111827;

    color: white;

    font-family: Arial, sans-serif;

}

h1 {

    text-align: center;

    font-size: 40px;

}'''
    },

    "SQL": {
        "extension": "sql",
        "description": (
            "SQL is used to store, retrieve, update and manage "
            "data in relational databases."
        ),
        "code": '''SELECT name, marks

FROM students

WHERE marks >= 50

ORDER BY marks DESC;'''
    },

    "C#": {
        "extension": "csharp",
        "description": (
            "C# is a modern object-oriented programming language "
            "developed by Microsoft."
        ),
        "code": '''using System;

class Program
{

    static void Main()
    {

        string name = "EduGenie";

        Console.WriteLine(
            "Hello, " + name
        );

    }

}'''
    },

    "PHP": {
        "extension": "php",
        "description": (
            "PHP is a server-side scripting language commonly "
            "used for web development."
        ),
        "code": '''<?php

$name = "EduGenie";

echo "Hello, " . $name;

?>'''
    },

    "Go": {
        "extension": "go",
        "description": (
            "Go is a compiled programming language designed "
            "for simplicity, concurrency and performance."
        ),
        "code": '''package main

import "fmt"

func main() {

    name := "EduGenie"

    fmt.Println("Hello,", name)
}'''
    },

    "Rust": {
        "extension": "rust",
        "description": (
            "Rust is a systems programming language focused "
            "on safety, speed and memory management."
        ),
        "code": '''fn main() {

    let name = "EduGenie";

    println!("Hello, {}!", name);

}'''
    },

    "Kotlin": {
        "extension": "kotlin",
        "description": (
            "Kotlin is a modern programming language commonly "
            "used for Android and JVM applications."
        ),
        "code": '''fun main() {

    val name = "EduGenie"

    println("Hello, $name")

}'''
    },

    "Swift": {
        "extension": "swift",
        "description": (
            "Swift is Apple's programming language used "
            "for iOS, macOS and other Apple platforms."
        ),
        "code": '''import Foundation

let name = "EduGenie"

print("Hello, \\(name)!")'''
    }
}


# =========================================================
# REQUEST MODELS
# =========================================================

class QARequest(BaseModel):
    language: str
    difficulty: str
    question: str


class ExplainRequest(BaseModel):
    language: str
    difficulty: str
    topic: str


class QuizRequest(BaseModel):
    language: str
    difficulty: str
    topic: str


# =========================================================
# HOME PAGE
# =========================================================

@app.get("/")
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "languages": LANGUAGES
        }
    )


# =========================================================
# GET LANGUAGES
# =========================================================

@app.get("/languages")
async def get_languages():

    return {
        "success": True,
        "languages": LANGUAGES
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
async def health():

    return {
        "success": True,
        "status": "EduGenie is running successfully"
    }


# =========================================================
# QUESTION & ANSWER
# =========================================================

@app.post("/qa")
async def question_answer(data: QARequest):

    language = data.language.strip()
    difficulty = data.difficulty.strip()
    question = data.question.strip()

    # Empty question
    if not question:

        return {
            "success": False,
            "detail": "Please enter a question."
        }

    # Unsupported language
    if language not in LANGUAGE_INFO:

        return {
            "success": False,
            "detail": (
                f"{language} is not currently supported."
            )
        }

    info = LANGUAGE_INFO[language]

    question_lower = question.lower()

    # -----------------------------------------------------
    # VARIABLE
    # -----------------------------------------------------

    if "variable" in question_lower:

        topic_answer = (
            f"### Variables in {language}\n\n"
            "A variable is used to store data in a program.\n\n"
            "Variables can store values such as numbers, "
            "text and other data.\n\n"
            f"In {language}, the exact syntax depends on "
            "the programming language."
        )

    # -----------------------------------------------------
    # LOOP
    # -----------------------------------------------------

    elif "loop" in question_lower:

        topic_answer = (
            f"### Loops in {language}\n\n"
            "A loop is used to execute a block of code "
            "repeatedly.\n\n"
            "Common loops include:\n\n"
            "- for loop\n"
            "- while loop\n"
            "- do-while loop where supported\n\n"
            "Loops are useful when the same operation "
            "needs to be performed multiple times."
        )

    # -----------------------------------------------------
    # FUNCTION
    # -----------------------------------------------------

    elif "function" in question_lower:

        topic_answer = (
            f"### Functions in {language}\n\n"
            "A function is a reusable block of code "
            "that performs a specific task.\n\n"
            "Functions help programmers:\n\n"
            "- Reuse code\n"
            "- Reduce duplication\n"
            "- Organize programs\n"
            "- Improve readability"
        )

    # -----------------------------------------------------
    # ARRAY / LIST
    # -----------------------------------------------------

    elif (
        "array" in question_lower
        or "list" in question_lower
    ):

        topic_answer = (
            f"### Arrays / Lists in {language}\n\n"
            "Arrays or list-like structures are used "
            "to store multiple values.\n\n"
            "For example, a collection can contain:\n\n"
            "- Value 1\n"
            "- Value 2\n"
            "- Value 3\n\n"
            "The exact syntax depends on the language."
        )

    # -----------------------------------------------------
    # CLASS / OBJECT
    # -----------------------------------------------------

    elif (
        "class" in question_lower
        or "object" in question_lower
    ):

        topic_answer = (
            f"### Classes and Objects in {language}\n\n"
            "A class defines the structure and behavior "
            "of objects.\n\n"
            "Object-oriented programming commonly uses:\n\n"
            "- Classes\n"
            "- Objects\n"
            "- Encapsulation\n"
            "- Inheritance\n"
            "- Polymorphism"
        )

    # -----------------------------------------------------
    # IF / CONDITION
    # -----------------------------------------------------

    elif (
        "condition" in question_lower
        or "if statement" in question_lower
        or question_lower.startswith("if ")
    ):

        topic_answer = (
            f"### Conditional Statements in {language}\n\n"
            "Conditional statements allow a program "
            "to make decisions.\n\n"
            "A program checks a condition and executes "
            "the appropriate block of code."
        )

    # -----------------------------------------------------
    # GENERAL QUESTION
    # -----------------------------------------------------

    else:

        topic_answer = (
            f"### Understanding Your Question\n\n"
            f"Your question is related to {language} "
            "programming.\n\n"
            "To solve the problem:\n\n"
            "1. Understand the requirement.\n"
            "2. Identify the input.\n"
            "3. Identify the expected output.\n"
            "4. Select the correct syntax.\n"
            "5. Write the programming logic.\n"
            "6. Test the program.\n"
            "7. Check the output."
        )

    # -----------------------------------------------------
    # CODE
    # -----------------------------------------------------

    code_block = (
        f"```{info['extension']}\n"
        f"{info['code']}\n"
        "```"
    )

    # -----------------------------------------------------
    # FINAL ANSWER
    # -----------------------------------------------------

    answer = (
        "# EduGenie Programming Answer\n\n"

        "## Programming Language\n"
        f"**{language}**\n\n"

        "## Difficulty\n"
        f"**{difficulty}**\n\n"

        "## Your Question\n"
        f"{question}\n\n"

        f"## About {language}\n\n"
        f"{info['description']}\n\n"

        f"{topic_answer}\n\n"

        "## Example Code\n\n"
        f"{code_block}\n\n"

        "## Important Points\n\n"
        f"- Use correct {language} syntax.\n"
        "- Understand the logic before writing code.\n"
        "- Use meaningful variable names.\n"
        "- Test the program with different inputs.\n"
        "- Check the output carefully.\n\n"

        "## Practice\n\n"
        f"Try modifying the example and practice {language}."
    )

    return {
        "success": True,
        "answer": answer,
        "language": language,
        "difficulty": difficulty,
        "question": question
    }


# =========================================================
# TOPIC EXPLANATION
# =========================================================

@app.post("/explain")
async def explain_topic(data: ExplainRequest):

    language = data.language.strip()
    difficulty = data.difficulty.strip()
    topic = data.topic.strip()

    if not topic:

        return {
            "success": False,
            "detail": "Please enter a topic."
        }

    if language not in LANGUAGE_INFO:

        return {
            "success": False,
            "detail": (
                f"{language} is not currently supported."
            )
        }

    info = LANGUAGE_INFO[language]

    explanation = (
        "# Topic Explanation\n\n"

        "## Topic\n"
        f"**{topic}**\n\n"

        "## Programming Language\n"
        f"**{language}**\n\n"

        "## Difficulty\n"
        f"**{difficulty}**\n\n"

        "## Simple Explanation\n\n"
        f"{topic} is an important programming concept "
        f"that can be learned using {language}.\n\n"

        "## How to Learn It\n\n"
        "1. Understand the definition.\n"
        "2. Learn the syntax.\n"
        "3. Study a simple example.\n"
        "4. Write your own program.\n"
        "5. Test different inputs.\n"
        "6. Debug errors.\n\n"

        f"## {language} Example\n\n"
        f"```{info['extension']}\n"
        f"{info['code']}\n"
        "```\n\n"

        "## Practice Task\n\n"
        f"Create a small {language} program using "
        f"**{topic}**."
    )

    return {
        "success": True,
        "answer": explanation,
        "topic": topic,
        "language": language,
        "difficulty": difficulty
    }


# =========================================================
# QUIZ GENERATOR
# =========================================================

@app.post("/quiz")
async def generate_quiz(data: QuizRequest):

    language = data.language.strip()
    difficulty = data.difficulty.strip()
    topic = data.topic.strip()

    if not topic:

        return {
            "success": False,
            "detail": "Please enter a topic."
        }

    if language not in LANGUAGE_INFO:

        return {
            "success": False,
            "detail": (
                f"{language} is not currently supported."
            )
        }

    questions = [

        {
            "question": (
                f"What is {topic} in {language}?"
            ),
            "options": [
                f"A programming concept used in {language}",
                "A computer virus",
                "A hardware component",
                "An operating system"
            ],
            "answer": 0
        },

        {
            "question": (
                "Which programming language is selected?"
            ),
            "options": [
                language,
                "HTML",
                "CSS",
                "SQL"
            ],
            "answer": 0
        },

        {
            "question": (
                f"What should you do first when learning {topic}?"
            ),
            "options": [
                "Understand the concept",
                "Delete the program",
                "Turn off the computer",
                "Skip the syntax"
            ],
            "answer": 0
        },

        {
            "question": (
                f"Why should you practice {topic}?"
            ),
            "options": [
                "To improve programming skills",
                "To damage the computer",
                "To remove source code",
                "None of these"
            ],
            "answer": 0
        },

        {
            "question": (
                f"What is important when writing {language} programs?"
            ),
            "options": [
                "Correct syntax and logic",
                "Only colors",
                "Only images",
                "None"
            ],
            "answer": 0
        }

    ]

    return {
        "success": True,
        "language": language,
        "difficulty": difficulty,
        "topic": topic,
        "questions": questions
    }


# =========================================================
# API INFORMATION
# =========================================================

@app.get("/api/info")
async def api_info():

    return {
        "success": True,
        "project": "EduGenie",
        "version": "1.0.0",
        "languages": LANGUAGES,
        "features": [
            "Question and Answer",
            "Topic Explanation",
            "Quiz Generator",
            "Difficulty Selection",
            "Multiple Programming Languages"
        ]
    }