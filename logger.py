import datetime, time
import models
import config
import test
import logging

#from peewee import *

start_button = True
flag = None
#Session is just an int that keeps track of when recording starts. If recording stops, the current session is exported and the session increments
session = 0

#Data Collection
def write_data(sensorName, data, pack, now, flag):

    models.Data.create(sensorName=sensorName, data=data, time=now, pack=pack, flagged=flag, session_id=(session))
    

if __name__ == "__main__":
    models.build_db()
    session = models.get_session()
    logging.basicConfig(filename='log.log', level=logging.WARNING)
    #session = models.get_session() + 1
    print session
    while True:
        #Continually check if start button is pressed
        #If start button is pressed begin data collection
        while start_button is True:
            #Write data specified by config file into database

            #This uses test.get_data. REPLACE WHEN GEOFF IS READY
            datapoint = test.get_data()
            #####################################################

            #CAN data parsed
            data = datapoint.get_data()
            sensor_name = datapoint.get_name()
            pack = datapoint.get_pack()
            #Time
            now = datetime.datetime.now().strftime('%H:%M:%S')

            #Search for sensor in config file
            for sensor_info in config.sensor_thresh_list:
                if sensor_info.name == sensor_name:
                    #Check thresholds
                    if data in range(sensor_info.lower_threshold, sensor_info.upper_threshold):
                        #Sensor data is within allowable range
                        flag = False
                    else:
                        #Sensor data is not within allowable range. Flag and check if drop out of drive mode needed
                        flag = True
                        #Do not need to drop out
                        if sensor_info.drop_out == 0:
                            logging.warning('%s : %s has exceeded the given threshold. Value: %d', now, sensor_name, data)
                        if sensor_info.drop_out == 1:
                            logging.critical('%s : %s has exceeded the given threshold. Value: %d', now, sensor_name, data)
                    write_data(sensorName=sensor_name, data=data, pack=pack, flag=flag, now=now)
                    start_button = False

            if start_button is False:
                #Export
                models.export_csv(session)
                #And begin a new session
                session = session+1

            time.sleep(1)

