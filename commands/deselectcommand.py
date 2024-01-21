from .command import Command


class DeselectCommand(Command):
	def __init__(self, progress=0):
		super().__init__(["deselect", "select_word"], progress)

