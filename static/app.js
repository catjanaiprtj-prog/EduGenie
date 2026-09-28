// ================================================
// SECTION NAVIGATION
// ================================================

function showSection(sectionId) {

    const sections = document.querySelectorAll(".tool-section");

    sections.forEach(section => {
        section.classList.remove("active");
    });

    const selected = document.getElementById(sectionId);

    if (selected) {
        selected.classList.add("active");

        selected.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    }
}


// ================================================
// GET SELECTED LANGUAGE
// ================================================

function getLanguage() {

    return document.getElementById("language").value;
}


function getDifficulty() {

    return document.getElementById("difficulty").value;
}


// ================================================
// ASK QUESTION
// ================================================

async function askQuestion() {

    const questionElement =
        document.getElementById("question");

    const result =
        document.getElementById("qaResult");

    const question =
        questionElement.value.trim();

    if (!question) {

        result.classList.add("show");

        result.innerHTML =
            "⚠️ Please enter a question.";

        return;
    }

    const language = getLanguage();

    const difficulty = getDifficulty();

    result.classList.add("show");

    result.innerHTML =
        "⏳ EduGenie is preparing your answer...";

    try {

        const response = await fetch("/qa", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                language: language,

                difficulty: difficulty,

                question: question

            })

        });

        const data = await response.json();

        if (!response.ok || !data.success) {

            throw new Error(
                data.detail || "Unable to get answer."
            );
        }

        result.innerHTML =
            formatAnswer(data.answer);

    } catch (error) {

        result.innerHTML =
            "❌ Error: " + error.message;
    }
}


// ================================================
// EXPLAIN TOPIC
// ================================================

async function explainTopic() {

    const topic =
        document.getElementById("topic")
            .value.trim();

    const result =
        document.getElementById("explainResult");

    if (!topic) {

        result.classList.add("show");

        result.innerHTML =
            "⚠️ Please enter a topic.";

        return;
    }

    result.classList.add("show");

    result.innerHTML =
        "⏳ Preparing explanation...";

    try {

        const response = await fetch("/explain", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                language: getLanguage(),

                difficulty: getDifficulty(),

                topic: topic

            })

        });

        const data = await response.json();

        if (!response.ok || !data.success) {

            throw new Error(
                data.detail || "Unable to explain topic."
            );
        }

        result.innerHTML =
            formatAnswer(data.answer);

    } catch (error) {

        result.innerHTML =
            "❌ Error: " + error.message;
    }
}


// ================================================
// GENERATE QUIZ
// ================================================

async function generateQuiz() {

    const topic =
        document.getElementById("quizTopic")
            .value.trim();

    const result =
        document.getElementById("quizResult");

    if (!topic) {

        result.classList.add("show");

        result.innerHTML =
            "⚠️ Please enter a quiz topic.";

        return;
    }

    result.classList.add("show");

    result.innerHTML =
        "⏳ Generating quiz...";

    try {

        const response = await fetch("/quiz", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                language: getLanguage(),

                difficulty: getDifficulty(),

                topic: topic

            })

        });

        const data = await response.json();

        if (!response.ok || !data.success) {

            throw new Error(
                data.detail || "Unable to generate quiz."
            );
        }

        renderQuiz(data.questions);

    } catch (error) {

        result.innerHTML =
            "❌ Error: " + error.message;
    }
}


// ================================================
// RENDER QUIZ
// ================================================

function renderQuiz(questions) {

    const result =
        document.getElementById("quizResult");

    let html =
        "<h3>🧠 Your Quiz</h3>";

    questions.forEach((item, index) => {

        html += `
            <div style="
                margin-top:20px;
                padding:18px;
                border-radius:14px;
                background:rgba(255,255,255,0.04);
            ">

                <strong>
                    ${index + 1}. ${item.question}
                </strong>

                <div style="
                    margin-top:12px;
                    display:grid;
                    gap:8px;
                ">

                    ${item.options.map(
                        (option, optionIndex) => `
                            <label style="
                                padding:10px;
                                border-radius:10px;
                                background:rgba(255,255,255,0.05);
                                cursor:pointer;
                            ">

                                <input
                                    type="radio"
                                    name="quiz-${index}"
                                    value="${optionIndex}"
                                >

                                ${option}

                            </label>
                        `
                    ).join("")}

                </div>

            </div>
        `;

    });

    html += `
        <button
            class="primary-button"
            style="margin-top:20px"
            onclick="checkQuiz(${JSON.stringify(questions).replace(/"/g, '&quot;')})">

            ✅ Submit Quiz

        </button>

        <div
            id="quizScore"
            style="margin-top:20px">
        </div>
    `;

    result.innerHTML = html;
}


// ================================================
// CHECK QUIZ
// ================================================

function checkQuiz(questions) {

    let score = 0;

    questions.forEach((question, index) => {

        const selected =
            document.querySelector(
                `input[name="quiz-${index}"]:checked`
            );

        if (
            selected &&
            Number(selected.value) === question.answer
        ) {

            score++;
        }

    });

    const scoreBox =
        document.getElementById("quizScore");

    scoreBox.innerHTML = `
        <div style="
            padding:20px;
            border-radius:15px;
            background:rgba(34,197,94,0.1);
            border:1px solid rgba(34,197,94,0.2);
        ">

            🎉 <strong>Quiz Completed!</strong>

            <br><br>

            Your Score:
            <strong>${score} / ${questions.length}</strong>

        </div>
    `;
}


// ================================================
// SUMMARIZE
// ================================================

function summarizeText() {

    const text =
        document.getElementById("summaryText")
            .value.trim();

    const result =
        document.getElementById("summaryResult");

    result.classList.add("show");

    if (!text) {

        result.innerHTML =
            "⚠️ Please enter some text.";

        return;
    }

    const sentences =
        text
            .split(/[.!?]+/)
            .map(item => item.trim())
            .filter(item => item.length > 0);

    const summary =
        sentences.slice(0, 3).join(". ") + ".";

    result.innerHTML = `
        <h3>📝 Summary</h3>

        <br>

        ${summary}
    `;
}


// ================================================
// FORMAT ANSWER
// ================================================

function formatAnswer(text) {

    let html = text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");

    html = html.replace(
        /```(\w+)?\n([\s\S]*?)```/g,
        function(match, language, code) {

            return `
                <pre style="
                    margin:15px 0;
                    padding:18px;
                    border-radius:14px;
                    overflow-x:auto;
                    background:#020617;
                    border:1px solid rgba(255,255,255,0.1);
                "><code>${code}</code></pre>
            `;
        }
    );

    html = html
        .replace(/^### (.*)$/gm, "<h3>$1</h3>")
        .replace(/^## (.*)$/gm, "<h2>$1</h2>")
        .replace(/^# (.*)$/gm, "<h2>$1</h2>")
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/\n/g, "<br>");

    return html;
}