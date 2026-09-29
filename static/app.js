// ================================================
// EduGenie AI - Frontend
// ================================================


function showSection(sectionId, button) {

    document
        .querySelectorAll(".content-section")
        .forEach(section => {
            section.classList.remove("active");
        });


    document
        .querySelectorAll(".nav-item")
        .forEach(item => {
            item.classList.remove("active");
        });


    const section =
        document.getElementById(sectionId);


    if (section) {
        section.classList.add("active");
    }


    if (button) {
        button.classList.add("active");
    }


    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}


// ================================================
// API
// ================================================

async function apiCall(url, data) {

    const response = await fetch(
        url,
        {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify(data)
        }
    );


    const contentType =
        response.headers.get(
            "content-type"
        ) || "";


    if (!contentType.includes("application/json")) {

        throw new Error(
            "AI service is temporarily unavailable."
        );
    }


    const result =
        await response.json();


    if (!response.ok) {

        throw new Error(
            result.detail ||
            "Please try again."
        );
    }


    return result;
}


// ================================================
// LOADING
// ================================================

function showLoading(element) {

    element.innerHTML = `

        <div class="loading-card">

            <div class="spinner"></div>

            <strong>
                EduGenie is thinking...
            </strong>

            <p>
                Creating your personalized answer ✨
            </p>

        </div>

    `;
}


// ================================================
// ANSWER
// ================================================

function showAnswer(element, answer) {

    const safeAnswer =
        escapeHTML(answer)
            .replace(/\n/g, "<br>");


    element.innerHTML = `

        <div class="answer-card">

            <div class="answer-header">

                <div class="ai-title">
                    ✨ EduGenie AI
                </div>

                <button
                    class="copy-button"
                    onclick="copyAnswer(this)"
                >
                    📋 Copy
                </button>

            </div>

            <div class="answer-text">
                ${safeAnswer}
            </div>

        </div>

    `;
}


// ================================================
// ERROR
// ================================================

function showError(element, message) {

    element.innerHTML = `

        <div class="error-card">
            ⚠️ ${escapeHTML(message)}
        </div>

    `;
}


// ================================================
// ESCAPE
// ================================================

function escapeHTML(text) {

    const div =
        document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}


// ================================================
// ASK QUESTION
// ================================================

async function askQuestion() {

    const question =
        document
            .getElementById("question")
            .value
            .trim();


    const difficulty =
        document
            .getElementById("qaDifficulty")
            .value;


    const result =
        document
            .getElementById("qaResult");


    if (!question) {

        showError(
            result,
            "Please type your question first."
        );

        return;
    }


    showLoading(result);


    try {

        const data =
            await apiCall(
                "/qa",
                {
                    question: question,
                    difficulty: difficulty
                }
            );


        showAnswer(
            result,
            data.answer
        );

    }

    catch (error) {

        showError(
            result,
            error.message
        );
    }
}


// ================================================
// QUICK QUESTION
// ================================================

function useQuestion(text) {

    const input =
        document.getElementById(
            "question"
        );


    input.value = text;

    input.focus();
}


// ================================================
// EXPLAIN
// ================================================

async function explainTopic() {

    const topic =
        document
            .getElementById("topic")
            .value
            .trim();


    const difficulty =
        document
            .getElementById("explainDifficulty")
            .value;


    const result =
        document
            .getElementById("explainResult");


    if (!topic) {

        showError(
            result,
            "Please enter a topic."
        );

        return;
    }


    showLoading(result);


    try {

        const data =
            await apiCall(
                "/explain",
                {
                    topic: topic,
                    difficulty: difficulty
                }
            );


        showAnswer(
            result,
            data.answer
        );

    }

    catch (error) {

        showError(
            result,
            error.message
        );
    }
}


// ================================================
// QUIZ
// ================================================

async function generateQuiz() {

    const topic =
        document
            .getElementById("quizTopic")
            .value
            .trim();


    const difficulty =
        document
            .getElementById("quizDifficulty")
            .value;


    const count =
        Number(
            document
                .getElementById("quizCount")
                .value
        );


    const result =
        document
            .getElementById("quizResult");


    if (!topic) {

        showError(
            result,
            "Please enter a quiz topic."
        );

        return;
    }


    showLoading(result);


    try {

        const data =
            await apiCall(
                "/quiz",
                {
                    topic: topic,
                    difficulty: difficulty,
                    number_of_questions: count
                }
            );


        showAnswer(
            result,
            data.answer
        );

    }

    catch (error) {

        showError(
            result,
            error.message
        );
    }
}


// ================================================
// SUMMARY
// ================================================

async function summarizeText() {

    const text =
        document
            .getElementById("summaryText")
            .value
            .trim();


    const result =
        document
            .getElementById("summaryResult");


    if (!text) {

        showError(
            result,
            "Please paste your study material first."
        );

        return;
    }


    showLoading(result);


    try {

        const data =
            await apiCall(
                "/summarize",
                {
                    text: text
                }
            );


        showAnswer(
            result,
            data.answer
        );

    }

    catch (error) {

        showError(
            result,
            error.message
        );
    }
}


// ================================================
// RECOMMENDATIONS
// ================================================

async function getRecommendations() {

    const topic =
        document
            .getElementById("recommendTopic")
            .value
            .trim();


    const difficulty =
        document
            .getElementById("recommendDifficulty")
            .value;


    const result =
        document
            .getElementById(
                "recommendResult"
            );


    if (!topic) {

        showError(
            result,
            "Please enter a learning topic."
        );

        return;
    }


    showLoading(result);


    try {

        const data =
            await apiCall(
                "/recommendations",
                {
                    topic: topic,
                    difficulty: difficulty
                }
            );


        showAnswer(
            result,
            data.answer
        );

    }

    catch (error) {

        showError(
            result,
            error.message
        );
    }
}


// ================================================
// COPY
// ================================================

async function copyAnswer(button) {

    const card =
        button.closest(
            ".answer-card"
        );


    const text =
        card
            .querySelector(
                ".answer-text"
            )
            .innerText;


    try {

        await navigator.clipboard
            .writeText(text);


        button.innerText =
            "✅ Copied";


        setTimeout(
            () => {
                button.innerText =
                    "📋 Copy";
            },
            1500
        );

    }

    catch {

        button.innerText =
            "Copy failed";
    }
}


// ================================================
// NEW SESSION
// ================================================

function newChat() {

    document
        .querySelectorAll(
            "textarea, input"
        )
        .forEach(element => {
            element.value = "";
        });


    document
        .querySelectorAll(
            ".result-area"
        )
        .forEach(element => {
            element.innerHTML = "";
        });


    const firstMenu =
        document.querySelector(
            ".nav-item"
        );


    showSection(
        "qa",
        firstMenu
    );
}


// ================================================
// CTRL + ENTER
// ================================================

document.addEventListener(
    "keydown",
    function(event) {

        if (
            event.ctrlKey &&
            event.key === "Enter"
        ) {

            const active =
                document.querySelector(
                    ".content-section.active"
                );


            if (
                active &&
                active.id === "qa"
            ) {

                askQuestion();
            }
        }

    }
);