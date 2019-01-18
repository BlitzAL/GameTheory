from websocket import create_connection
import json
import random

URL = "ws://dmc.alepoydes.com:3014"

LOGIN = "Highway_to_hell"
PASSWORD = "w4WLC8JKzhL9IntHStpleSFqNKDqJkezOMpVn5GWKRVUn7qlppSwm5s4SHv7KKM1"
DEBUG = False

def receive():
    result = json.loads(ws.recv())
    if result["state"]=="error":
        print("Error: {}".format(result["error"]))
        return None
    return result

def send(msg):
    ws.send(json.dumps(msg))

if __name__ == "__main__":
    random.seed()
    ws = create_connection(URL)
    result = receive()
    assert(result["state"]=="info")
    
    send({"state":"login", "login": LOGIN, "password": PASSWORD, "debug": DEBUG})
    result = receive()
    if result is None:
        print("Access denied")
        exit(1)
    assert(result["state"]=="access")
   

    while True:
        result = receive()
        if result is None: continue
        game = result["game"]
        if result["state"]=="start":
            myhand = result["hand"]
            count = 0
            turn = 0
        elif result["state"]=="gameover":
            print("Game {} is finished with scores {}".format(game,result["scores"]))
            continue
        elif result["state"]=="turnover":
            print("Game {} end of turn, players moves are {}".format(game, result["moves"]))
            mass = result["moves"]
            pass
        else: 
            print("Unknown message: {}".format(result))
            exit(1)
			
        if count == 5:
           turn = 1
        else:
           turn = 0
		   
        move = turn
        count = count + 1
        send({"state":"move", "strategy": move, "game": game})