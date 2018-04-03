class Error(object):

	def __init__(self, sensor_id, num_errors, critical_error):
		self.sensor_id = sensor_id
		self.num_errors = num_errors
		self.critical_error = critical_error