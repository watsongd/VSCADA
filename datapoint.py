class Datapoint(object):
    sensor_name = ""
    data = 0
    pack = ""
    
    def __init__(self, sensor_name, data, pack):
        self.sensor_name = sensor_name
        self.data = data
        self.pack = pack

    def get_name(self):
        return self.sensor_name
    
    def get_data(self):
        return self.data

    def get_pack(self):
        return self.pack