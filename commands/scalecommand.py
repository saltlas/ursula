from .command import Command


class ScaleCommand(Command):
	"""command-specific logic for a spoken scaling command"""

	def __init__(self, progress=0):
		super().__init__(["scale", "scale_word"], progress)


