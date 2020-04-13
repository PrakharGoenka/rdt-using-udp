import socket


class Socket:
  sock = ''

  def __init__(self):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  def bind(self, addressPort):
    self.sock.bind(addressPort)
  
  def sendto(self, data, server):
    self.sock.sendto(data, server)

  def recvfrom(self, bufferSize):
    return self.sock.recvfrom(bufferSize)


if __name__ == "__main__":
  pass
