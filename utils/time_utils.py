from datetime import timedelta, datetime



def add_offset(offset, init_time, unit="milliseconds"):
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