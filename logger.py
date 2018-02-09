import datetime, time
import models
import config
import test

#from peewee import *

start_button = True
flag = None
#Session is just an int that keeps track of when recording starts. If recording stops, the current session is exported and the session increments
session = 0

#Data Collection
def write_data(sensorName, data, pack, flag):
    now = datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S.%f')

    models.Data.create(sensorName=sensorName, data=data, time=now, pack=pack, flagged=flag, session_id=(session))
    

if __name__ == "__main__":
    models.build_db()
    session = models.get_session()
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
            for sensor_info in config.sensor_thresh_list:
                if sensor_info.name == datapoint.get_name():
                    #Check thresholds
                    if datapoint.get_data() in range (sensor_info.lower_threshold, sensor_info.upper_threshold):
                        #Sensor data is within allowable range
                        flag = False
                    else:
                        #Sensor data is not within allowable range. Flag and drop out of drive mode
                        flag = True
                    write_data(datapoint.get_name(), datapoint.get_data(), datapoint.get_pack(), flag=flag)
                    start_button = False
            
            if start_button is False:
                #Export
                models.export_csv(session)
                #And begin a new session
                session = session+1

            time.sleep(1)

