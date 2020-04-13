import socket


class Socket:
  sock = ''

  def __init__(self):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  def bind(self, addressPort):
    self.sock.bind(addressPort)
  
  def sendto(self, data, server):
    data = data.decode()
    n = 3
    chunks = [data[i:i+n] for i in range(0, len(data), n)]
    for c in chunks:
      c = str.encode(c)
      self.sock.sendto(c, server)
    end = str.encode("d0ne")
    self.sock.sendto(end, server)

  def recvfrom(self, bufferSize):
    message = ''
    address = ''
    #need to change this limit
    while (len(message) < bufferSize):
      newData = self.sock.recvfrom(bufferSize)
      newMessage = newData[0].decode()
      if(newMessage == "d0ne"):
        address = newData[1]
        break
      message = message + newMessage      
    return (str.encode(message), address)


if __name__ == "__main__":
  pass
