from .command import Command
from utils import jsonserializer
import json

class MoveCommand(Command):
	def __init__(self, keywords, init_time, progress=0):
		super().__init__(keywords, init_time, progress)

	def serialize(self):
		for word in self.keywords:
			if word.isdigit():
				x = word
		event = {
			"moveX": x,
			"moveY": 0,
			"moveZ": 0,
			"timestamps": self.times
		}
		return json.dumps(event, default=jsonserializer.json_serial)

