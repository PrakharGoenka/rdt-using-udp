from udp_socket import Socket

host = "127.0.0.1"
port = 4000

addr = (host, port)

sock = Socket()
sock.bind(addr)
print("listening")

BUFFER = 512

file_name, addr = sock.recvfrom(BUFFER)
file_name = file_name.decode().strip()

target = '/received/'
file_name = target + file_name
print("writing to " + file_name)

with open(file_name, 'a') as f:
    data, addr = sock.recvfrom(BUFFER)
    try:    
        f.write(data.decode())
        data, addr = sock.recvfrom(BUFFER)
    except EnvironmentError as err:
        print(err)
        
    