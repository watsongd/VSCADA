import csv
import collections

sensor_thresh_list = []

SensorInfo = collections.namedtuple('sensor', 'name lower_threshold upper_threshold')

with open('config.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        sensor = SensorInfo(name=row[0], lower_threshold=int(row[1]), upper_threshold=int(row[2]))
        sensor_thresh_list.append(sensor)

print sensor_thresh_list