import re
from websocketclient import WebSocketClient
from commands import rotatecommand, selectcommand, deselectcommand, scalecommand

class CommandProcessor: 
	"""Processor for transcripts of voice commands"""
	def __init__(self, init_time):
		self.init_time = init_time
		self.commands = {"rotate":rotatecommand.RotateCommand, "select":selectcommand.SelectCommand, "deselect":deselectcommand.DeselectCommand, "scale":scalecommand.ScaleCommand} # maybe make a selectcommand for "that" type thing
		self.active_command = None
		self.websocketclient = WebSocketClient()
		print("client not blocking")


	def process_commands(self, word_str, time):
		if word_str in self.commands.keys():
			if not(self.active_command != None and self.active_command.check_current_keyword(word_str)):
				cmd = self.commands[word_str]()
				self.active_command = cmd

		if self.active_command != None:
			cmd = self.active_command
			if cmd.check_current_keyword(word_str):
				msg = cmd.action(time, word_str)
				if msg:
					print(self.active_command)
					self.websocketclient.send_message(msg)
				if cmd.finished:
					self.active_command = None
			else:
				self.active_command = None




	def close(self):
		self.websocketclient.close()



