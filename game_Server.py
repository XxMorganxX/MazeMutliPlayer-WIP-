import socket, sys, pickle
from _thread import *
from maze_main import mazeGame
from game_Handler import gameHandle



Server = "192.168.7.83"
Port = 5555 # What port to use on the computer 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Types of connection

try:
    s.bind((Server, Port)) # binds socket to port
except socket.error as e:
    print(e)

s.listen(2) #Opens port and allows 2 clients to connect
print("Waiting for connection, Server Opened")

connected = set()
games = {}
idCount = 0




def threaded_client(conn, curr_player, gameId): # Run in the background - Doesn't have to finish executing before the next while loop is run
    global idCount
    conn.send(str.encode(str(curr_player)))

    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(8192))

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "0submit":
                        print(mazeGame.num_board)
                        #game.play(0, [mazeGame.num_board, mazeGame.rect_board])
                        
                    elif data == "1submit":
                        print("accepted Submisson")
                        #game.play(1, [mazeGame.num_board, mazeGame.rect_board])
                    elif data == "get":
                        pass
                    elif data == "nextPhase":
                        game.nextPhase()
                   

                    reply = game
                    conn.sendall(pickle.dumps(reply))

            else:
                break
        except:
            pass
    
    print("Lost Connection")
    try:
        del games[gameId]
        print(f"Closing Game {gameId}")

    except:
        pass

    idCount -= 1
    conn.close()

while True: # Continually send and recieve info
    conn, addr = s.accept() #conn = object, addr = IP address
    print(f"Connected to: {addr}")

    idCount += 1
    p = 0
    gameId = (idCount-1)//2

    if idCount % 2 == 1:
        games[gameId] = gameHandle(gameId)
        print("Creating new game")
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))
    