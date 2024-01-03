import re
from websocketclient import WebSocketClient
from commands import movecommand, rotatecommand

class CommandProcessor: #maybe make this cmdprocessorregex and make cmdprocessor the parent class
	"""Processor for transcripts of voice commands"""
	def __init__(self, init_time):
		self.init_time = init_time
		self.commands = {r'rotate\s+(\d+)\s+degrees':rotatecommand.RotateCommand, r'move\s+(\d+)':movecommand.MoveCommand} # change - maybe to dict w functions as vals?
		self.websocketclient = WebSocketClient()
		
	def process_commands(self, transcript, words):
		for command in self.commands.keys():
			for match in re.finditer(command, transcript):
				keywords = transcript[match.start():match.end() + 1].split()
				cmd = self.commands[command](keywords, self.init_time)
				for word_info in words:
					word = word_info.word
					end_time = word_info.end_time.seconds
					if word == cmd.current_keyword and not cmd.finished:
						cmd.action(end_time)
					elif word != cmd.current_keyword and not cmd.finished:
						cmd.reset()
				if cmd.finished:
					self.websocketclient.send_message(cmd.serialize())
					cmd.reset()

	def close(self):
		self.websocketclient.close()