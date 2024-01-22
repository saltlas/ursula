import re
from websocketclient import WebSocketClient
from commands import rotatecommand, selectcommand, deselectcommand, scalecommand

class CommandProcessor: 
	"""Processor for transcripts of voice commands.
	Receives strings representing voice input, matches them to command keywords
	and sends relevant messages to websocket connection."""

	def __init__(self, init_time):
		self.init_time = init_time

		# first keyword in each command to match to the Command object containing relevant command logic
		self.commands = {
			"rotate":rotatecommand.RotateCommand,
			"select":selectcommand.SelectCommand,
			"deselect":deselectcommand.DeselectCommand,
			"scale":scalecommand.ScaleCommand
		} 

		self.active_command = None # only one active command at a time

		# initializing websocket connection
		self.websocketclient = WebSocketClient()
		print("client not blocking") # debug


	def process_commands(self, word_str, time):
		"""on reception of a string representing a word, and a timestamp,
		pass it to the relevant Command object it belongs to"""

		# checking if it's the first word in a new command
		if word_str in self.commands.keys():
			# if it's also the next keyword of a command we've been processing already, we want to stay on the current command rather than switching.
			if not(self.active_command != None and self.active_command.check_current_keyword(word_str)):

				# initialize Command object
				cmd = self.commands[word_str]()
				self.active_command = cmd


		if self.active_command != None:
			cmd = self.active_command
			if cmd.check_current_keyword(word_str):

				# if command-specific logic for this keyword returns a message, we send it through websocket connection
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



