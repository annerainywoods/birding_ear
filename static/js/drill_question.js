
// DrillQuestion(mix_bird_list)

// createQuestion()
//   validateMix() // validate mix has at least 2 birds
//   getFrequencies() // get settings from Drill model
//   sortBirdList() // get list of user birds from mix and separate into new/learned/missed lists
//   chooseBirdPile() // use random number to decide which bird pile to pull from (new/learned/missed)
//   selectBird() // get random bird from bird_list where bird_pile = ___
//   selectDistractors() // get 2 random birds from bird list that aren't the selected Bird
//   randomizeOptions() // combine selected bird and distractors into one list, then scramble order
//   compilateAudio() // concatenate the audio for the birds in the question, same order multiple choice
//   playBird() // audio should auto play when page loads

//checkAnswer()
//   isUserCorrect() // compare user's answer against selected bird
//   updateBird_birdPile() // save selected bird's bird_pile to learned or missed, update list
//   playFeedback() // Play right or wrong sound followed by name of correct bird
//   highlightBird() // change color of button to the mix color
//   nextQuestion() // get new question and update screen (chooseBirdPile(),selectBird(),selectDistractors(),randomizeOptions(),etc)

//attributes
//   drill.frequency_new
//   drill.frequency_learned
//   drill.frequency_missed
//   mix.bird_list
//   option1
//   option2
//   option3
//   audio_compilation
//   audio_right
//   audio_wrong



/*
START DRILL // When user clicks Drill from a mix
    Get Mix ID
    Test that mix has at least 1 bird
    Get drill frequencies
        frequency_new
        frequency_learned
        frequency-missed
    Calculate sum of the drill frequencies and test that its not zero
    Calculate decimal fraction for each frequency (example frequency_new/sum_of_frequencies)
    Set range for each frequency (example 0-.33 = range_new, .34-.50 = range_learned, .51-.99 = range_missed)
    Go to drill question

CREATE DRILL QUESTION // program initiates this at end of START DRILL, or user selected answer option.
    Select question_bird
        generate random number
        test for frequency range random number corresponds to
        select random bird from corresponding bird pile
    Select two distractor birds at random from entire mix

    Randomize order of question_bird and distractor birds
    Concatenate audio for narration and call for all three birds + call of question_bird
    Display multiple choice
    When user leaves Drill pause the drill

CREATE FEEDBACK // When user selects an answer
    Check if selected answer is the question_bird
        YES: Play "bing", set bird status to "learned"
        NO: Play "bonk", play narration & set bird status to "missed"
    Go to next drill question

PAUSE DRILL // user clicks pause on audio player
*/