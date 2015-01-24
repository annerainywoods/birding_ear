var AWOODS = {};
AWOODS.DRILL =  function() {
        var LEARNED_MIN = 5; // Learned bird pile has a minimum before app will draw from it
        var DRILL_MIN = 5; // Number of birds in the drill can't be smaller than this
        var NUM_ANSWER_OPTIONS = 3; // Number of answer options in the multiple choice
        var MILLISECONDS_FOR_ANSWER = 1000; // After the bird call plays this is the pause before answer is given
        var MILLISECONDS_FOR_NEXT = 6000; // After the bird call plays this is the pause before next question loads
        var QUESTION_BIRD; // the correct answer for the drill
        var BIRD_PILE_FREQUENCIES; // a user-set percentage controls how often the question bird is pulled from Learned, Missed or New.
        var BIRD_PILE_LISTS; // The birds for the drill are divided into three lists: Learned, Missed or New.
        var DRILL_BIRDS; // The list of birds for the drill (mix birds minus and user-set "excluded" birds)

        //TODO add color info

        var request = new XMLHttpRequest();

        function draw(data) {
            var list = document.getElementById("list");
            var template = document.getElementById("template");
            var output = [];
            data.forEach(function (item) {
                //console.log(item);
                var text = template.innerHTML;
                for (var p in item) {
                    if (item.hasOwnProperty(p)) {
                        text = text.replace("{bird." + p + "}", item[p]);
                    }
                }
                output.push(text)
                });
            list.innerHTML = "<li>" + output.join("</li><li>") + "</li>";
        }

        // User can remove specific birds from drills on the bird detail page
        function removeExcluded(data) {
            var drill_birds = [];
            data.forEach(function (item) {
                if (item["excluded"] == false) {
                    drill_birds.push(item);
                }
            });
            return drill_birds;
        }

        function validateDrill(drill_birds) {
            if (drill_birds.length < DRILL_MIN) {
                console.log(drill_birds.length + "Not enough birds to meet the drill minimum (" + DRILL_MIN + ")");
                return false;
            }
            if (DRILL_MIN < LEARNED_MIN) {
                console.log("Can't have fewer birds in the DRILL minimum (" + DRILL_MIN + ") than the LEARNED minimum (" + LEARNED_MIN + ")");
                return false;
            }
            if (DRILL_MIN < NUM_ANSWER_OPTIONS) {
                console.log("Can't have fewer birds in the DRILL minimum (" + DRILL_MIN + ") than the number of answer options(" + NUM_ANSWER_OPTIONS + ")");
                return false;
            }
            return true;
        }

        // show the number of birds for the drill
        function showTotalBirds(array) {
            document.getElementById("drill_total_span").innerHTML = array.length;
        }

        // Frequencies are set by user in "settings". Gets the setting for each birdpile and calculates percent.
        function getFrequencyPercentages() {
            var frequency_new = Number(document.getElementById("frequency_new").innerHTML);
            var frequency_learned = Number(document.getElementById("frequency_learned").innerHTML);
            var frequency_missed = Number(document.getElementById("frequency_missed").innerHTML);
            var sum = frequency_new + frequency_learned + frequency_missed;
            var percentages = [];
                percentages['new'] = (frequency_new/sum);
                percentages['learned'] = (frequency_learned/sum);
                percentages['missed'] = (frequency_missed/sum);
            console.log("%NEW:" + percentages['new'] + ", %LEARNED:" + percentages['learned'] + ", % MISSED:" + percentages['missed']);
            return percentages;
        }

        // sorts drill birds into the three bird piles: New, Learned, Missed
        function sortBirdPiles(drill_birds) {
            var bird_pile_New = [];
            var bird_pile_Learned = [];
            var bird_pile_Missed = [];
            drill_birds.forEach(function (item) {
                switch(item["bird_pile"]) {
                    case "N":
                        bird_pile_New.push(item);
                        break;
                    case "L":
                        bird_pile_Learned.push(item);
                        break;
                    case "M":
                        bird_pile_Missed.push(item);
                        break;
                    default:
                        console.log(item["bird_pile"] + ": Bird without bird_pile in function SortBirdPiles")
                }
            });
            var sortedBirdList = [];
                sortedBirdList['new'] = bird_pile_New;
                sortedBirdList['learned'] = bird_pile_Learned;
                sortedBirdList['missed'] = bird_pile_Missed;
            return sortedBirdList;
        }

        //make buttons for multiple choice, specific values are added in later
        function makeButtons() {
            var buttonId;
            var buttonToAdd;
            var parentDiv = document.getElementById("buttons");
            for (var i = 0; i < NUM_ANSWER_OPTIONS; i++) {
                buttonId = "option" + i;
                buttonToAdd = document.createElement("button");
                buttonToAdd.setAttribute("id", buttonId);
                buttonToAdd.setAttribute("class", "btn btn-default btn-lg btn-block");
                buttonToAdd.setAttribute("role", "button");
                buttonToAdd.setAttribute("value", "");
                parentDiv.appendChild(buttonToAdd);
            }
        }

        //check if New birdpile is empty or not
        function verifyNewBirdPile(array) {
            return (array.length > 0);
        }

        //select which bird pile the question bird will be pulled from.
        function chooseBirdPile(bird_pile_frequencies, new_has_birds) {
            var selector = Math.random();
            var question_bird_pile;
            var percent_new = bird_pile_frequencies['new'];
            var percent_learned = bird_pile_frequencies['learned'];
            if ( new_has_birds) {
                if (selector < percent_new) {
                    question_bird_pile = "N";
                }
                else if (selector < percent_learned + percent_new) {
                    question_bird_pile = "L";
                }
                else {
                    question_bird_pile = "M";
                }
            }
            else {
            // since new birds will go down to zero as the user drills,
            // divide the percentage for New between Missed and Learned
            //TODO needs more accurate offset
                var offset = percent_new * .5;
                if (selector < (percent_learned + offset)) {
                    question_bird_pile = "L";
                    console.log("no New birds, used offset");
                }
                else {
                    question_bird_pile = "M";
                    console.log("no New birds, used offset");
                }
            }
            return question_bird_pile;
        }

        // find the matching bird pile and randomly select a bird from it.
        function selectBird(bird_pile_lists, question_bird_pile) {
            var question_bird = '0';
            var random_bird;
            var i = 0;
            console.log('Looking for a bird in ' + question_bird_pile);
            do {
                switch (question_bird_pile) {
                    case "M":
                        //if case matches M and there are birds in that bird pile...
                        if (bird_pile_lists['missed'].length != 0) {
                            //generate random number between 0 and the number of birds
                            random_bird = Math.floor(Math.random() * (bird_pile_lists['missed'].length - 0)) + 0;
                            //use random number for index
                            question_bird = bird_pile_lists['missed'][random_bird];
                            console.log('Found bird in M');
                            return question_bird;
                        }
                        else {
                            console.log('M bird is pile empty, fall thru to next case');
                        }
                    case "N":
                        //if case matches N and there are birds in that bird pile...
                        if (bird_pile_lists['new'].length != 0) {
                            //generate random number between 0 and the number of birds
                            random_bird = Math.floor(Math.random() * (bird_pile_lists['new'].length - 0)) + 0;
                            //use random number for index
                            question_bird = bird_pile_lists['new'][random_bird];
                            console.log('Found bird in N');
                            return question_bird;
                        }
                        else {
                            console.log('N bird pile is empty, fall thru to next case');
                        }
                    case "L":
                        //if case matches L and the number of birds meets the learned birdpile minimum...
                        if (bird_pile_lists['learned'].length >= LEARNED_MIN) {
                            //generate random number between 0 and the number of birds
                            random_bird = Math.floor(Math.random() * (bird_pile_lists['learned'].length - 0)) + 0;
                            //use random number for index
                            question_bird = bird_pile_lists['learned'][random_bird];
                            console.log("Found bird in L. Number of birds in pile=" + bird_pile_lists['learned'].length + ", minimum=" + LEARNED_MIN);
                            return question_bird;
                        }
                        else {
                            console.log('L bird pile is <= ' + LEARNED_MIN + ", starting switch again");
                            question_bird_pile = "M";
                        }
                }
                i++;
            } while(i < 10); // counter is to ensure infinite loop will not occur.
            console.log("exited without finding bird");

        }

        function selectAnswerOptions(question_bird, possible_birds) {
            var selector;
            console.log("question bird is "  + question_bird.name);
            var answerOptions = [];
            //add question bird to the answer options
            answerOptions.push(question_bird);
            //remove question bird from the remaining possible birds
            var question_bird_index = possible_birds.indexOf(question_bird);
            possible_birds.splice(question_bird_index, 1);
            for (var i = 1; i < NUM_ANSWER_OPTIONS; i++) {
                selector = Math.floor(Math.random() * (possible_birds.length - 0)) + 0;
                answerOptions[i] = possible_birds[selector];
                possible_birds.splice(selector, 1);
                console.log("distractor bird " + i + " is "  + answerOptions[i].name);
            }
            shuffle(answerOptions);
            return answerOptions;
        }

        function shuffle(array) {
            var currentIndex = array.length, temporaryValue, randomIndex;
            while (0 !== currentIndex) {
                randomIndex = Math.floor(Math.random() * currentIndex);
                currentIndex -= 1;
                temporaryValue = array[currentIndex];
                array[currentIndex] = array[randomIndex];
                array[randomIndex] = temporaryValue;
            }
            return array;
        }

        function updateButtons(answerOptions) {
            for (var i = 0; i < answerOptions.length; i++) {
                var buttonId = "option" + i;
                var button = document.getElementById(buttonId);
                button.innerHTML = answerOptions[i].name;
                button.name = answerOptions[i].name;
                button.value = answerOptions[i].id;
                button.disabled = false;
                button.style.background = '#4b6071';
            }
        }

        // show the number of learned birds for the drill
        function showLearnedBirds(array) {
            document.getElementById("learned_birds_span").innerHTML = array.length;
        }

        // update bird call and play audio
        function playCall(question_bird) {
            var call = document.getElementById("question_bird_audio");
            call.src = question_bird.bird_call;
            console.log(question_bird.bird_call);
        }

        function playNarration(question_bird) {
            var answer_audio = new Audio(question_bird.bird_narration);
            answer_audio.play();
        }

        function updateBirdPiles(question_bird, question_missed, bird_pile_lists) {
            // find birdpile for question bird
            var birdpile = question_bird.bird_pile;
            console.log("question bird pile: " + birdpile);
            console.log( "Learned:" + bird_pile_lists['learned'].length + ", Missed:" + bird_pile_lists['missed'].length + ", New:" + bird_pile_lists['new'].length );

            var question_bird_index;
            if (question_missed) {
                if (birdpile === "N") {
                    //change birdpile on bird object
                    question_bird.bird_pile = "M";
                    //add bird to Missed list
                    bird_pile_lists['missed'].push(question_bird);
                    //remove bird from New list
                    question_bird_index = bird_pile_lists['new'].indexOf(question_bird);
                    bird_pile_lists['new'].splice(question_bird_index, 1);
                    console.log( "Learned:" + bird_pile_lists['learned'].length + ", Missed:" + bird_pile_lists['missed'].length + ", New:" + bird_pile_lists['new'].length );

                    //TODO updateJASONbirdPile(question_bird, "M");

                }
                else if (birdpile === "L") {
                    //change birdpile on bird object
                    question_bird.bird_pile = "M";
                    //add bird to Missed list
                    bird_pile_lists['missed'].push(question_bird);
                    //remove bird from Learned list
                    question_bird_index = bird_pile_lists['learned'].indexOf(question_bird);
                    bird_pile_lists['learned'].splice(question_bird_index, 1);
                    console.log( "Learned:" + bird_pile_lists['learned'].length + ", Missed:" + bird_pile_lists['missed'].length + ", New:" + bird_pile_lists['new'].length );

                    //TODO updateJASONbirdPile(question_bird, "M");
                }
                else {
                    console.log("question bird was already Missed, no change to birdpile");
                }
            }
            else { //TODO add logic for updated birdpiles
                if (birdpile === "N") {
                    //remove bird from New
                    //add bird to Learned
                }
                else if (birdpile === "M") {
                    //remove bird from Missed
                    //add bird to Learned
                }
            }
            return bird_pile_lists;
        }

        function disableButtons() {
            for (var i = 0; i < NUM_ANSWER_OPTIONS; i++) {
                var buttonId = "option" + i;
                var button = document.getElementById(buttonId);
                button.disabled = true;
            }
        }

        function highlightAnswer(question_bird) {
            var name = question_bird.name;
            console.log(name);
            document.getElementsByName(name)[0].style.background = '#000000';
        }

        function giveFeedback(question_bird, bird_pile_frequencies, bird_pile_lists, drill_birds) {
            var question_missed;
            //listen for bird call audio to end
            var player = document.getElementById("question_bird_audio");
            player.onended=function() {
                setTimeout(playNarration, MILLISECONDS_FOR_ANSWER, question_bird);
                setTimeout(disableButtons, MILLISECONDS_FOR_ANSWER);
                setTimeout(highlightAnswer, MILLISECONDS_FOR_ANSWER, question_bird);
                question_missed = true;
                bird_pile_lists = updateBirdPiles(question_bird, question_missed, bird_pile_lists);
                setTimeout(makeNewQuestion, MILLISECONDS_FOR_NEXT, bird_pile_frequencies, bird_pile_lists, drill_birds);
                //TODO update bird piles
                //TODO create next question
            };
            //listen for user to click button
            for (var i = 0; i < NUM_ANSWER_OPTIONS; i++) {
                var buttonId = "option" + i;
                var button = document.getElementById(buttonId);
                button.addEventListener("click", console.log("button created"));
                //TODO finish button listener
                //TODO stop player
            }
        }

        function makeNewQuestion(bird_pile_frequencies, bird_pile_lists, drill_birds) {
            var new_has_birds = verifyNewBirdPile(bird_pile_lists["new"]);
            var question_bird_pile = chooseBirdPile(bird_pile_frequencies, new_has_birds);
            var question_bird = selectBird(bird_pile_lists, question_bird_pile);
            var answer_options = selectAnswerOptions(question_bird, drill_birds);
            updateButtons(answer_options);
            showLearnedBirds(bird_pile_lists["learned"]);
            playCall(question_bird);
            giveFeedback(question_bird, bird_pile_frequencies, bird_pile_lists, drill_birds);
        }

        function drawQuestion(data) {
            var drill_birds = removeExcluded(data);
            var drill_validates = validateDrill(drill_birds);
            if (drill_validates) {
                showTotalBirds(drill_birds);
                var bird_pile_frequencies = getFrequencyPercentages();
                var bird_pile_lists = sortBirdPiles(drill_birds);
                makeButtons();
                makeNewQuestion(bird_pile_frequencies, bird_pile_lists, drill_birds);
            }
            else {
                console.log("Drill fails validation");
                document.getElementById("fail-validation").innerHTML = "You need at least " + DRILL_MIN + " birds available for a drill.";
            }

            //   ONCLICK check(Answer) check answer, give feedback, and move bird into new bird_pile and update JSON object.
            //   TIMEOUT drawMultipleChoice() repeat Choose BirdPile(), etc
        }

        function onRequestChange() {
            //console.log(request.readyState, request.status);
            if ((request.readyState == 4) && (request.status == 200)) {
                var data = JSON.parse(request.responseText);
                //draw(data);
                drawQuestion(data);
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

        function saveData(formData){
            request.open("POST","/ajax/",true);
            request.onload = fetch;
            request.setRequestHeader("Content-type","application/x-www-form-urlencoded");
            request.send(formData);
        }
        function captureSubmit(){
            //Get inputs inside form and iterate over them.
            var elementList = document.getElementById("f1").children;
            formDataList = [];
            //Creating something like this:
            //title=spiderman&role=hero&color=red
            for(var i=0; i < elementList.length; i++){
                var element = elementList[i];
                formDataList.push(
                        encodeURIComponent(element.name)
                        + "=" +
                        encodeURIComponent(element.value)
                );
                console.log(element.name);
            }
            saveData(formDataList.join("&"));
            //CANCEL FORM SUBMISSION; must be returned in onsubmit below.
            return false;
        }

}(); //IIFE