from .command import Command
from utils import jsonserializer, wildcards, time_utils
import json

class PutCommand(Command):
	def __init__(self, progress=0):
		super().__init__(["put", "select_word", "move_word"], progress)
		self.time = None

	def action(self, offset):
		keyword_index = self.progress



		if keyword_index != self.num_keywords - 1:
			self.update_next_keyword()
		else:
			self.finish()


		if keyword_index == 1:
			timestamp =  time_utils.add_offset(offset, self.init_time)

			event = {
				"command": "select",
				"timestamp": timestamp
			}
			return json.dumps(event, default=jsonserializer.json_serial)

		if keyword_index == 2:
			timestamp =  time_utils.add_offset(offset, self.init_time)

			event = {
				"command": "move",
				"timestamp": timestamp
			}
			return json.dumps(event, default=jsonserializer.json_serial)

	def finish(self):
		self.finished = True

	def serialize(self):
		for word in self.keywords:
			if word.isdigit():
				x = word
		event = {
			"putX": x,
			"putY": 0,
			"putZ": 0,
			"timestamp": self.times
		}
		return json.dumps(event, default=jsonserializer.json_serial)

	def check_current_keyword(self, keyword):
		if self.current_keyword in wildcards.wildcardsdict:
			return keyword in wildcards.wildcardsdict[self.current_keyword]

		else:
			return self.current_keyword == keyword