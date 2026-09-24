document.addEventListener("DOMContentLoaded", function () {

    const task = document.getElementById("task");
    const inputText = document.getElementById("inputText");
    const level = document.getElementById("level");
    const generateBtn = document.getElementById("generateBtn");
    const output = document.getElementById("output");
    const copyBtn = document.getElementById("copyBtn");
    const charCount = document.getElementById("charCount");
    const buttonText = document.getElementById("buttonText");
    const buttonIcon = document.getElementById("buttonIcon");


    inputText.addEventListener(
        "input",
        function () {

            charCount.textContent =
                `${inputText.value.length} characters`;

        }
    );


    task.addEventListener(
        "change",
        function () {

            const placeholders = {

                qa:
                    "Example: What is Python?",

                explain:
                    "Example: Explain Machine Learning",

                quiz:
                    "Example: Create a quiz about Python",

                summarize:
                    "Paste the text you want to summarize here...",

                learning:
                    "Example: I want to learn Python"

            };

            inputText.placeholder =
                placeholders[task.value];

            copyBtn.hidden = true;

        }
    );


    generateBtn.addEventListener(
        "click",
        generateAnswer
    );


    async function generateAnswer() {

        const text =
            inputText.value.trim();


        if (!text) {

            output.innerHTML = `
                <div class="error-box">
                    ⚠️ Please enter a question or topic.
                </div>
            `;

            return;
        }


        let url = "/qa";

        let body = {
            text: text
        };


        if (task.value === "explain") {

            url = "/explain";

            body = {
                topic: text,
                level: level.value
            };

        }


        else if (task.value === "quiz") {

            url = "/quiz";

            body = {
                topic: text,
                number_of_questions: 5,
                level: level.value
            };

        }


        else if (task.value === "summarize") {

            url = "/summarize";

            body = {
                text: text,
                number_of_sentences: 5
            };

        }


        else if (task.value === "learning") {

            url = "/learn/recommendations";

            body = {
                topic: text,
                weeks: 4,
                level: level.value
            };

        }


        generateBtn.disabled = true;

        buttonText.textContent =
            "Generating...";

        buttonIcon.textContent =
            "⏳";


        output.innerHTML = `
            <div class="loading">
                <div class="spinner"></div>

                <div>
                    EduGenie is thinking...
                </div>

                <small>
                    Creating your learning response
                </small>
            </div>
        `;


        try {

            const response =
                await fetch(
                    url,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(body)
                    }
                );


            const contentType =
                response.headers.get(
                    "content-type"
                ) || "";


            let data;


            if (
                contentType.includes(
                    "application/json"
                )
            ) {

                data =
                    await response.json();

            }

            else {

                const textResponse =
                    await response.text();

                data = {
                    detail:
                        textResponse ||
                        "Server returned an unexpected response."
                };

            }


            console.log(
                "API response:",
                data
            );


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Something went wrong."
                );

            }


            if (
                task.value === "quiz"
            ) {

                showQuiz(data);

            }

            else if (
                task.value === "learning"
            ) {

                showLearningPath(data);

            }

            else {

                showTextResult(
                    data.result
                );

            }

        }


        catch (error) {

            console.error(
                "EduGenie error:",
                error
            );

            output.innerHTML = `
                <div class="error-box">

                    <strong>
                        ❌ Something went wrong
                    </strong>

                    <br><br>

                    ${escapeHTML(
                        error.message
                    )}

                </div>
            `;

        }


        finally {

            generateBtn.disabled =
                false;

            buttonText.textContent =
                "Generate Answer";

            buttonIcon.textContent =
                "✨";

        }

    }


    function showTextResult(text) {

        const safeText =
            escapeHTML(
                text ||
                "No answer received."
            );


        output.innerHTML = `

            <div>

                <h3 class="answer-title">
                    ✨ EduGenie Response
                </h3>

                <div class="answer-text">
                    ${safeText.replace(
                        /\n/g,
                        "<br>"
                    )}
                </div>

            </div>
        `;


        copyBtn.hidden = false;


        copyBtn.onclick =
            async function () {

                await navigator.clipboard.writeText(
                    text || ""
                );

                copyBtn.textContent =
                    "✓ Copied";

                setTimeout(
                    function () {

                        copyBtn.textContent =
                            "📋 Copy";

                    },
                    1500
                );

            };

    }


    function showQuiz(data) {

        if (
            !data ||
            !Array.isArray(data.questions)
        ) {

            showTextResult(
                JSON.stringify(
                    data,
                    null,
                    2
                )
            );

            return;
        }


        let html = `

            <h3 class="answer-title">
                🧠
                ${escapeHTML(
                    data.title ||
                    "AI Quiz"
                )}
            </h3>

        `;


        data.questions.forEach(
            function (
                question,
                index
            ) {

                html += `
                    <div class="quiz-card">

                        <h3>
                            ${index + 1}.
                            ${escapeHTML(
                                question.question
                            )}
                        </h3>
                `;


                question.options.forEach(
                    function (option) {

                        html += `

                            <button
                                class="quiz-option"
                                type="button"
                                onclick='checkAnswer(
                                    this,
                                    ${JSON.stringify(option)},
                                    ${JSON.stringify(question.answer)}
                                )'
                            >
                                ${escapeHTML(option)}
                            </button>

                        `;

                    }
                );


                html += `

                        <div class="quiz-feedback">
                        </div>

                    </div>

                `;

            }
        );


        output.innerHTML =
            html;

        copyBtn.hidden = true;

    }


    window.checkAnswer =
        function (
            button,
            selected,
            correct
        ) {

            const card =
                button.closest(
                    ".quiz-card"
                );

            const feedback =
                card.querySelector(
                    ".quiz-feedback"
                );

            const buttons =
                card.querySelectorAll(
                    ".quiz-option"
                );


            buttons.forEach(
                function (btn) {

                    btn.disabled = true;

                }
            );


            if (
                selected === correct
            ) {

                button.classList.add(
                    "correct-answer"
                );

                feedback.innerHTML =
                    "✅ Correct!";

            }

            else {

                button.classList.add(
                    "wrong-answer"
                );

                feedback.innerHTML =
                    `❌ Correct answer: ${escapeHTML(correct)}`;

            }

        };


    function showLearningPath(data) {

        let html = `

            <h3 class="answer-title">
                🗺️
                ${escapeHTML(
                    data.title ||
                    "Your Learning Path"
                )}
            </h3>

            <p class="answer-text">
                ${escapeHTML(
                    data.overview ||
                    ""
                )}
            </p>

        `;


        if (
            Array.isArray(
                data.weeks
            )
        ) {

            data.weeks.forEach(
                function (week) {

                    html += `

                        <div class="week-card">

                            <div class="week-number">
                                WEEK ${escapeHTML(
                                    week.week
                                )}
                            </div>

                            <h3>
                                ${escapeHTML(
                                    week.topic
                                )}
                            </h3>

                            <p>
                                <strong>
                                    🎯 Goals
                                </strong>
                            </p>

                            <ul>
                    `;


                    (
                        week.goals ||
                        []
                    ).forEach(
                        function (goal) {

                            html += `
                                <li>
                                    ${escapeHTML(goal)}
                                </li>
                            `;

                        }
                    );


                    html += `
                            </ul>

                        </div>
                    `;

                }
            );

        }


        output.innerHTML =
            html;

        copyBtn.hidden = true;

    }


    function escapeHTML(text) {

        const div =
            document.createElement(
                "div"
            );

        div.textContent =
            String(text);

        return div.innerHTML;

    }

});