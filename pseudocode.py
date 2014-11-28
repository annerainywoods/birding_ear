'''

class="glyphicon glyphicon-plus"

HOME PAGE
    Display mix buttons in order of created_by, favorites, add-new

ADD NEW // When Add New is clicked
    Go to add_new.html
    Show empty form
    On submit
        Create mix record
        Display mix button on home page

EDIT MIX // When user clicks Edit from a mix
    Update form data
        If drill question is paused, unpause.
    Delete mix

VIEW MIX // When user clicks View from a mix

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

CREATE FEEDBACK // When user selects an answer
    Check if selected answer is the question_bird
        YES: Play "bing", set bird status to "learned"
        NO: Play "bonk", play narration & set bird status to "missed"
    Go to next drill question

PAUSE DRILL // user clicks pause on audio player


'''