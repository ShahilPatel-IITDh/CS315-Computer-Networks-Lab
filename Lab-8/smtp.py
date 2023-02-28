from socket import *
import base64
import time

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it

mailserver = ("smtplab23@gmail.com", 25)


# Create socket called clientSocket and establish a TCP connection with mailserver
#Fill in start
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(mailserver)
#Fill in end

recv = clientSocket.recv(1024).decode()
print(recv)

if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())

recv1 = clientSocket.recv(1024).decode()
print(recv1)

if recv1[:3] != '250':
    print('250 reply not received from server.')

# Username and password
Username = "smtplab23@gmail.com"
Password = "lmvgusmmhxkmzoti"

base64_str = ("\x00" + Username + "\x00" + password).encode()
base64_str = base64.b64encode(base64_str)

authMsg = "AUTH PLAIN ".encode()+base64_str+"\r\n".encode()

clientSocket.send(authMsg)
recv_auth = clientSocket.recv(1024)

print(recv_auth.decode())

mailFrom = "MAIL FROM:<xxxxxxxx>\r\n"
clientSocket.send(mailFrom.encode())

recv2 = clientSocket.recv(1024).decode()

print("After MAIL FROM command: "+recv2)

rcptTo = "RCPT TO:<xxxxxxxxxx>\r\n"
clientSocket.send(rcptTo.encode())

recv3 = clientSocket.recv(1024).decode()

print("After RCPT TO command: "+recv3)
data = "DATA\r\n"

clientSocket.send(data.encode())

recv4 = clientSocket.recv(1024).decode()

print("After DATA command: "+recv4)
subject = "Subject: testing my client\r\n\r\n"

clientSocket.send(subject.encode())

date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
date = date + "\r\n\r\n"

clientSocket.send(date.encode())
clientSocket.send(msg.encode())
clientSocket.send(endmsg.encode())

recv_msg = clientSocket.recv(1024).decode()
print("Response after sending message body:"+recv_msg)

quit = "QUIT\r\n"

clientSocket.send(quit.encode())

recv5 = clientSocket.recv(1024).decode()
print(recv5.)
clientSocket.close()
