from udp_socket import Socket

client = Socket()

msgFromClient = "Hello UDP Server"
bytesToSend = str.encode(msgFromClient)
serverAddressPort = ("localhost", 3000)
client.sendto(bytesToSend, serverAddressPort)

bufferSize = 1024

msgFromServer = client.recvfrom(bufferSize)
msgFromServer = msgFromServer[0].decode()
msg = "Message from Server: {}".format(msgFromServer)
print(msg)
