import socket
from utils import *


def main():

    print("[STARTING] Client is starting...")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    send(client, "Hello World!")
    send(client, DISCONNECT_MESSAGE)


def send(client, msg):
    message = msg.encode(FORMAT)
    msgLength = len(message)
    sendLength = str(msgLength).encode(FORMAT)
    sendLength += b' ' * (HEADER-len(sendLength))
    client.send(sendLength)
    client.send(message)


if __name__ == '__main__':
    main()
