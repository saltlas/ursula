import uuid
from utils import serializer, wildcards
from word2number import w2n


class Command:
	"""Base class for all commands dictating default logic. 
	commands extend this class for customisability of behaviour."""

	def __init__(self, keywords, progress=0, finishable=False):

		# there are a few fields here that are useless in current implementation, like times and passing progress as an argument, but may be useful for later implementations

		self.keywords = keywords
		if len(keywords) < 1:
			raise ValueError("Keywords list is empty!")
		self.num_keywords = len(keywords)
		self.progress = progress
		self.current_keyword = keywords[progress]
		self.finished = False
		self.times = {}
		self.finishable = finishable

		# generate unique session ID at command beginning using UUID 4
		self.session_id = str(uuid.uuid4())

	def action(self, timestamp, keyword):
		"""action to take based on keyword spoken. 
		not relevant to current implementation
		but in some cases could specifically send 
		certain things depending on keyword index"""

		keyword_index = self.progress
		if self.current_keyword == "num_word":
			try:
				keyword = w2n.word_to_num(keyword)
			except ValueError:
				pass			
		# if this isn't the final keyword, move the next expected keyword to be the keyword that comes after the one passed
		if keyword_index != self.num_keywords - 1:
			self.update_next_keyword()


		# not doing self.finish() on final keyword means you can get select that that that instead of only select that
		elif self.finishable:
			self.finish()

		# data to send to input manager, json serialized
		event = {
				"session_id": self.session_id,
				"phrase": keyword,
				"timestamp": timestamp
			}
		return self.serialize(event)	


	def check_current_keyword(self, keyword):
		"""checks if 'keyword' matches the current expected keyword, returns true or false"""
		if self.current_keyword in wildcards.wildcardsdict:
			return keyword in wildcards.wildcardsdict[self.current_keyword]
		elif self.current_keyword == "num_word":
			if keyword.isdigit():
				return True
			try:
				w2n.word_to_num(keyword)
				return True
			except ValueError:
				return False

		else:
			return self.current_keyword == keyword

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

	def serialize(self, data):
		return serializer.json_serialize(data)

