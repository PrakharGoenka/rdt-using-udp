import socket
import time


class Socket:
  sock = ''

  def __init__(self):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  def bind(self, addressPort):
    self.sock.bind(addressPort)
  
  def sendto(self, data, server):
    print('Sending')
    data = data.decode()

    n = 3   
    chunks = [data[i:i+n] for i in range(0, len(data), n)]

    baseSequence = 0
    seqNumber = baseSequence

    for i in range(0, len(chunks)):   
      c = chunks[i]

      ackFlag = '0'
      lastFlag = '0'
      if(i == len(chunks) - 1):
        lastFlag = '1'

      flags = ackFlag + lastFlag

      s = str(seqNumber)
      header = flags + s.zfill(3)   # add padding for constant length of s
      c = header + c
      c = str.encode(c)
      chunks[i] = c
      seqNumber = (seqNumber + 1) % 1000
    
    windowSize = 7
    ack = [0] * windowSize
    sendTime = [0] * windowSize
    base = 0
    current = 0
    self.sock.settimeout(1)
    while(base < len(chunks)):
      while(current - base < windowSize and current < len(chunks)):
        self.sock.sendto(chunks[current], server)
        ack[current % windowSize] = 0
        sendTime[current % windowSize] = time.time()
        current += 1
      
      while(ack[base % windowSize] != 1):
        newData = None

        try:
          newData = self.sock.recvfrom(5)
        except:
          pass

        if(newData == None):
          self.sock.sendto(chunks[base], server)
          sendTime[base % windowSize] = time.time() 
        else:
          newMessage = newData[0].decode()
          ackFlag = int(newMessage[ : 1])
          if(ackFlag == 0):
            continue    # manage this later
          seqNumber = int(newMessage[2 : 5])
          print('Ack:', seqNumber)
          if(seqNumber < base):    # check this thing
            continue
          ack[seqNumber % windowSize] = 1
          

      base += 1
    self.sock.settimeout(None)

  def recvfrom(self, bufferSize):
    print('Receiving')
    message = ''
    address = ''
    sendAck = [0] * 1024
    # need to change this limit. Critical area, decide acc to original protocol
    while (len(message) < bufferSize):
      newData = self.sock.recvfrom(bufferSize)
      newMessage = newData[0].decode()
      address = newData[1]
      ackFlag = int(newMessage[ : 1])
      lastFlag = int(newMessage[1 : 2])
      seqNumber = int(newMessage[2 : 5])

      # wont be receiving acks when receiving messages, coz only one side
      # speaks at a time
      if(ackFlag == 1):
        print('Ack received: ', newMessage)
        continue
      
      if(sendAck[seqNumber] == 0):
        sendAck[seqNumber] = 1
        print('packet with seq no. {} dropped!!'.format(seqNumber))
      else:
        ack = '10' + newMessage[2 : 5]
        ack = str.encode(ack)
        self.sock.sendto(ack, address)   
        print('header = ', newMessage[ : 5])
        newMessage = newMessage[5: ]
        message = message + newMessage      
        if(lastFlag == 1):
          break
    print('header = ', newMessage[ : 5])         
    return (str.encode(message), address)


if __name__ == "__main__":
  pass
