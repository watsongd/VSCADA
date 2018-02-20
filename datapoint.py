class Datapoint(object):
    sensor_name = ""
    data = 0
    system = ""
    sampleTime = 15
    pack = None

    def __init__(self, sensor_name, data, system, sampleTime, pack):
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
