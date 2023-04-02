import socket
import threading

HOST = '127.0.0.1'
PORT = 65345

class Peer:
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def handleManager(self):
		while True:
			data = self.socket.recv(1024)
			if not data:
				raise Exception('Manager disconnected!')
			
			if data == b'PING':
				print('Pong!')
				self.socket.sendall(b'PONG')
				continue
			
			print('Received peer update!')
			self.peers = [(p.split(",")[0], p.split(",")[1]) for p in data.decode().split(';')]

	def run(self):
		try:
			self.socket.connect((self.host, self.port))
			self.handleManager()

		except KeyboardInterrupt:
			self.socket.sendall(b'CLOSE')
			self.socket.close()
			print('Shutting down...')
			exit(0)

		except Exception as exp:
			self.socket.sendall(b'CLOSE')
			self.socket.close()
			print(f'[ERROR] {exp}')
			raise

if __name__ == '__main__':
	Peer(HOST, PORT).run()