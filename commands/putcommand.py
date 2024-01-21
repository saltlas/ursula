from .command import Command

class PutCommand(Command):
	def __init__(self, progress=0):
		super().__init__(["put", "select_word", "move_word"], progress)