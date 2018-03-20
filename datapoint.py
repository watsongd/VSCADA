class Datapoint(object):
    sensor_name = ""
    data = 0
    system = ""
    sampleTime = 15
    pack = None
    sensor_id = 0

    def __init__(self,sensor_id, sensor_name, data, system, sampleTime, pack):
        self.sensor_id = sensor_id
        self.sensor_name = sensor_name
        self.data = data
        self.system = system
        self.sampleTime = sampleTime
        self.pack = pack

    def get_name(self):
        return self.sensor_name

    def get_data(self):
        return self.data

    def get_pack(self):
        return self.pack

    def get_system(self):
        return self.system
