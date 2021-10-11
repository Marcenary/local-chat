import socket as s
import sys, json
import threading as t

info = json.load(open('serv_conf.json'))
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
	return wrapper

@thread
def message(client):
	global quit
	
	while not quit:
		try:
			data = client.recv(1024).decode()
			
			data = json.loads(data)
			if data['commands'] == ':exit':
				quit = False #  возможна ошибка не выхода
			else:
				print(data['message'])
		except: pass

def run(client):
		global quit
		try:
			user['name'] = input('Name: ')
			user['id'] = int(client.recv(1024).decode())
			
			user['system'] = ''
			
			message(client)
			
			while not quit:
			   user['commands'] = ''
			   mess = input('> ')
			   
			   if mess.find(':') == 0:
			   	if ':callback' in mess:
			   		user['commands'] = mess.split(' ', 1)[0]
			   		mess = mess.split(' ', 1)[1]
			   	else:
			   		user['commands'] = mess
			   		if user['commands'] == ':exit':
			   			quit = True
			   
			   user['message'] = mess
			   data = json.dumps(user).encode()
			   client.send(data)
			   print(user['message'])
			   	
		except Exception as e: print('\n\n' + str(e) + '\n\n')
		client.close()
		return

run(client)