from socket import *
import ssl
from ssl import SSLContext
import base64 as b64


msg = "\r\n I love computer networks!"

endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailServer = "smtp.gmail.com"

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((mailServer, 587))  # using port 587 for secure SMTP connection

recv = clientSocket.recv(1024).decode()
print(recv)

if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
encodedHelo = heloCommand.encode()
clientSocket.send(encodedHelo)

recv1 = clientSocket.recv(1024).decode()
print(recv1)

if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send STARTTLS command to initiate secure connection

startTTLsCommand = "STARTTLS\r\n"

encodedCommand = startTTLsCommand.encode()
clientSocket.send(encodedCommand)

recv2 = clientSocket.recv(1024).decode()
print(recv2)

if recv2[:3] != '220':
    print('220 reply not received from server.')

# Initiating secure connection
clientSocket = ssl.wrap_socket(clientSocket)

# Send AUTH LOGIN command to authenticate user
authCommand = "AUTH LOGIN\r\n"
encodedAuth = authCommand.encode()
clientSocket.send(encodedAuth)

recv3 = clientSocket.recv(1024).decode()
print(recv3)

if recv3[:3] != '334':
    print('334 reply not received from server.')

# Send username and password encoded in base64

username = "smtplab23@gmail.com"
password = " lmvgusmmhxkmzoti"

username64bits = b64.b64encode(username.encode())
password64bits = b64.b64encode(password.encode())

clientSocket.send(username64bits)
clientSocket.send("\r\n".encode())

clientSocket.send(password64bits)
clientSocket.send("\r\n".encode())

recv4 = clientSocket.recv(1024).decode()
print(recv4)

if recv4[:3] != '235':
    print('235 reply not received from server.')

# Send MAIL FROM command and print server response.
mailFromCommand = "MAIL FROM:<smtplab23@gmail.com>\r\n"
encodedMailFrom = mailFromCommand.encode()
clientSocket.send(encodedMailFrom)

recv5 = clientSocket.recv(1024).decode()
print(recv5)

if recv5[:3] != '250':
    print('555 250 reply not received from server.')


# Send RCPT TO command and print server response.
rcptToCommand = "RCPT TO:<shahilpatel809@gmail.com>\r\n"
encodedRCPT = rcptToCommand.encode()
clientSocket.send(encodedRCPT)

recv6 = clientSocket.recv(1024).decode()
print(recv6)

if recv6[:3] != '250':
    print('556 250 reply not received from server.')

# Send DATA command and print server response.
dataString = "DATA\r\n"
encodedDataString = dataString.encode()
clientSocket.send(encodedDataString)

recv7 = clientSocket.recv(1024).decode()
print(recv7)

if recv7[:3] != '354':
    print('354 reply not received from server.')

# Send message data.
encodedMSG = msg.encode()
clientSocket.send(encodedMSG)

# Message ends with a single period.
encodedEndMSG = endmsg.encode()
clientSocket.send(encodedEndMSG)

recv8 = clientSocket.recv(1024).decode()
print(recv8)

if recv8[:3] != '354':
    print('8 354 reply not received from server.')

# Send QUIT command and get server response.
quitCommand = "QUIT\r\n"
encodedQUITCommand = quitCommand.encode()
clientSocket.send(encodedQUITCommand)

recv9 = clientSocket.recv(1024).decode()
print(recv9)
if recv[:3] != '221':
    print('221 reply not received from server.')

# close the socket
clientSocket.close()