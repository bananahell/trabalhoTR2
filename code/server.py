import socket
import threading
from utils import *


rooms = {}


def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    server.bind(ADDR)
    print(f"[LISTENING] Server is listening on {SERVER}")
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
                client.send(
                    f"        {username} connected".encode(FORMAT))
            roomFound.append(conn)
        else:
            newRoom = [conn]
            rooms[room] = newRoom
        thread = threading.Thread(
            target=handleClient, args=(conn, addr, room, username))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}\n")


def handleClient(conn, addr, room, username):
    print(f"[NEW CONNECTION] {username} connected to room {room}")
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
                        client.send(
                            f"        {username} disconnected".encode(FORMAT))
                    else:
                        client.send(
                            f"                [{username}]: {msg}".encode(FORMAT))
            if msg == DISCONNECT_MESSAGE:
                connected = False
                print(f"[DISCONNECTION] {username} ({addr}) disconnected...")
                roomFound.remove(conn)
    conn.close()


if __name__ == '__main__':
    main()
