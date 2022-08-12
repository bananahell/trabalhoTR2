from inspect import isclass
import socket
import threading
from utils import *


client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
connected = True


def main():
    print("[STARTING] Client is starting...")
    client.connect(ADDR)
    username = input('Input your username: ')
    room = input('Choose a room to join: ')
    print(f"\nRoom {room}\n")
    message = username.encode(FORMAT)
    usernameLength = len(message)
    sendLength = str(usernameLength).encode(FORMAT)
    sendLength += b' ' * (HEADER-len(sendLength))
    client.send(sendLength)
    client.send(message)
    message = room.encode(FORMAT)
    roomLength = len(message)
    sendLength = str(roomLength).encode(FORMAT)
    sendLength += b' ' * (HEADER-len(sendLength))
    client.send(sendLength)
    client.send(message)
    listener = threading.Thread(target=listen)
    sender = threading.Thread(target=send)
    listener.start()
    sender.start()


def listen():
    global connected
    while connected:
        print(client.recv(2048).decode(FORMAT))


def send():
    global connected
    while connected:
        msg = input()
        if (msg == DISCONNECT_MESSAGE):
            connected = False
        message = msg.encode(FORMAT)
        msgLength = len(message)
        sendLength = str(msgLength).encode(FORMAT)
        sendLength += b' ' * (HEADER-len(sendLength))
        client.send(sendLength)
        client.send(message)


if __name__ == '__main__':
    main()
