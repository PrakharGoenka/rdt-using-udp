import socket
import time
import hashlib


class Socket:
  packetSize = 1200
  windowSize = 7
  sequnceRange = 1000
  sequenceWidth = len(str(sequnceRange))
  flagWidth = 2
  headerWidth = flagWidth + sequenceWidth
  checksumWidth = 16
  segmentSize = headerWidth + packetSize + checksumWidth
  timeout = 1

  def __init__(self):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  def bind(self, addressPort):
    self.sock.bind(addressPort)
  
  def __makeChunks(self, data):
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
      header = flags + s.zfill(self.sequenceWidth)   
      header = header.encode()

      chunks[i] = header + chunks[i]
      checksum = hashlib.md5(chunks[i]).digest()
      chunks[i] += checksum 
      seqNumber = (seqNumber + 1) % self.sequnceRange
    
    return chunks


  def sendto(self, data, server):
    chunks = self.__makeChunks(data)    
    
    ack = [0] * self.windowSize
    sendTime = [0] * self.windowSize
    base = 0
    current = 0
    
    while(base < len(chunks)):
      while(current - base < self.windowSize and current < len(chunks)):
        self.sock.sendto(chunks[current], server)
        ack[current % self.windowSize] = 0
        sendTime[current % self.windowSize] = time.time()
        current += 1
      
      while(ack[base % self.windowSize] != 1):
        newData = None

        try:
          self.sock.settimeout(max([0, self.timeout - (time.time() - sendTime[base % self.windowSize])]))
          newData = self.sock.recvfrom(self.headerWidth)
        except socket.timeout:
          pass

        if(newData == None):
          prevIndex = (base - 1 + self.windowSize) % self.windowSize
          if(time.time() - sendTime[prevIndex] > 60):
            raise TimeoutError('No acks received for too long.')
          self.sock.sendto(chunks[base], server)
          sendTime[base % self.windowSize] = time.time() 
        else:
          newMessage = newData[0].decode()
          ackFlag = int(newMessage[ : 1])
          if(ackFlag == 0):
            continue    
          seqNumber = int(newMessage[self.flagWidth : self.flagWidth + self.sequenceWidth])
          if(seqNumber < base):    
            continue
          ack[seqNumber % self.windowSize] = 1
          

      base += 1
    self.sock.settimeout(None)
    return len(data)


  def recvfrom(self, bufferSize):
    windowSize = self.windowSize
    message = ''
    address = ''
    receiveWindow = [None] * windowSize
    base = 0    
    count = 0
    lastFlagU = 0
    
    while (len(message) < bufferSize):
      newData = self.sock.recvfrom(self.segmentSize) 
      newMessage = newData[0][ : -(self.checksumWidth)].decode()
      address = newData[1]
      ackFlag = int(newMessage[ : 1])
      lastFlag = int(newMessage[1 : 2])
      seqNumber = int(newMessage[self.flagWidth : self.flagWidth + self.sequenceWidth])
      checksum = newData[0][-(self.checksumWidth) : ]

      if(ackFlag == 1):
        continue
      
      checksumNew = hashlib.md5(newMessage.encode()).digest()
      if(checksumNew != checksum):
        continue
    
      if(seqNumber >= base - windowSize - 1 and seqNumber < base + windowSize):   # confirm this
        ack = '10' + str(seqNumber)
        ack = str.encode(ack)
        self.sock.sendto(ack, address)  

      if(seqNumber >= base and seqNumber < base + windowSize):
        newMessage = newMessage[self.headerWidth : ]
        if(receiveWindow[seqNumber - base] == None):
          count += 1
        receiveWindow[seqNumber - base] = newMessage
        
        lastFlagU = lastFlag or lastFlagU
        if(lastFlag == 1):
          windowSize = seqNumber - base + 1

        if(count == windowSize):
          for i in range(0, windowSize):
            message += receiveWindow[i]  
          receiveWindow = [None] * windowSize
          count = 0
          base += windowSize
          if(lastFlagU == 1):
            break
                  
    return (str.encode(message), address)


  def close(self):
    self.sock.close()


if __name__ == "__main__":
  pass
