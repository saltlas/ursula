from .command import Command


class RotateCommand(Command):
	def __init__(self, progress=0):
		super().__init__(["rotate", "select_word"], progress)

