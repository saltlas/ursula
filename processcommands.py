import re
from websocketclient import WebSocketClient
from commands import putcommand
from datetime import timedelta

class CommandProcessor: #maybe make this cmdprocessorregex and make cmdprocessor the parent class
	"""Processor for transcripts of voice commands"""
	def __init__(self, init_time):
		self.init_time = init_time
		self.commands = {"put":putcommand.PutCommand} # maybe make a selectcommand for "that" type thing
		self.active_commands = []
		self.websocketclient = WebSocketClient()
		
	def process_commands(self, word):
		end_time = word.end_time / timedelta(milliseconds = 1)

		for command in self.commands.keys():
			if word.word == command:
				print(11111)
				cmd = self.commands[command](self.init_time)
				self.active_commands.append(cmd)

		if len(self.active_commands) > 0:
			for cmd in self.active_commands:
				if cmd.check_current_keyword(word.word):
					print(33333)
					msg = cmd.action(end_time)
					if msg:
						print(222222)
						self.websocketclient.send_message(msg)
					if cmd.finished:
						self.active_commands.remove(cmd)
				else:
					self.active_commands.remove(cmd)

	def close(self):
		self.websocketclient.close()



