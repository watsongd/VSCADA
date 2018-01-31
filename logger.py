import datetime, time
import models
import config

start_button = None

#Data Collection
while True:
    #Allows the system to export once the start_button is toggled
    ready_to_export = True
    #Continually check if button is pressed
    #If start button is pressed begin data collection
    while start_button is True:
        #Write data specified by config file into database
        datapoint = get_data()
        if datapoint.get_name() in config.sensor_list:
            write_data(datapoint.get_name(), datapoint.get_data, datapoint.get_pack())
        time.sleep(.025)
    
    if ready_to_export is True:
        #Export data to CSV

        ready_to_export = False

def write_data(sensorName, data, pack):
    now = datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S.%f')

    data = models.Data(sensorName=sensorName, data=data, time=now, pack=pack)
    data.save()
