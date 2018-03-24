import csv
import collections

sensor_thresh_list = []

SensorInfo = collections.namedtuple('sensor', 'name lower_threshold upper_threshold drop_out')

with open('/home/pi/Desktop/VSCADA/config.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        sensor = SensorInfo(name=row[0], lower_threshold=int(row[1]), upper_threshold=int(row[2]), drop_out=int(row[3]))
        sensor_thresh_list.append(sensor)

#print (sensor_thresh_list)
