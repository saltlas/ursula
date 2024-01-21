import uuid
from utils import jsonserializer, wildcards
import json

class Command:
	"""a command class"""
	def __init__(self, keywords, progress=0):
		self.keywords = keywords
		if len(keywords) < 1:
			raise ValueError("Keywords list is empty!")
		self.num_keywords = len(keywords)
		self.progress = progress
		self.current_keyword = keywords[progress]
		self.finished = False
		self.times = {}
		self.session_id = str(uuid.uuid4())

	def action(self, timestamp, keyword):
		keyword_index = self.progress
		print("action", keyword_index)

		if keyword_index != self.num_keywords - 1:
			self.update_next_keyword()
		else:
			self.finish()

		event = {
				"session_id": self.session_id,
				"phrase": keyword,
				"timestamp": timestamp
			}
		return json.dumps(event, default=jsonserializer.json_serial)		


	def finish(self):
		self.finished = True

	def update_next_keyword(self):
		if self.finished:
			return False
		else:
			self.progress += 1
			self.current_keyword = self.keywords[self.progress]

	def reset(self):
		self.progress = 0
		self.current_keyword = self.keywords[0]
		self.finished = False

	def check_current_keyword(self, keyword):
		if self.current_keyword in wildcards.wildcardsdict:
			print(1)
			return keyword in wildcards.wildcardsdict[self.current_keyword]

		else:
			print(2)
			return self.current_keyword == keyword


