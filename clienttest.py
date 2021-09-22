import socket as s, sys, json
import threading as t

from config import info

client = s.socket()
client.connect( (info['addr'], info['port']) )
client.setblocking(0)

quit, user = False, {
	'id': None,
	'name': 'Anon'
}

def thread(func):
	def wrapper(*args, **kwargs):
		th = t.Thread(
			target=func,
			args=args,
			kwargs=kwargs)
		th.start()
		th.join()
	return wrapper

@thread
def message(client):
	global quit, id
	id = int(client.recv(1024).decode())
	
	while not quit:
		try:
# error
			data = json.loads(client.recv(1024).decode())
			if data['commands'] == ':exit':
				quit = False
			else:
				print(data['message'])
		except: pass

def run(client):
		global quit
		try:
			name = input('Name: ')
			
			user['name'] = name
			data = { 'id': user['id'], 'name': user['name'], 'message' : '', 'commands': '', 'system': '' }
			
			message(client)
			
			while not quit:
			   data['commands'] = ''
			   mess = input()
			   print(mess)
			   
			   if mess.find(':') == 0:
			   	data['commands'] = mess
			   	mess = ''
			   
			   data['message'] = mess
			   data = json.dumps(data)
			   print(data)
			   #client.send(data)
			   if data['commands'] == ':exit':
			   	quit = False
			   	
		except: pass
		client.close()

run(client)
sys.exit()
