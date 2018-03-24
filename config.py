import csv
import collections
import os

sensor_thresh_list = []

SensorInfo = collections.namedtuple('sensor', 'name lower_threshold upper_threshold drop_out')

for root, dirs, files in os.walk("/media/pi"):
    for file in files:
        if file.startswith("config"):
            print (root)
            config_path = root + 'config.csv'
        else:
            print ('No config file on flash drive or not flash drive present')
            config_path = 'config.csv'

print (config_path)
with open(config_path, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        sensor = SensorInfo(name=row[0], lower_threshold=int(row[1]), upper_threshold=int(row[2]), drop_out=int(row[3]))
        sensor_thresh_list.append(sensor)

#print (sensor_thresh_list)
