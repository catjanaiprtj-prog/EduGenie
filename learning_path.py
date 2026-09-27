import json

from gemini_client import generate_structured


def generate_learning_path(
    topic: str,
    weeks: int = 4,
    level: str = "beginner"
):

    prompt = f"""
Create a personalized learning path specifically for the requested topic.

IMPORTANT RULES:
1. The learning path MUST be about "{topic}".
2. Do NOT give a generic learning path.
3. Every week's topic, goals and activities must be directly related to "{topic}".
4. Use real concepts, skills and practical activities from "{topic}".
5. If the topic is C Programming, include C-specific concepts such as:
   variables, data types, printf, scanf, conditions, loops, functions,
   arrays, strings, pointers, structures and file handling.
6. If the topic is Python, use Python-specific concepts.
7. If the topic is Java, use Java-specific concepts.
8. If the topic is JavaScript, use JavaScript-specific concepts.
9. For AI or Artificial Intelligence, use AI-specific concepts.
10. Never replace the requested topic with another programming language.

Topic:
{topic}

Level:
{level}

Duration:
{weeks} weeks

Return valid JSON only.

Use exactly this structure:

{{
    "title": "Topic-specific learning path title",
    "overview": "Short overview specifically about the requested topic",
    "weeks": [
        {{
            "week": 1,
            "topic": "Topic-specific week topic",
            "goals": [
                "Topic-specific goal 1",
                "Topic-specific goal 2"
            ],
            "activities": [
                "Topic-specific activity 1",
                "Topic-specific activity 2"
            ],
            "resource_types": [
                "documentation",
                "video",
                "practice"
            ]
        }}
    ]
}}

Make every week specific to "{topic}".
"""

    try:

        json_text = generate_structured(
            prompt,
            None
        )

        data = json.loads(json_text)

        return data

    except Exception as exc:

        print(
            "Learning path error:",
            exc
        )

        # Topic-specific fallback
        topic_lower = topic.lower().strip()

        if "c++" in topic_lower or "cpp" in topic_lower:

            topics = [
                "C++ Fundamentals",
                "Object-Oriented Programming",
                "STL and Data Structures",
                "Projects and Advanced C++"
            ]

        elif topic_lower == "c" or "c programming" in topic_lower:

            topics = [
                "C Programming Fundamentals",
                "Control Statements and Functions",
                "Arrays, Strings and Pointers",
                "Structures, File Handling and Projects"
            ]

        elif "python" in topic_lower:

            topics = [
                "Python Fundamentals",
                "Conditions, Loops and Functions",
                "Lists, Dictionaries and Modules",
                "Projects and Advanced Python"
            ]

        elif "java" in topic_lower and "javascript" not in topic_lower:

            topics = [
                "Java Fundamentals",
                "Classes, Objects and Methods",
                "Inheritance and Polymorphism",
                "Collections and Java Projects"
            ]

        elif "javascript" in topic_lower:

            topics = [
                "JavaScript Fundamentals",
                "Functions, Arrays and Objects",
                "DOM and Events",
                "Modern JavaScript Projects"
            ]

        elif "html" in topic_lower:

            topics = [
                "HTML Fundamentals",
                "Forms and Semantic HTML",
                "Tables, Media and Links",
                "Building Complete Web Pages"
            ]

        elif "sql" in topic_lower:

            topics = [
                "SQL Fundamentals",
                "SELECT, WHERE and Filtering",
                "JOINs, GROUP BY and Aggregation",
                "Database Projects and Advanced SQL"
            ]

        elif (
            topic_lower == "ai"
            or "artificial intelligence" in topic_lower
            or "machine learning" in topic_lower
        ):

            topics = [
                "AI and Machine Learning Fundamentals",
                "Data and Machine Learning Concepts",
                "Model Training and Evaluation",
                "AI Projects and Applications"
            ]

        else:

            topics = [
                f"{topic} Fundamentals",
                f"{topic} Core Concepts",
                f"Practical {topic}",
                f"{topic} Projects and Advanced Topics"
            ]

        fallback_weeks = []

        for index in range(weeks):

            topic_name = topics[
                index % len(topics)
            ]

            fallback_weeks.append({

                "week": index + 1,

                "topic": topic_name,

                "goals": [
                    f"Understand {topic_name}",
                    f"Build practical knowledge in {topic}"
                ],

                "activities": [
                    f"Study {topic_name}",
                    f"Complete {topic}-based practice exercises"
                ],

                "resource_types": [
                    "documentation",
                    "video",
                    "practice"
                ]

            })

        return {

            "title":
                f"{topic.title()} Learning Path",

            "overview":
                f"A {weeks}-week {topic}-specific learning plan for {level} level.",

            "weeks":
                fallback_weeks

        }