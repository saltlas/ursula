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

	def action(self, timestamp):
		keyword_index = self.progress
		self.times[self.current_keyword] = timestamp

		if keyword_index != self.num_keywords - 1:
			self.update_next_keyword()
		else:
			self.finish()		


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


