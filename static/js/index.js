var isActiveGame = false;
var maxPinsAllowed = 10;
var currentFrame = 1;

$(function () {
    startNewGame();
    refreshScore();
    $("#bStartGame").click(function () {
        startNewGame();
        refreshScore();
    });

    $("#bThrowBall").click(function () {
        throwBall();
    });

    window.setInterval(function(){
        refreshScore();
      }, 2000);

 });


function startNewGame(){
    $.post("start-game", function( data ) {
        data = JSON.parse(data);
        if(data.success !== undefined){
            isActiveGame = true;
            $("#fThrowBall").show();
            $("#messageOnAction").html("game is running....<br>current frame: "+currentFrame
            +" and max pins allowed "+maxPinsAllowed);
        }else
            alert("an error occured in starting the game");
    });
}


function throwBall(){
    var pinsThrown = $("#iPins").val();
    if(pinsThrown > maxPinsAllowed){
        alert("You cant throw more than "+maxPinsAllowed+" in this frame. Try again!")
    }else{
        $.ajax({
            type: 'POST',
            url: 'throw-ball',
            data: { 
                'pins': pinsThrown
            },
            success: function(data){
                data = JSON.parse(data);
                if(data.success.is_game_finished == 1){
                    finishGame();
                    return;
                }
                maxPinsAllowed = data.success.remaining_frame_pins;
                currentFrame = data.success.current_frame + 1;
                $("#messageOnAction").html("game is running....<br>current frame: "+currentFrame
                        +" and max pins allowed "+maxPinsAllowed);
                console.log(data);
            },
            error: function(data){  
                data = JSON.parse(data);              
                alert('an error occured' + data.error);
            }
        });
    }
}

function refreshScore(){
    $.post("get-score", function( data ) {
        data = JSON.parse(data);
        if(data["error"]!== undefined){
            alert("an error occured in score");
            return;
        }

        var totalScore = 0;
        var html="<table class=\"table table-striped\"><thead><tr><th>Frame</th><th>Score</th></tr></thead><tbody>";
        for(var i=0;i<10;i++){
            if(data["success"][i]){
                html += "<tr><td>"+(data["success"][i]["frame"]+1)+"</td><td>"+data["success"][i]["score"]+"</td></tr>"
                totalScore += data["success"][i]["score"];
            }
        }
        html += "<tr><td>Total Score</td><td>"+totalScore+"</td></tr>"
        html += "</tbody></table>";
        $("#tScore").html(html);
    });
}

function finishGame(){
    isActiveGame = false;
    $("#messageOnAction").text("Game has finished....")
    $("#fThrowBall").hide();
}