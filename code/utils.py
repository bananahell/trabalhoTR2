import socket
import urllib.request


HEADER = 12
PORT = 5050
# para IPv4 AF_INET
# SERVER = socket.gethostbyname(socket.gethostname())
# para IPv6 AF_INET6
SERVER = urllib.request.urlopen('https://ident.me').read().decode('utf8')
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'quit'
