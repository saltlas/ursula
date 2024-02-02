from .command import Command

class RotateCommand(Command):
	"""command-specific logic for a spoken rotation command"""
	def __init__(self, progress=0):
		super().__init__(["rotate", "around", "axis_word", "axis", "by", "num_word"], progress)

