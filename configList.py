import csv
import collections
import os

SensorInfo = collections.namedtuple('sensor', 'name lower_threshold upper_threshold drop_out')

class configList(object):
    sensor_thresh_list = []
    def __init__(self):
        self.sensor_thresh_list = []

    def get_config_path(self):
        config_path = ''

        for root, dirs, files in os.walk("/media/pi"):
            for file in files:
                if file.startswith("config"):
                    print (root)
                    config_path = root + 'config.csv'
                    return config_path
        config_path ='/home/pi/Desktop/VSCADA/' + 'config.csv'
        return config_path

    def populate_thresh_list(self):
        config_path = self.get_config_path()
        with open(config_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                sensor = SensorInfo(name=row[0], lower_threshold=float(row[1]), upper_threshold=float(row[2]), drop_out=float(row[3]))
                self.sensor_thresh_list.append(sensor)
        print (self.sensor_thresh_list)
