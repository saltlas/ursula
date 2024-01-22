from .command import Command


class DeselectCommand(Command):
	"""command-specific logic for a spoken deselection command"""

	def __init__(self, progress=0):
		super().__init__(["deselect", "select_word"], progress)

