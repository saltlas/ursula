"""utility functions for handling anything time-related"""



from datetime import timedelta, datetime
import time


def add_offset(offset, init_time, unit="milliseconds"):
	"""adds an offset to a timestamp and returns modified timestamp.
	equivalent to init_time + timedelta('milliseconds'=offset) but more versatile"""
	try:
		kws = {unit: offset}
		return init_time + timedelta(**kws)
	except TypeError as e:
		print("ERROR: You have specified an invalid unit to use for word timestamps. Timestamps will be invalid.")
		print(e)

def convert_timedelta_to_milliseconds(time_to_convert):
	return time_to_convert / timedelta(milliseconds = 1)

def get_time():
	return datetime.now()

def get_time_milliseconds():
	# technically could be done with datetime.now.timestamp() * 1000 but that's uglier and probably slower
	return time.time() * 1000