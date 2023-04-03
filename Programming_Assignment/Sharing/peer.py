import socket
import threading

HOST = '127.0.1.1'
PORT = 8000

class Peer:
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def handle_manager(self):
		name = input('Enter peer name: ')
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
			# print the active peers list here

	def run(self):
		try:
			self.socket.connect((self.host, self.port))
			self.handle_manager()

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