#import socket module
import socket

serverPort=6789
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Prepare a sever socket
# Fill in start
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

print ('The web server is up on port: ',serverPort)

# Fill in end
while True:

   # Establish the connection
   print ('Ready to serve...')

   # Return a new socket representing the connection, and the address of the client. The socket is usable like a regular socket object, e.g. you can call its send() and recv() methods. The address is a pair (hostaddr, port) for IPv4, where hostaddr is a string representing the IPv4 address and port is an integer.
   connectionSocket, address = serverSocket.accept()

   try:
      message = connectionSocket.recv(1024)
      print (message,'::',message.split()[0],':',message.split()[1])
      filename = message.split()[1]
      print (filename,'||',filename[1:])
      inputFile = open(filename[1:])
      outputdata = inputFile.read()
      print (outputdata)

      # Send one HTTP header line into socket
      # Fill in start
      connectionSocket.send('\nHTTP/1.1 200 OK\n\n')
      connectionSocket.send(outputdata)
      
      # Fill in end
      # Send the content of the requested file to the client

      for i in range(0, len(outputdata)):
         connectionSocket.send(outputdata[i])
         
      connectionSocket.close()
   except IOError:

   # Send response message for file not found
   # Fill in start
      connectionSocket.send('\nHTTP/1.1 404 Not Found\n\n')
      connectionSocket.send('\nHTTP/1.1 404 Not Found\n\n')