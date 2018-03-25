import csv
import collections
import os

sensor_thresh_list = []

SensorInfo = collections.namedtuple('sensor', 'name lower_threshold upper_threshold drop_out')
'''
config_path = ''

for root, dirs, files in os.walk("/media/pi"):
    for file in files:
        if file.startswith("config"):
            print (root)
            config_path = root + 'config.csv'
        else:
            print ('No config file on flash drive or not flash drive present')
            config_path ='/home/pi/Desktop/VSCADA/' + 'config.csv'

print (config_path)
'''

with open('/home/pi/Desktop/VSCADA/config.csv' , newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        sensor = SensorInfo(name=row[0], lower_threshold=float(row[1]), upper_threshold=float(row[2]), drop_out=float(row[3]))
        sensor_thresh_list.append(sensor)

#print (sensor_thresh_list)
