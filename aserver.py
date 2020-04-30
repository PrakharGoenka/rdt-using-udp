import socket

host = "127.0.0.1"
port = 4000

addr = (host, port)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(addr)
print("listening")

BUFFER = 512

data, addr = sock.recvfrom(BUFFER)
data = data.strip()
print(data.decode())
with open(data.decode()) as f:
    data, addr = sock.recvfrom(BUFFER)
    try:
        while (data):
            # f.write(data.decode())
            print(data.decode())
            data, addr = s.recvfrom(buf)
    except:
        pass
    sock.close()
    print("out")
