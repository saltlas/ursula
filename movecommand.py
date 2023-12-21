import command
from datetime import timedelta, datetime
import json
import websockets
import asyncio

times = {}

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

async def handler(times):
	print(1.5)
	async with websockets.connect(
            'ws://localhost:8001') as websocket:
		print(2)

		event = {
			"moveX": 30,
			"moveY": 0,
			"moveZ": 0,
			"timestamp": times["30"]
		}
		await websocket.send(json.dumps(event, default=json_serial))



class MoveCommand(command.Command):
	def __init__(self, progress=0):
		super().__init__(["move", "30"], progress)
		self.times = {}

	def action(self, offset):
		keyword_index = self.progress
		self.times[self.current_keyword] = self.init_time + timedelta(seconds=offset)

		if keyword_index == 0:
			print("moving 1", datetime.now())
			self.update_next_keyword()
		elif keyword_index == 1:
			print("moving", datetime.now())
			self.finish()

	def confirm_command(self):
		print("sending", self.times)
		self.send_event()


	def set_init_time(self, init_time):
		self.init_time = init_time
# not done - how to know what axis to rotate along?			




	def send_event(self):
		print(1)
		asyncio.get_event_loop().run_until_complete(handler(self.times))

