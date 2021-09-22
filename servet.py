import socket as s, sys
import threading as t, json

from config import info

def thread(func):
	def wrapper(*args, **kwargs):
		new_thread = t.Thread(
			target=func,
			args=args,
			kwargs=kwargs)
		new_thread.start()
	return wrapper


class Socket:
	def __init__(self, info: dict) -> None:
		self.server = s.socket()
		self.server.bind( (info['addr'], info['port']) )
		self.users = []
		self.ids = 0
	
	def __del__(self):
		self.disconnect_all()
	
	def run(self) -> None:
		self.server.listen(info['users'])
		print( f"Server running on { info['addr'] }:{ info['port'] }.." )
		self.on_connect()
	
	def on_connect(self) -> None:
		print('Server wait a connect..')
		while 1:
			client, addr = self.server.accept()
			
			client.send( b'%d'%self.ids ) # отсылает пользователю его идентификатор
			
			if client not in self.users:
				self.users.append( [client, addr, self.ids] )
				self.ids += 1
				
			print(f'{ addr } was connect')
			self.on_message(client)
	
	def disconnect_all(self):
		try:
			if self.users != None:
				for i in self.users:
					i[0].send(b'close')
					i[0].close()
		except Exception as e: print(repr(e))
		sys.exit()
	
	@thread
	def on_message(self, client: s.socket) -> None:
		usr = [ i if i[0] == client else None for i in self.users ][0]
		while 1:
			try:
				data = client.recv(1024).decode()
				#data = json.loads(data)
				print(data)
				
				#if data['commands'] == ':callback':
#					data['commands'] = ''
#					data['message'] = '[ server ]' + data['message']
#					client.send(data + '\n' + json.dumps(data).encode())
#					
#				elif data['commands'] == ':exit':
#					print(f"{ usr[1] } was disconnect")
#					
#					client.send(json.dumps(data).encode())
#					client.close()
#					self.users.remove(usr)
#					
#					data['commands'] = ''
#					data['message'] = data['name'] + ' was disconnect'
#					
#					for user in self.users:
#						if user[0] != client:
#							user[0].send(json.dumps(data).encode())
#					return
#					
#				else:
#					for user in self.users:
#						if user[0] != client:
#							user[0].send(data)
#						# else: usr = user
#					
				data = data.decode()
				print(f"{ usr[1] } `{ data }`")
			except Exception as e:
				print(repr(e))
				self.disconnect_all()
	

if __name__ == '__main__':
	Socket(info).run()
	sys.exit()