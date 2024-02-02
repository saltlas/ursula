from .command import Command

class MoveCommand(Command):
	"""command-specific logic for a spoken 'put that there' type command"""

	def __init__(self, progress=0):
		super().__init__(["move", "move_word"], progress)