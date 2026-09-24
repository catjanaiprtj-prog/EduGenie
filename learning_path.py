import json

from gemini_client import generate_structured


def generate_learning_path(
    topic: str,
    weeks: int = 4,
    level: str = "beginner"
):

    prompt = f"""
Create a personalized learning path.

Topic:
{topic}

Level:
{level}

Duration:
{weeks} weeks

Return valid JSON only.

Each week must contain:

week
topic
goals
activities
resource_types
"""

    try:

        json_text = generate_structured(
            prompt,
            None
        )

        data = json.loads(
            json_text
        )

        return data

    except Exception as exc:

        print(
            "Learning path error:",
            exc
        )

        fallback_weeks = []

        topics = [
            "Fundamentals",
            "Core Concepts",
            "Practical Application",
            "Revision and Project"
        ]

        for index in range(weeks):

            topic_name = topics[
                index % len(topics)
            ]

            fallback_weeks.append({

                "week": index + 1,

                "topic":
                    f"{topic} - {topic_name}",

                "goals": [
                    "Understand the important concepts",
                    "Practice what you learned"
                ],

                "activities": [
                    "Study the topic",
                    "Complete practice exercises"
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
                f"A {weeks}-week learning plan for {level} level.",

            "weeks":
                fallback_weeks

        }