//equivalent
var a = "Text";
a = 'Text'


//equivalent
o = {};
o = Object();
o = new Object();
var o = {};

// variables can contain objects
var data = {
    "APPL" : 123,
    "INTL" : 456
}

//variables can contain functions
function f(){
    //...
}

var f = function(){
    //...
}

// default namespace is "window"

//equivalent of a class is...

var game = {
    score : 0,
    win : function(amount) {
        this.score += amount;
    }
}
game.win(99);
game.win(2);
console.log(game.score)

//equivalent to
var game = {};
game.score = 0;
game.win = function() {
    //...
}





