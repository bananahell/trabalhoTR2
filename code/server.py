import socket
import threading
from utils import *


rooms = {}


def main():
    print("[STARTING] Server is starting...")
    print("ADDRESS_FAMILY = " + str(ADDRESS_FAMILY))
    print("ADDR = " + str(ADDR))
    server = socket.socket(ADDRESS_FAMILY, socket.SOCK_STREAM)
    server.bind(ADDR)
    print("[LISTENING] Server is listening on " + SERVER)
    while True:
        server.listen(20)
        conn, addr = server.accept()
        username = ""
        room = 0
        msgLength = conn.recv(HEADER).decode(FORMAT)
        if msgLength:
            msgLength = int(msgLength)
            username = conn.recv(msgLength).decode(FORMAT)
            msgLength = int(conn.recv(HEADER).decode(FORMAT))
            room = conn.recv(msgLength).decode(FORMAT)
        roomFound = rooms.get(room)
        if roomFound:
            for client in roomFound:
                auxstring = "[NOTICE] " + username + " connected"
                client.send(auxstring.encode(FORMAT))
            roomFound.append(conn)
        else:
            newRoom = [conn]
            rooms[room] = newRoom
        thread = threading.Thread(
            target=handleClient, args=(conn, addr, room, username)
        )
        thread.start()
        print("[ACTIVE CONNECTIONS] " + str(threading.active_count() - 1))


def handleClient(conn, addr, room, username):
    print("[NEW CONNECTION] " + username + " connected to room " + room)
    connected = True
    while connected:
        msgLength = conn.recv(HEADER).decode(FORMAT)
        if msgLength:
            msgLength = int(msgLength)
            msg = conn.recv(msgLength).decode(FORMAT)
            roomFound = rooms.get(room)
            for client in roomFound:
                if client != conn:
                    if msg == DISCONNECT_MESSAGE:
                        connected = False
                        auxstring = "[NOTICE] " + username + " disconnected"
                        client.send(auxstring.encode(FORMAT))
                    else:
                        auxstring = "[Room " + room + "][" + username + "]: " + msg
                        client.send(auxstring.encode(FORMAT))
            if msg == DISCONNECT_MESSAGE:
                connected = False
                print("[DISCONNECTION] " + username + " (" + str(addr) + ") disconnected...")
                roomFound.remove(conn)
    conn.close()


if __name__ == "__main__":
    main()
