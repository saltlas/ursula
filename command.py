class Command:
	"""a command class"""
	def __init__(self, keywords, progress=0):
		self.keywords = keywords
		if len(keywords) < 1:
			raise ValueError("Keywords list is empty!")
		self.num_keywords = len(keywords)
		self.progress = progress
		self.current_keyword = keywords[progress]

	def finished(self):
		return self.progress = self.num_keywords

	def update_next_keyword(self):
		if self.finished():
			return False
		else:
			self.progress += 1
			self.current_keyword = self.keywords[progress]

	def action(self):
		raise NotImplementedError("Actions not implemented!")