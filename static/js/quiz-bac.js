//CONSTANTS
var NUM_QUESTIONS = 5;
var LEVEL = {};
LEVEL[0] = "Rookie Birder";
LEVEL[1] = "Advanced Birder";
LEVEL[2] = "Expert Birder";
var MESSAGE = {};
MESSAGE[0] = "Good job! Keep drilling to learn those birds.";
MESSAGE[1] = "Excellent! Very impressive achievement.";
MESSAGE[2] = "Wow! You have developed quite the birding ear.";

//GLOBALS
var QUIZ_BIRDS = [];
var USER_ANSWERS = [];
USER_ANSWERS = [];
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

function validateInput(input) {
    addToAnswers(input);
    if (USER_ANSWERS.length < NUM_QUESTIONS) {
        clearHint();
        makeNewQuestion();
    }
    else {
        showAnswers();
    }
}

function addToAnswers(input) {
    console.log("Before adding the current input, user answers array length is " + USER_ANSWERS.length);
    USER_ANSWERS.push(input);

    console.log("After adding the current input, the user answers length is " + USER_ANSWERS.length);
}

function showAnswers() {
    console.log("show answers");
    for (i = 0; i < NUM_QUESTIONS; i++) {
        USER_ANSWERS[i] //TODO print user answers to the screen
    }

}

function makeNewQuestion() {
    var index = USER_ANSWERS.length;
    //console.log("index is " + index + ". And QUESTION_LIST.length is " + QUESTION_LIST.length);
    if (index < QUESTION_LIST.length) {
        updateQuestionNum(index);
        addHintListener(index);
        playCall(index);
    }
}


function drawQuiz(data) {
    var quiz_validates = validateQuiz(data);
    if (quiz_validates) {
        buildQuestionList();
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

function captureSubmit() {
    var input = document.getElementById("birdname").value;
    console.log("captureSubmit input is " + input);
    validateInput(input);
    return false;
}