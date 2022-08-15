import socket
import urllib.request


HEADER = 12
PORT = 5050
ADDRESS_FAMILY = 0
IPV6 = False
if (IPV6 == False):
  # para IPv4 AF_INET
  ADDRESS_FAMILY = socket.AF_INET
  SERVER = socket.gethostbyname(socket.gethostname())
else:
  # para IPv6 AF_INET6
  ADDRESS_FAMILY = socket.AF_INET6
  SERVER = urllib.request.urlopen('https://ident.me').read().decode('utf8')
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'quit'
