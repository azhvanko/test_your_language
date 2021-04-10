function selectAnswer(event) {
    let answer = event.target;
    if (answer.className !== 'test-answer') {
        return;
    }

    let answers = answer.closest('.test-answers').children;

    for (let answer of answers) {
        if (answer.firstChild.matches('.test-answer-selected')) {
            answer.firstChild.setAttribute('class', 'test-answer');
            break;
        }
    }

    answer.setAttribute('class', 'test-answer test-answer-selected');

    let question = answer.closest('.test-wrap').querySelector('.test-question');
    let questionSpan = question.querySelector('.test-gap');

    if (question.querySelector('.test-gap-miss-empty')) {
        questionSpan.setAttribute('class', 'test-gap test-gap-miss');
    }

    questionSpan.innerHTML = answer.innerHTML;
}


async function getTestResult(url) {
    let testAnswers = getTestAnswers();
    let response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(testAnswers)
    });

    let result = await response.json();

    showTestResult(result['data']);
}


//https://docs.djangoproject.com/en/3.1/ref/csrf/
function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');

        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function getTestAnswers() {
    let questions = document.getElementById('languageTest').children;
    let questionsMap = new Map();

    for (let question of questions) {
        let questionId = question.getAttribute('data-question');
        let selectedAnswer = question.querySelector('.test-answer-selected');

        if (selectedAnswer) {
            answerId = selectedAnswer.getAttribute('data-answer');
        } else {
            answerId = '';
        }
        questionsMap.set(questionId, answerId);
    }
    return Object.fromEntries(questionsMap);
}


function showTestResult(rightAnswerList) {
    const rightSelectedAnswer = `test-answer test-answer-selected
                                 test-answer-selected-right`;
    const wrongSelectedAnswer = `test-answer test-answer-selected
                                 test-answer-selected-wrong`;
    let questions = document.getElementById('languageTest').children;
    let numberRightAnswers = 0;

    for (let question of questions) {
        let answers = question.querySelectorAll('.test-answer');
        let questionSpan = question.querySelector('.test-gap');
        let questionId = question.getAttribute('data-question');
        let rightAnswerId = rightAnswerList[questionId];

        questionSpan.setAttribute('class', 'test-gap');
        for (answer of answers) {
            let answerId = Number(answer.getAttribute('data-answer'));

            if (answerId === rightAnswerId) {
                questionSpan.innerHTML = answer.innerHTML;
            }

            if (answer.matches('.test-answer-selected')) {
                if (answerId === rightAnswerId) {
                    answer.setAttribute('class', rightSelectedAnswer);
                    numberRightAnswers += 1;
                } else {
                    answer.setAttribute('class', wrongSelectedAnswer);
                }
            }
        }
    }
    let testScorePercentage = Math.round(numberRightAnswers / questions.length * 100);
    let testScoreAnswer = getTestScoreAnswer(numberRightAnswers);

    document.getElementById('testScoreAnswers').innerHTML = testScoreAnswer;
    document.getElementById('testScorePercentage').innerHTML = testScorePercentage;
    document.querySelector('.test-score').hidden = false;
    document.querySelector('.btn-check-result').hidden = true;
    document.querySelector('.btn-restart-test').hidden = false;
}


function getTestScoreAnswer(value) {
    let result;
    let arr = [2, 3, 4];

    if (value === 1 || value > 20 && value % 10 === 1 ) {
        result = `вопрос`;
    } else if (arr.includes(value) || value > 20 && arr.includes(value % 10)) {
        result = 'вопроса';
    } else {
        result = 'вопросов';
    }
    return `${value} ${result}`;
}
