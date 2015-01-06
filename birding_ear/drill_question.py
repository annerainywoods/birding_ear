#DrillQuestion(mix.id)
#method: checkAnswer(selected_option)
#attributes: mix_id, bird_list, question_audio, option1, option2, option2
#bird_list is userbirds, which have bird_pile
#options are userbirds, which have narration, call, name
#constants: FREQUENCY_NEW, FREQUENCY_LEARNED, FREQUENCY_MISSED


'''
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


'''