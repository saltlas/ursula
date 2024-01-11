import re
from websocketclient import WebSocketClient
from commands import putcommand
from utils import time_utils

class CommandProcessor: #maybe make this cmdprocessorregex and make cmdprocessor the parent class
	"""Processor for transcripts of voice commands"""
	def __init__(self, init_time):
		self.init_time = init_time
		self.commands = {"put":putcommand.PutCommand} # maybe make a selectcommand for "that" type thing
		self.active_commands = []
		self.websocketclient = WebSocketClient()
		print("client not blocking")
		
	def process_commands(self, word):
		end_time = time_utils.convert_timedelta_to_milliseconds(word.end_time) 

		for command in self.commands.keys():
			if word.word == command:
				cmd = self.commands[command]()
				self.active_commands.append(cmd)

		if len(self.active_commands) > 0:
			for cmd in self.active_commands:
				if cmd.check_current_keyword(word.word):
					timestamp = time_utils.add_offset(end_time, self.init_time)
					msg = cmd.action(timestamp)
					if msg:
						self.websocketclient.send_message(msg)
					if cmd.finished:
						self.active_commands.remove(cmd)
				else:
					self.active_commands.remove(cmd)

	def close(self):
		self.websocketclient.close()



