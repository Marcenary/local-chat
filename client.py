import kivy, time, json
#===== new
import socket as s
import threading as t

#===== old
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.config import Config

Window.clearcolor = (0, .3, .5, .1)
Config.set('kivy', 'keyboard_mode', 'systemanddock')

Builder.load_string('''
<Auth>:
	nik: nik
	paswd: paswd
	lbl: warning
	
	BoxLayout:
		orientation: 'vertical'
		size_hint: .8, .7
		pos_hint: { 'center_x': .5, 'center_y': .5 }
		spacing: 15
		
		Label:
			text: 'Log In'
			pos_hint: { 'center_x': .5, 'center_y': .8 }
			font_size: 100
		
		Label:
			markup: True
			text: '[size=80]Name[/size]'
#			font_size: 80
		
		TextInput:
			id: nik
			size_hint: 1, None
			height: 125
			multiline: False
			hint_text: 'Enter login...'
			halign: 'center'
			valign: 'center'
			font_size: 80
			focus: True
		
		Label:
			text: 'Password'
			font_size: 80
		
		TextInput:
			id: paswd
			size_hint: 1, None
			height: 125
			multiline: False
			hint_text: 'Enter password...'
			halign: 'center'
			valign: 'center'
			password: True
			font_size: 80
		
		Label:
			id: warning
		Button:
			text: 'Log In'
			size_hint: .8, None
			height: 200
			pos_hint: {'center_x': .5}
			font_size: 70
			on_press: root.on_login()
		
<Menu>:
	BoxLayout:
		orientation: 'vertical'
		
		BoxLayout:
			size_hint: 1, .2
			Image:
				pos_hint: { 'center_y': .5, 'center_x': .5 } # ?
			Button:
				size_hint_x: .2
				text: 'Back'
				background_color: 0, .3, .5, .1
				on_press: root.manager.current = 'form'
		
		GridLayout:
			size_hint: 1, .8
			cols: 2
			
			Button:
				text: 'Settings'
				size_hint: .8, 1
				background_color: 0, .3, .5, .1
			Label:
				size_hint: .2, 1 # -
			Button:
				text: 'Settings'
				size_hint: .8, 1
				background_color: 0, .3, .5, .1
			Label:
			Button:
				text: 'Settings'
				size_hint: .8, 1
				background_color: 0, .3, .5, .1
			Label:
			Button:
				text: 'Settings'
				size_hint: .8, 1
				background_color: 0, .3, .5, .1
			Label:
			
<Form>:
	area: area
	data: data.text
	
	BoxLayout:
		orientation: 'vertical'
		
		BoxLayout:
			padding: 10
			spacing: 5
			size_hint: (1, .06)
			
			Button:
				text: 'Menu'
				background_color: 0, .3, .5, .1
				on_release: root.manager.current = 'menu'
		
			Label:
				text: app.nik
			
			Button:
				text: 'Exit' # future: свойства беседы
				background_color: 0, .3, .5, .1
				on_press: root.pressExit() # new screen
					
		BoxLayout:
			padding: 10
			size_hint: (1, .64)
		
			TextInput:
				id: area
				readonly: True
				multiline: True
						
		BoxLayout:
			#id: messages
			padding: 10
			spacing: 5
			size_hint: (1, .15)
					
			TextInput:
				id: data
				size_hint: (.7, 1)
				hint_text: 'Enter text'
						
			Button:
				text: "Send"
				size_hint: (.2, 1)
				on_press: root.pressed()
''')

#===== new
#info = json.load(open('serv_conf.json'))
#client = s.socket()
#client.connect( (info['addr'], info['port']) )
#client.setblocking(0)

def thread(func):
	def wrapper(*args, **kwargs):
		th = t.Thread(
			target=func,
			args=args,
			kwargs=kwargs)
		th.start()
	return wrapper

#===== old
class Menu(Screen):
	pass


class Auth(Screen):
	nik = ObjectProperty(None)
	paswd = ObjectProperty(None)
	def on_login(self):
		if self.nik.text != '' and self.paswd.text != '':
			# проверка пользователя(ответ от сервера)
			if self.nik == 'guest': pass
			
			app.nik = self.nik.text
			app.paswd = self.paswd.text
			self.lbl.text = app.nik
			self.manager.current = 'form'


class Form(Screen):
	area = ObjectProperty(None)
	data = ObjectProperty(None)
	
#===== new
	def __init__(self, name):
		super().__init__()
		
		self.name = name
		
		self.quit = False
		self.user = {
			'id': None,
			'name': app.nik,
			'commands': '',
			'system': ''
		}
		#self.user['id'] = int(client.recv(1024).decode())
		#self.on_message(client)
		
	@thread
	def on_message(self, client):
		while not self.quit:
			try:
				data = client.recv(1024).decode()
				
				data = json.loads(data)
				if data['commands'] == ':exit':
					self.quit = False #  возможна ошибка не выхода
				else:
					self.area.text += '<' + data['name'] + '>' + data['message']
			except: pass
			
	def pressed(self): # проблемы с отправкой или получением сервером
		try:
			text = f'{ self.data }\n'
			if text.find(':') == 0:
				if ':callback' in text:
					self.user['commands'] = text.split(' ', 1)[0] #======= проверить не проверялось ========#
					text = text.split(' ', 1)[1]
				else:
					self.user['commands'] = text
					if ':exit' in self.user['commands']:
						self.quit = True
			   
			self.user['message'] = text
			data = json.dumps(self.user).encode()
			client.send(data)
			#self.area.text += '[logging] message not send!\n'
			self.area.text += self.user['message']
			   	
		except Exception as e: self.area.text += str(e)
		client.close()
		return
	def pressExit(self):
		if not quit:
			self.user['commands'] = ':exit'
			self.user['message'] = ''
			self.quit = True
			
			client.send(json.dumps(self.user).encode())
		
		app.stop()

#===== old
class Main(App):
	def __init__(self):
		super().__init__()
		self.nik = 'guest'
		self.paswd = 'guest'
		self.host = '127.0.0.1'
		self.port = 8080
		
	def build(self):
		self.sm = ScreenManager()
		auth = Auth(name='auth')
		menu = Menu(name='menu')
		form = Form(name='form')
		
		self.sm.add_widget(auth)
		self.sm.add_widget(menu)
		self.sm.add_widget(form)
		
		return self.sm
		
if __name__ == '__main__':
	app = Main()
	app.run()