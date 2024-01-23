import uuid
from utils import serializer, wildcards

class Command:
	"""Base class for all commands dictating default logic. 
	commands extend this class for customisability of behaviour."""

	def __init__(self, keywords, progress=0):

		# there are a few fields here that are useless in current implementation, like times and passing progress as an argument, but may be useful for later implementations

		self.keywords = keywords
		if len(keywords) < 1:
			raise ValueError("Keywords list is empty!")
		self.num_keywords = len(keywords)
		self.progress = progress
		self.current_keyword = keywords[progress]
		self.finished = False
		self.times = {}

		# generate unique session ID at command beginning using UUID 4
		self.session_id = str(uuid.uuid4())

	def action(self, timestamp, keyword):
		"""action to take based on keyword spoken. 
		not relevant to current implementation
		but in some cases could specifically send 
		certain things depending on keyword index"""

		keyword_index = self.progress
		print("action", keyword_index)

		# if this isn't the final keyword, move the next expected keyword to be the keyword that comes after the one passed
		if keyword_index != self.num_keywords - 1:
			self.update_next_keyword()
		else:
			self.finish()

		# data to send to input manager, json serialized
		event = {
				"session_id": self.session_id,
				"phrase": keyword,
				"timestamp": timestamp
			}
		return self.serialize(event)	


	def finish(self):
		self.finished = True

	def update_next_keyword(self):
		"""moves forward one keyword in the command"""
		# return values not used in current implementation
		if self.finished:
			return False
		else:
			self.progress += 1
			self.current_keyword = self.keywords[self.progress]
			return True


	def check_current_keyword(self, keyword):
		"""checks if 'keyword' matches the current expected keyword, returns true or false"""
		if self.current_keyword in wildcards.wildcardsdict:
			return keyword in wildcards.wildcardsdict[self.current_keyword]

		else:
			return self.current_keyword == keyword

	def serialize(self, data):
		return serializer.json_serialize(data)

