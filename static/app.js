// ==========================================
// EduGenie - Programming Learning App
// ==========================================

document.addEventListener("DOMContentLoaded", () => {

    console.log("EduGenie loaded successfully 🚀");

    const language =
        document.getElementById("language");

    const difficulty =
        document.getElementById("difficulty");

    const question =
        document.getElementById("question");

    const topic =
        document.getElementById("topic");

    const answer =
        document.getElementById("answer");

    const result =
        document.getElementById("result");


    // ==========================================
    // API Helper
    // ==========================================

    async function requestAPI(url, body) {

        const response = await fetch(url, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(body)

        });


        const contentType =
            response.headers.get("content-type") || "";


        if (!contentType.includes("application/json")) {

            const text =
                await response.text();

            console.error(
                "Server response:",
                text
            );

            throw new Error(
                "Server returned an invalid response."
            );
        }


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Request failed."
            );
        }


        return data;
    }


    // ==========================================
    // Loading
    // ==========================================

    function loading(element, text) {

        element.innerHTML = `

            <div class="loading-box">

                <div class="loader"></div>

                <p>${text}</p>

            </div>

        `;
    }


    // ==========================================
    // Error
    // ==========================================

    function showError(element, error) {

        element.innerHTML = `

            <div class="error-box">

                ❌ ${escapeHTML(
                    error.message || error
                )}

            </div>

        `;
    }


    // ==========================================
    // Ask Question
    // ==========================================

    window.askQuestion = async function () {

        const selectedLanguage =
            language.value;

        const selectedDifficulty =
            difficulty.value;

        const userQuestion =
            question.value.trim();


        if (!userQuestion) {

            alert(
                "Please enter your question."
            );

            question.focus();

            return;
        }


        loading(
            answer,
            "Preparing your answer..."
        );


        try {

            const data =
                await requestAPI(
                    "/qa",
                    {
                        language:
                            selectedLanguage,

                        question:
                            userQuestion,

                        difficulty:
                            selectedDifficulty
                    }
                );


            answer.innerHTML = `

                <div class="answer-content">

                    <h3>
                        💡 ${selectedLanguage}
                        Answer
                    </h3>

                    <div>
                        ${data.answer}
                    </div>

                    <button
                        class="copy-btn"
                        onclick="copyAnswer()"
                    >
                        📋 Copy Answer
                    </button>

                </div>

            `;

            answer.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        }

        catch (error) {

            showError(
                answer,
                error
            );
        }

    };


    // ==========================================
    // Explain Topic
    // ==========================================

    window.explainTopic = async function () {

        const selectedLanguage =
            language.value;

        const selectedDifficulty =
            difficulty.value;

        const userTopic =
            topic.value.trim();


        if (!userTopic) {

            alert(
                "Please enter a topic."
            );

            topic.focus();

            return;
        }


        loading(
            result,
            "Preparing topic explanation..."
        );


        try {

            const data =
                await requestAPI(
                    "/explain",
                    {
                        language:
                            selectedLanguage,

                        topic:
                            userTopic,

                        difficulty:
                            selectedDifficulty
                    }
                );


            result.innerHTML = `

                <div class="result-content">

                    <h3>
                        📚 Topic Explanation
                    </h3>

                    ${data.explanation}

                </div>

            `;


            result.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        }

        catch (error) {

            showError(
                result,
                error
            );
        }

    };


    // ==========================================
    // Generate Quiz
    // ==========================================

    window.generateQuiz = async function () {

        const selectedLanguage =
            language.value;

        const selectedDifficulty =
            difficulty.value;

        const userTopic =
            topic.value.trim();


        const quizTopic =
            userTopic ||
            selectedLanguage;


        loading(
            result,
            "Creating your quiz..."
        );


        try {

            const data =
                await requestAPI(
                    "/quiz",
                    {
                        language:
                            selectedLanguage,

                        topic:
                            quizTopic,

                        difficulty:
                            selectedDifficulty
                    }
                );


            renderQuiz(
                data.questions
            );


            result.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        }

        catch (error) {

            showError(
                result,
                error
            );
        }

    };


    // ==========================================
    // Render Quiz
    // ==========================================

    function renderQuiz(questions) {

        let html = `

            <div class="quiz-container">

                <h3>
                    🧠 ${language.value}
                    Programming Quiz
                </h3>

        `;


        questions.forEach(
            (item, index) => {

                html += `

                    <div
                        class="quiz-question"
                        data-answer="${item.answer}"
                    >

                        <h4>
                            ${index + 1}.
                            ${escapeHTML(
                                item.question
                            )}
                        </h4>

                `;


                item.options.forEach(
                    (option, optionIndex) => {

                        html += `

                            <label
                                class="quiz-option"
                            >

                                <input
                                    type="radio"
                                    name="quiz-${index}"
                                    value="${optionIndex}"
                                >

                                ${escapeHTML(
                                    option
                                )}

                            </label>

                        `;
                    }
                );


                html += `

                    </div>

                `;
            }
        );


        html += `

                <button
                    class="submit-quiz-btn"
                    onclick="submitQuiz()"
                >
                    ✅ Submit Quiz
                </button>

                <div id="quiz-score"></div>

            </div>

        `;


        result.innerHTML = html;
    }


    // ==========================================
    // Submit Quiz
    // ==========================================

    window.submitQuiz = function () {

        const questions =
            document.querySelectorAll(
                ".quiz-question"
            );


        let score = 0;

        let answered = 0;


        questions.forEach(
            (item, index) => {

                const selected =
                    document.querySelector(
                        `input[name="quiz-${index}"]:checked`
                    );


                if (!selected) {
                    return;
                }


                answered++;


                const correct =
                    Number(
                        item.dataset.answer
                    );


                if (
                    Number(
                        selected.value
                    ) === correct
                ) {

                    score++;
                }

            }
        );


        const percentage =
            questions.length > 0
                ? Math.round(
                    (score /
                        questions.length) *
                    100
                )
                : 0;


        const scoreBox =
            document.getElementById(
                "quiz-score"
            );


        scoreBox.innerHTML = `

            <div class="score-card">

                🎉 Quiz Completed!

                <br><br>

                Score:
                <strong>
                    ${score}/${questions.length}
                </strong>

                <br>

                Percentage:
                <strong>
                    ${percentage}%
                </strong>

                <br>

                Answered:
                <strong>
                    ${answered}
                </strong>

                <br><br>

                ${
                    percentage >= 70
                    ? "🌟 Great job! Keep learning!"
                    : "📖 Keep practicing. You can do it!"
                }

            </div>

        `;
    };


    // ==========================================
    // Copy Answer
    // ==========================================

    window.copyAnswer = async function () {

        const content =
            document.querySelector(
                ".answer-content"
            );


        if (!content) return;


        try {

            await navigator.clipboard.writeText(
                content.innerText
            );


            const button =
                document.querySelector(
                    ".copy-btn"
                );


            if (button) {

                button.innerText =
                    "✅ Copied!";


                setTimeout(() => {

                    button.innerText =
                        "📋 Copy Answer";

                }, 1500);

            }

        }

        catch (error) {

            alert(
                "Unable to copy answer."
            );
        }

    };


    // ==========================================
    // HTML Escape
    // ==========================================

    function escapeHTML(value) {

        const div =
            document.createElement("div");

        div.textContent =
            String(value);

        return div.innerHTML;
    }


    // ==========================================
    // Enter Key
    // ==========================================

    question.addEventListener(
        "keydown",
        (event) => {

            if (
                event.key === "Enter" &&
                !event.shiftKey
            ) {

                event.preventDefault();

                window.askQuestion();
            }

        }
    );


    console.log(
        "✅ EduGenie ready!"
    );

});