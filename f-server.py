import sys
from udp_socket import Socket

host = "127.0.0.1"
port = 4000

addr = (host, port)

sock = Socket()
sock.bind(addr)
print("listening")

BUFFER = 10000

file_name, addr = sock.recvfrom(BUFFER)
file_name = file_name.decode().strip()

target = sys.argv[1]
file_name = target + file_name
print("writing to " + file_name)

with open(file_name, 'w') as f:
    data, addr = sock.recvfrom(BUFFER)
    try: 
        f.write(data.decode())
    except EnvironmentError as err:
        print(err)
        
sock.close()
    