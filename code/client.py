# from inspect import isclass
import socket
import threading
import utils as utils


client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
connected = True


def main():
    print("[STARTING] Client is starting...")

    client.connect(utils.ADDR)

    global username
    global room
    username = input("Input your username: ")
    room = input("Choose a room to join: ")

    message = username.encode(utils.FORMAT)
    usernameLength = len(message)
    sendLength = str(usernameLength).encode(utils.FORMAT)
    sendLength += b" " * (utils.HEADER - len(sendLength))

    client.send(sendLength)
    client.send(message)

    message = room.encode(utils.FORMAT)
    roomLength = len(message)
    sendLength = str(roomLength).encode(utils.FORMAT)
    sendLength += b" " * (utils.HEADER - len(sendLength))

    client.send(sendLength)
    client.send(message)

    listener = threading.Thread(target=listen)
    sender = threading.Thread(target=send)
    listener.start()
    sender.start()


def listen():
    global connected
    while connected:
        print(client.recv(2048).decode(utils.FORMAT).strip())


def send():
    global connected
    while connected:
        msg = input()
        if msg == utils.DISCONNECT_MESSAGE:
            connected = False
        message = msg.encode(utils.FORMAT)
        msgLength = len(message)
        sendLength = str(msgLength).encode(utils.FORMAT)
        sendLength += b" " * (utils.HEADER - len(sendLength))
        client.send(sendLength)
        client.send(message)
        if connected:
            print("\033[A", end="")  # move the cursor up a line
            print("\033[K", end="")  # erase the line
            print(f"[Room {room}][{username}]: " + msg)


if __name__ == "__main__":
    main()
