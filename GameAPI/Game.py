from flask import Blueprint,request
import json

game_bp = Blueprint('game_bp', __name__)


@game_bp.route("/start-game",methods=["POST"])
def resetGame():
    game = Game()
    game.cleanOldGameData()
    return json.dumps({"success":"game started"})


@game_bp.route("/get-score",methods=["POST"])
def getScore():
    game = Game()
    return json.dumps(game.getCurrentScore())

@game_bp.route("/throw-ball",methods=["POST"])
def throwBall():
    game = Game()
    return json.dumps(game.throwBall(int(request.form.get('pins'))))


class Game:
    maxframe = 10
    initialJSON = "{\"maxframe\":10,\"is_game_finshed\":0,\"current_frame\":0,\"remaining_frame_balls\":2,\"remaining_frame_pins\":10,\"data\":{}}"
    def cleanOldGameData(self):
        data_file = open("data/gamedata.txt", "w")
        data_file.write(self.initialJSON)
        data_file.close()

    def throwBall(self,pinCount):
        response = {}
        data = {}
        data_file = open("data/gamedata.txt", "r")
        data = json.loads(data_file.read())
        data_file.close()

        if data["is_game_finshed"] == 1:
            response["error"] = "game finished"
            return response

        if data["remaining_frame_balls"] == 2:
            data["data"][str(data["current_frame"])] = {}
            data["data"][str(data["current_frame"])]["score"] = {}
            data["data"][str(data["current_frame"])]["status"] = "normal"
            data["data"][str(data["current_frame"])]["score"]["0"] = pinCount
            if pinCount==10 and data["current_frame"]==10:
                data["remaining_frame_pins"] = 10
                data["remaining_frame_balls"] -= 1
            elif pinCount==10:
                data["remaining_frame_pins"] = 10
                data["data"][str(data["current_frame"])]["status"] = "strike"
                data["current_frame"] +=  1
            else:
                data["remaining_frame_pins"] -= pinCount
                data["remaining_frame_balls"] -= 1
        elif data["remaining_frame_balls"] == 1:
            prevScore = data["data"][str(data["current_frame"])]["score"]["0"]
            if prevScore+pinCount ==10 and data["current_frame"]==10:
                data["remaining_frame_balls"] = 1
                data["data"][str(data["current_frame"])]["status"] = "spare"
            elif prevScore+pinCount ==10:
                data["remaining_frame_balls"] = 2
                data["data"][str(data["current_frame"])]["status"] = "spare"
            else:
                data["remaining_frame_balls"] = 2
                data["data"][str(data["current_frame"])]["status"] = "normal"
            
            data["data"][str(data["current_frame"])]["score"]["1"] = pinCount
            data["remaining_frame_pins"] = 10
            data["current_frame"] += 1

        #saving current state
        data_file = open("data/gamedata.txt", "w")
        data_file.write(json.dumps(data))
        data_file.close()

        
        #check if game over
        if data["current_frame"] > 10 or (data["current_frame"] > 9 and data["data"][str(data["current_frame"]-1)]["status"] != "strike" and data["data"][str(data["current_frame"]-1)]["status"] != "spare"):
            response["success"] = {}
            response["success"]["is_game_finished"] = 1
        else:
            response["success"] = {}
            response["success"]["is_game_finished"] = 0
            response["success"]["remaining_frame_pins"] = data["remaining_frame_pins"]
            response["success"]["current_frame"] = data["current_frame"]

        return response
    
    def getCurrentScore(self):
        scores = {}
        response = {}
        data = {}
        data_file = open("data/gamedata.txt", "r")
        data = json.loads(data_file.read())
        data_file.close()

        for i in range(10):
            if str(i) in data["data"]:
                score = {}
                score["frame"] = i
                score["score"] = self.getFrameScore(i,data)
                scores[str(i)] = score
            else:
                break
        response["success"] = scores
        return response

    def getFrameScore(self,node,data):
        score = 0
        if(data["data"][str(node)]["status"]=="strike" and str(node+1) in data["data"]):
            score = self.getFrameScore(node+1,data)
        elif(data["data"][str(node)]["status"]=="spare" and str(node+1) in data["data"]):
            score = data["data"][str(node+1)]["score"]["0"]
        

        if "0" in data["data"][str(node)]["score"]:
            score += data["data"][str(node)]["score"]["0"] 
        if "1" in data["data"][str(node)]["score"]:
            score += data["data"][str(node)]["score"]["1"] 

        return score
