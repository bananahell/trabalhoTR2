import socket
import threading
import utils as utils


rooms = {}


def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    server.bind(utils.ADDR)
    print(f"[LISTENING] Server is listening on {utils.SERVER}")
    while True:
        server.listen(20)
        conn, addr = server.accept()
        username = ""
        room = 0
        msgLength = conn.recv(utils.HEADER).decode(utils.FORMAT)
        if msgLength:
            msgLength = int(msgLength)
            username = conn.recv(msgLength).decode(utils.FORMAT)
            msgLength = int(conn.recv(utils.HEADER).decode(utils.FORMAT))
            room = conn.recv(msgLength).decode(utils.FORMAT)
        roomFound = rooms.get(room)
        if roomFound:
            for client in roomFound:
                client.send(f"[Notice]: {username} connected".encode(utils.FORMAT))
            roomFound.append(conn)
        else:
            newRoom = [conn]
            rooms[room] = newRoom
        thread = threading.Thread(
            target=handleClient, args=(conn, addr, room, username)
        )
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}\n")


def handleClient(conn, addr, room, username):
    print(f"[NEW CONNECTION] {username} connected to room {room}")
    connected = True
    while connected:
        msgLength = conn.recv(utils.HEADER).decode(utils.FORMAT)
        if msgLength:
            msgLength = int(msgLength)
            msg = conn.recv(msgLength).decode(utils.FORMAT)
            roomFound = rooms.get(room)
            for client in roomFound:
                if client != conn:
                    if msg == utils.DISCONNECT_MESSAGE:
                        connected = False
                        client.send(
                            f"[Notice]: {username} disconnected".encode(utils.FORMAT)
                        )
                    else:
                        client.send(
                            f"   [Room {room}][{username}]: {msg}".encode(utils.FORMAT)
                        )
            if msg == utils.DISCONNECT_MESSAGE:
                connected = False
                print(f"[DISCONNECTION] {username} ({addr}) disconnected...")
                roomFound.remove(conn)
    conn.close()


if __name__ == "__main__":
    main()
