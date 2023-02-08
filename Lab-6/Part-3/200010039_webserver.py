
# To run: python 200010039_webserver.py
# In browser: http://<ip_address>:3600/HelloWorld.html

# Import socket module
import socket

# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)
serverPort = 3600
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Prepare a sever socket
#Fill in start
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print ('The web server is up on port: ', serverPort)
#Fill in end

while True:
	#Establish the connection

	print ('Ready to serve...')

	# Set up a new connection from the client
	 # Return a new socket representing the connection, and the address of the client. The socket is usable like a regular socket object, e.g. you can call its send() and recv() methods. The address is a pair (hostaddr, port) for IPv4, where hostaddr is a string representing the IPv4 address and port is an integer.
	connectionSocket, addr = serverSocket.accept() #Fill in start   #Fill in end

	try:

		message = connectionSocket.recv(1024)  #Fill in start #Fill in end

		filename = message.split()[1]
		
		inputFile = open(filename[1:])

		outputdata =inputFile.read() #Fill in start #Fill in end
		print (outputdata)
		#Send one HTTP header line into socket
		#Fill in start
		# If the file is found, send the file to the client
		connectionSocket.send('\nHTTP/1.1 200 OK\n\n\n'.encode())
		#Fill in end

		# Send the content of the requested file to the connection socket
		for i in range(0, len(outputdata)):
			# send one encoded byte at a time
			connectionSocket.send(outputdata[i].encode())

		connectionSocket.send("\r\n".encode())
		# Close the client connection socket	
		connectionSocket.close()

	# Error handling for file not found in server
	except IOError:
		# Send HTTP response message for file not found
		#Fill in start
		connectionSocket.send("\nHTTP/1.1 404 Not Found\n\n\n".encode())
		#Fill in end
		# Close the client connection socket
                #Fill in start
		connectionSocket.close()
		#Fill in end
serverSocket.close()