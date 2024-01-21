from .command import Command


class SelectCommand(Command):
	def __init__(self, progress=0):
		super().__init__(["select", "select_word"], progress)

