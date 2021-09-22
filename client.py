import kivy, time

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.config import Config

Window.clearcolor = (0, .3, .5, .1)
#Window.softinput_mod = 'below_target'

Config.set('kivy', 'keyboard_mode', 'systemanddock')

Builder.load_string('''
<Auth>:
	nik: nik.text
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
				# имя чата или собеседика
			
			Button:
				text: 'Exit' # future: свойства беседы
				background_color: 0, .3, .5, .1
				on_press: app.stop() # new screen
					
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


class Menu(Screen):
	pass


class Auth(Screen):
	nik = ObjectProperty(None)
	paswd = ObjectProperty(None)
	def on_login(self):
		if self.nik != '' and self.paswd != '':
			# проверка пользователя(ответ от сервера)
			if self.nik == 'guest': pass
			
			app.nik = self.nik
			app.paswd = self.paswd
			self.manager.current = 'form'


class Form(Screen):
	area = ObjectProperty(None)
	data = ObjectProperty(None)
	def pressed(self):
		text = f'{ self.data }\n'
		self.area.text += text


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