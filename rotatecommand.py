import command

class RotateCommand(command.Command):
	def __init__(self, progress=0):
		super.__init__(["rotate", "30", "degrees"], progress)

	def action(self):
		if keyword_index == 0:
# not done - how to know what axis to rotate along?			