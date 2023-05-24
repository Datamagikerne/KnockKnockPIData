# To test proxy without PI
from socket import *

port = 12100
s = socket(AF_INET, SOCK_DGRAM)
s.bind(('', port))

while True:
    response, server_address = s.recvfrom(65507)
    decoded = response.decode()
    print(decoded)


