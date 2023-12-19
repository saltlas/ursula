import command

class MoveCommand(command.Command):
	def __init__(self, progress=0):
		super.__init__(["move", "30"], progress)

	def action(self):
		keyword_index = self.progress
		if keyword_index == 0:
			self.update_next_keyword()
		elif keyword_index == 1:
			print("moving")
# not done - how to know what axis to rotate along?			