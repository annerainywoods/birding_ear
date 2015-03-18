//CONSTANTS
var NUM_QUESTIONS = 5;
var PERCENT_LEVEL = [];
PERCENT_LEVEL[0] = 70;
PERCENT_LEVEL[1] = 90;
PERCENT_LEVEL[2] = 100;
var LEVEL = [];
LEVEL[0] = "Rookie Birder";
LEVEL[1] = "Advanced Birder";
LEVEL[2] = "Expert Birder";
var MESSAGE = [];
MESSAGE[0] = "Good job! Keep drilling to learn those birds.";
MESSAGE[1] = "Excellent! Very impressive achievement.";
MESSAGE[2] = "Wow! You have developed quite the birding ear.";

//GLOBALS
var QUIZ_BIRDS = [];
var USER_ANSWERS = [];
var QUESTION_LIST = [];

var request = new XMLHttpRequest();

function validateQuiz(data) {
    data.forEach(function (item) {
        QUIZ_BIRDS.push(item);
    });
    if (QUIZ_BIRDS.length < NUM_QUESTIONS) {
        return false;
    }
    return true;
}

function buildQuestionList() {
    // pick questions randomly
    var quiz_birds_proxy = [];
    for (var i = 0; i < QUIZ_BIRDS.length; i++) {
        quiz_birds_proxy.push(QUIZ_BIRDS[i]);
    }
    var random_bird;

    for (var j = 0; j < NUM_QUESTIONS; j++) {
        do {
            random_bird = Math.floor(Math.random() * (NUM_QUESTIONS - 0)) + 0;
        } while (quiz_birds_proxy[random_bird].used === true);
        //add the used property so we don't get duplicates
        quiz_birds_proxy[random_bird].used = true;
        QUESTION_LIST.push(quiz_birds_proxy[random_bird]);
    }
}

// update bird call and play audio
function playCall(index) {
    var call = document.getElementById("question_bird_audio");
    call.src = QUESTION_LIST[index].bird_call;
    console.log(QUESTION_LIST[index].bird_call);
}

function updateQuestionNum(index) {
    document.getElementById("question-number").innerHTML = (index + 1).toString();
    document.getElementById("question-total").innerHTML = NUM_QUESTIONS.toString();
}

function addHintListener(index) {
    // Give user the bird type when the click the hint button
    var hint_button = document.getElementById("hint");
    hint_button.addEventListener("click", function () {
        hint_button.innerHTML = QUESTION_LIST[index].bird_type;
    });
}

function clearHint() {
    // Give user the bird type when the click the hint button
    var hint_button = document.getElementById("hint");
    hint_button.innerHTML = "Hint";
}

function clearInputField() {
    var inputField = document.getElementById("birdname");
    inputField.value = ""
}

function addToAnswers(input) {
    USER_ANSWERS.push(input);
}

function checkQuestionNumber() {
    if (USER_ANSWERS.length < NUM_QUESTIONS) {
        // this is not the last question
        return false
    }
    else {
        //quiz questions are done
        console.log("last question");
        return true
    }
}

function toggleQuestionsOn() {
    var quizResults = document.getElementById("quiz-results");
    var quiz = document.getElementById("quiz");
    quizResults.style.display = "none";
    quiz.style.display = "block"
}

function toggleQuestionsOff() {
    var quizResults = document.getElementById("quiz-results");
    var quiz = document.getElementById("quiz");
    quizResults.style.display = "block";
    quiz.style.display = "none"
}

// stop player when user has selected an answer
function pauseCall() {
    var call = document.getElementById("question_bird_audio");
    call.pause();
}

function getScore() {
    // compare user answers to question list
    var score = 0;
    for (var i = 0; i < QUESTION_LIST.length; i++) {
        // console.log("question list " + i + " is " + QUESTION_LIST[i].name);
        // console.log("user answers " + i + " is " + USER_ANSWERS[i]);
        if (QUESTION_LIST[i].name.toLowerCase() == USER_ANSWERS[i].toLowerCase()) {
            // count how many answers are correct
            score++;
        }
    }
    // convert count to percentage
    score = Math.round((score / QUESTION_LIST.length) * 100);
    return score;
}
function showScore(score) {
    console.log("Score is " + score);
    var level;
    var message;
    if( score < PERCENT_LEVEL[0]) {
        level = score.toString() + "% " +  LEVEL[0];
        message = MESSAGE[0];
        console.log("level 0")
    }
    else if( score < PERCENT_LEVEL[1]) {
        level = score.toString() + "% " +  LEVEL[1];
        message = MESSAGE[1];
        console.log("level 1")
    }
    else
    {
        level = score.toString() + "% " +  LEVEL[2];
        message = MESSAGE[2];
        console.log("level 2")
    }
    // display level and message on screen
    document.getElementById("level").innerHTML = level;
    document.getElementById("message").innerHTML = message;
}

//TODO add listener to toggle audio button

//TODO add listener for btn_new_quiz to reload screen

function showFeedback() {
    var feedbackList = document.getElementById("quiz-feedback");
    for(var i = 0; i < QUESTION_LIST.length; i++) {
        // TODO http://www.w3schools.com/jsref/met_node_clonenode.asp
        // clone list item and append to feedbackList
        // Add innerHTML for user's answer and audio source for play button
        // If user's answer was wrong, add innerHTML for correct answer and relevant glyph class
        // Remove class "hidden" from the list item
    }
}


// When quiz questions are finished, show the answers
function showAnswers() {
    console.log("show answers");
    toggleQuestionsOff();
    pauseCall();
    var score = getScore();
    showScore(score);
    showFeedback();
}

function makeNewQuestion() {
    var index = USER_ANSWERS.length;
    //console.log("index is " + index + ". And QUESTION_LIST.length is " + QUESTION_LIST.length);
    if (index < QUESTION_LIST.length) {
        clearInputField();
        clearHint();
        updateQuestionNum(index);
        addHintListener(index);
        playCall(index);
    }
}

// When user submits answer, add to answers and make the next question, or show answers
function captureSubmit() {
    var input = document.getElementById("birdname").value;
    console.log("captureSubmit input is " + input);
    addToAnswers(input);
    var lastQuestion = checkQuestionNumber();
    if (lastQuestion) {
        showAnswers()
    }
    else {
        makeNewQuestion()
    }
    return false;
}

// When page loads, draw the first question
function drawQuiz(data) {
    var quiz_validates = validateQuiz(data);
    if (quiz_validates) {
        buildQuestionList();
        toggleQuestionsOn();
        makeNewQuestion();
    }
    else {
        //TODO add message in HTML
        console.log("Not enough birds " + QUIZ_BIRDS.length + " for quiz" + NUM_QUESTIONS);
    }
}

function onRequestChange() {
    //console.log(request.readyState, request.status);
    if ((request.readyState == 4) && (request.status == 200)) {
        var data = JSON.parse(request.responseText);
        drawQuiz(data);
    }
}

function fetch() {
    var mix_slug = document.getElementById("mix_slug").innerHTML;
    request.onload = undefined;
    request.onreadystatechange = onRequestChange;
    var url = "/mix_drill_birds/" + mix_slug + "/";
    //console.log(url);
    request.open("GET", url, true);
    request.send();
}

function load() {
    fetch();
}

window.addEventListener("load", load);