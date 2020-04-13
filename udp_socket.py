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

    seqNumber = 0
    ackFlag = '0'
    for i in range(0, len(chunks)):
      c = chunks[i]
      flags = ackFlag
      if(i == len(chunks) - 1):
        flags = flags + '1'
      else:
        flags = flags + '0'

      s = str(seqNumber)
      header = flags + s.zfill(3 - len(s) + 1)
      c = header + c
      c = str.encode(c)
      self.sock.sendto(c, server)
      seqNumber = (seqNumber + 1) % 1000

  def recvfrom(self, bufferSize):
    message = ''
    address = ''
    #need to change this limit
    while (len(message) < bufferSize):
      newData = self.sock.recvfrom(bufferSize)
      newMessage = newData[0].decode()
      ackFlag = int(newMessage[ : 1])
      lastFlag = int(newMessage[1 : 2])
      seqNumber = int(newMessage[2 : 5])
      if(ackFlag == 1):
        continue
      newMessage = newMessage[5: ]
      message = message + newMessage      
      if(lastFlag == 1):
        address = newData[1]
        break
    return (str.encode(message), address)


if __name__ == "__main__":
  pass
