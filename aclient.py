import socket
import sys


serv_addr = ('127.0.0.1', 4000)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
BUFFER = 512

file_name = sys.argv[1]
sock.sendto(file_name.encode('utf-8'), serv_addr)

with open(file_name) as f:
    data = f.read(BUFFER)

    while (data):
        if (sock.sendto(data.encode('utf-8'), serv_addr)):
            print("sending file")
            data = f.read(BUFFER)

    sock.close()
