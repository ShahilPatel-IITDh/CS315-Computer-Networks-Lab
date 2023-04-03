import socket
import threading
import time

HOST = '127.0.1.1'
PORT = 8000

class Manager:
	class Peer:
		def __init__(self, conn, addr):
			self.conn = conn
			self.addr = addr

	def __init__(self, host, port):
		# Setup socket
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind((host, port))
		self.timeout = 10
		self.active_peers = []


	def register_peer_in_list(self, peer):
		peer.conn.settimeout(10)
		threading.Lock().acquire()
		self.active_peers.append(peer)
		print(f'[INFO] New peer connected: {peer.addr}')
		threading.Lock().release()

		self.broadcast_peer_list()

	def broadcast_peer_list(self):
		threading.Lock().acquire()
		for peer in self.active_peers:
			l = ';'.join([f"{p.addr[0]},{p.addr[1]}" for p in self.active_peers])
			peer.conn.sendall(l.encode())
		threading.Lock().release()

	def delete_peer(self, peer):

		# Remove peer from active peers, lock the connection and close it
		threading.Lock().acquire()
		print(f'The following peer is disconnected: {peer.addr}')
		self.active_peers.remove(peer)
		threading.Lock().release()
		peer.conn.close()

		self.broadcast_peer_list()

	def handlePeer(self, peer):
		while True:
			try:
				data = peer.conn.recv(1024)
				if not data or data == b'CLOSE':
					self.delete_peer(peer)
					break
			except socket.timeout:
				print(f'Pinging {peer.addr}')
				peer.conn.sendall(b'PING')
				data = peer.conn.recv(1024)
				if not data == b'PONG':
					self.delete_peer(peer)
					break

	def handleConnections(self):
			while True:
				self.socket.listen()
				conn, addr = self.socket.accept()
				self.register_peer_in_list(self.Peer(conn, addr))
				threading.Thread(target=self.handlePeer, args=(self.active_peers[-1],), daemon=True).start()

	def run(self):
		try:
			self.handleConnections()
		except KeyboardInterrupt:
			print('Shutting down the Manager...')
			self.socket.close()

			for peer in self.active_peers.copy():
				peer.conn.close()
				self.active_peers.remove(peer)
			exit(0)

		except Exception as e:
			self.socket.close()
			for peer in self.active_peers.copy():
				peer.conn.close()
				self.active_peers.remove(peer)
			print(f'{e}')
			raise

if __name__ == '__main__':
	print('Starting Manager...')
	Manager(HOST, PORT).run()