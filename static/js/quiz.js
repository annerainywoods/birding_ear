var AWOODS = {};
AWOODS.QUIZ =  function() {
    //CONSTANTS
    var NUM_QUESTIONS = 5;
    var LEVEL = [];
    LEVEL[0] = "Rookie Birder";
    LEVEL[1] = "Advanced Birder";
    LEVEL[2] = "Expert Birder";
    var MESSAGE = [];
    MESSAGE[0] = "Good job! Keep drilling to learn those birds.";
    MESSAGE[1] = "Excellent! Very impressive achievement.";
    MESSAGE[2] = "Wow! You have developed quite the birding ear.";

    //GLOBALS
    var QUIZ_BIRDS;
    var INPUT_ARRAY = [];
    var QUESTION_LIST = [];

    var request = new XMLHttpRequest();

    function validateQuiz(data) {
        QUIZ_BIRDS = [];
        data.forEach(function (item) {
            QUIZ_BIRDS.push(item);
        });
        if(QUIZ_BIRDS.length < NUM_QUESTIONS) {
            return false;
        }
        return true;
    }

    function buildQuestionList() {
        // pick questions randomly
        var random_bird;
        for (var j = 0; j < NUM_QUESTIONS; j++) {
            do {
                random_bird = Math.floor(Math.random() * (NUM_QUESTIONS - 0)) + 0;
            } while (QUIZ_BIRDS[random_bird].used != undefined);
            //add the used property so we don't get duplicates
            QUIZ_BIRDS[random_bird].used = true;
            QUESTION_LIST.push(QUIZ_BIRDS[random_bird]);
        }
    }

    function addHintListener(index) {
        // Give user the bird type when the click the hint button
        var hint = document.getElementsByTagName("button")[0];
        var text = document.createTextNode(QUESTION_LIST[index].bird_type + " ");
        console.log(QUESTION_LIST[index].bird_type);
        hint.addEventListener("click", function () {
            hint.appendChild(text);
            //TODO make icon dark grey
        });
    }

    function countQuestions(input) {
        INPUT_ARRAY = INPUT_ARRAY.push(input);
        if(INPUT_ARRAY.length < NUM_QUESTIONS) {
            makeNewQuestion()
        }
        else {
            showAnswers();
        }
    }

    function makeNewQuestion() {
        var input;
        var index = INPUT_ARRAY.length;
        document.getElementById("question-number").innerHTML = (index + 1).toString();
        document.getElementById("question-total").innerHTML = NUM_QUESTIONS.toString();
        addHintListener(index);
        //TODO update audio
        var form = document.getElementById("form");
        form.onsubmit = function() {
            //TODO get input
            countQuestions(input);
        }

    }

    function drawQuiz(data) {
        var quiz_validates = validateQuiz(data);
        if (quiz_validates) {
            buildQuestionList();
            makeNewQuestion();

            //showResults(question_list, user_total_input);  //TODO hide question div and show results div

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

}(); //IIFE