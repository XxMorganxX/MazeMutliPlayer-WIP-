import socket, _thread, sys

Server = ""
Port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((Server, Port))
except socket.error as e:
    print(e)

s.listen(2) 
print("waiting for server, Server Opened")

def threaded_client(conn):
    pass

while True:
    conn, addr = s.accept()