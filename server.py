from udp_socket import Socket


address = "localhost"
port = 3000
bufferSize  = 1024

server = Socket() 
server.bind((address, port))
print("UDP server up and listening")

while(True):
  bytesAddressPair = server.recvfrom(bufferSize)

  message = bytesAddressPair[0]
  address = bytesAddressPair[1]
  clientMsg = "Message from Client:{}".format(message)
  clientIP  = "Client IP Address:{}".format(address)    
  print(clientMsg)
  print(clientIP)

  msgFromServer = "Hello UDP Client"
  bytesToSend = str.encode(msgFromServer)

  server.sendto(bytesToSend, address)
