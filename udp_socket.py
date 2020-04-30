import socket
import time
import hashlib


class Socket:
  packetSize = 3
  windowSize = 7
  sequnceRange = 1000
  sequenceWidth = len(str(sequnceRange))
  flagWidth = 2
  headerWidth = flagWidth + sequenceWidth
  checksumWidth = 16
  segmentSize = headerWidth + packetSize + checksumWidth
  # baseSequence = 0

  def __init__(self):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  def bind(self, addressPort):
    self.sock.bind(addressPort)
  
  def sendto(self, data, server):
    print('Sending')

    n = self.packetSize   
    chunks = [data[i : i + n] for i in range(0, len(data), n)]

    baseSequence = 0
    seqNumber = baseSequence

    for i in range(0, len(chunks)):  
      ackFlag = '0'
      lastFlag = '0'
      if(i == len(chunks) - 1):
        lastFlag = '1'
      flags = ackFlag + lastFlag

      s = str(seqNumber)
      header = flags + s.zfill(self.sequenceWidth)   # add padding for constant length of s
      header = header.encode()

      chunks[i] = header + chunks[i]
      print('chunk is:', chunks[i])
      checksum = hashlib.md5(chunks[i]).digest()
      chunks[i] += checksum 
      seqNumber = (seqNumber + 1) % self.sequnceRange
    
    ack = [0] * self.windowSize
    sendTime = [0] * self.windowSize
    base = 0
    current = 0
    self.sock.settimeout(1)
    while(base < len(chunks)):
      while(current - base < self.windowSize and current < len(chunks)):
        self.sock.sendto(chunks[current], server)
        ack[current % self.windowSize] = 0
        sendTime[current % self.windowSize] = time.time()
        current += 1
      
      while(ack[base % self.windowSize] != 1):
        newData = None

        try:
          newData = self.sock.recvfrom(self.headerWidth)
        except:
          pass

        if(newData == None):
          self.sock.sendto(chunks[base], server)
          sendTime[base % self.windowSize] = time.time() 
        else:
          newMessage = newData[0].decode()
          ackFlag = int(newMessage[ : 1])
          if(ackFlag == 0):
            continue    # manage this later
          seqNumber = int(newMessage[self.flagWidth : self.flagWidth + self.sequenceWidth])
          print('Ack:', seqNumber)
          if(seqNumber < base):    # check this thing
            continue
          ack[seqNumber % self.windowSize] = 1
          

      base += 1
    self.sock.settimeout(None)

  def recvfrom(self, bufferSize):
    print('Receiving')
    message = ''
    address = ''

    receiveWindow = [None] * self.windowSize
    base = 0    # todo: make base number universal
    count = 0
    lastFlagU = 0
    # need to change this limit. Critical area, decide acc to original protocol
    while (len(message) < bufferSize):
      newData = self.sock.recvfrom(self.segmentSize) # set it to the fixed packet size
      newMessage = newData[0][ : -(self.checksumWidth)].decode()
      address = newData[1]
      ackFlag = int(newMessage[ : 1])
      lastFlag = int(newMessage[1 : 2])
      seqNumber = int(newMessage[self.flagWidth : self.flagWidth + self.sequenceWidth])
      checksum = newData[0][-(self.checksumWidth) : ]

      # wont be receiving acks when receiving messages, coz only one side
      # speaks at a time
      if(ackFlag == 1):
        print('Ack received: ', newMessage.decode())
        continue
      
      checksumNew = hashlib.md5(newMessage.encode()).digest()
      if(checksumNew != checksum):
        print('Corrupted Packet Received')
        continue
    
      if(seqNumber >= base - self.windowSize - 1 and seqNumber < base + self.windowSize):   # confirm this
        ack = '10' + str(seqNumber)
        ack = str.encode(ack)
        self.sock.sendto(ack, address)  

      if(seqNumber >= base and seqNumber < base + self.windowSize):
        print('header = ', newMessage[ : self.headerWidth])
        newMessage = newMessage[self.headerWidth : ]
        
        if(receiveWindow[seqNumber - base] == None):
          count += 1
        receiveWindow[seqNumber - base] = newMessage
        
        lastFlagU = lastFlag or lastFlagU
        if(lastFlag == 1):
          self.windowSize = seqNumber - base + 1

        if(count == self.windowSize):
          for i in range(0, self.windowSize):
            message += receiveWindow[i]  
          receiveWindow = [None] * self.windowSize
          count = 0
          base += self.windowSize
          if(lastFlagU == 1):
            break
                  
    return (str.encode(message), address)


if __name__ == "__main__":
  pass
