from .command import Command
from jsonserializer import json_serial
import json

class RotateCommand(Command):
	def __init__(self, keywords, init_time, progress=0):
		super().__init__(keywords, init_time, progress)

	def serialize(self):
		for word in self.keywords:
			if word.isdigit():
				x = word
		event = {
			"rotateX": x,
			"rotateY": 0,
			"rotateZ": 0,
			"timestamps": self.times
		}
		return json.dumps(event, default=json_serial)


# not done - how to know what axis to rotate along?	