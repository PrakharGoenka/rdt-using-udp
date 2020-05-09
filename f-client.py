import sys
from udp_socket import Socket


serv_addr = ('127.0.0.1', 4000)

sock = Socket()
BUFFER = 512

file_add = sys.argv[1]
file_name = file_add[(file_add.rfind('/')) + 1 : ]
sock.sendto(file_name.encode(), serv_addr)

with open(file_add) as f:
    data = f.read(BUFFER)
    print("sending file")
    while (data):
        sock.sendto(data.encode(), serv_addr)
        data = f.read(BUFFER)

sock.close()
