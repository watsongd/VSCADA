import datetime #For sensor readings
import csv, sys, sqlite3, os
from shutil import copyfile

# Import from peewee
from peewee import *
from playhouse.dataset import DataSet

#Connect  to sqlite3 database
db = SqliteDatabase('/home/pi/Desktop/car_data.db')

#Table for Pack1 Data
class Data(Model):
    sensor_id  = IntegerField()
    sensorName = CharField()
    data       = CharField()
    time       = DateTimeField()
    system     = CharField(max_length = 6)
    pack       = CharField(max_length = 6, null = True)
    flagged    = BooleanField()
    csv_out    = IntegerField()
    session_id = IntegerField()

    class Meta:
        database = db
        table_name = 'data'

def build_db():
    try:
        Data.create_table()
    except OperationalError:
        print ("Data table already exists!")

def get_session():
    conn = sqlite3.connect('/home/pi/Desktop/car_data.db')
    c = conn.cursor()
    session = c.execute("SELECT session_id FROM data WHERE session_id=(SELECT MAX(session_id) FROM data)")
    try:
        max_session = session.fetchone()[0]
        return max_session + 1
    except:
        return 0

#Exports data from db to two csv files
#One file has all data from db. The other has only the data from the most recent session
def export_csv(session):

    #Search for text file on fash drive. Get path
    flash_drive_path = search_flash_drive()
    if flash_drive_path == '':
        if not os.path.exists("../VSCADA_CSV_FILES/"):
            os.makedirs("../VSCADA_CSV_FILES/")
        flash_drive_path = "/home/pi/Desktop/VSCADA_CSV_FILES/"

    #Connect to database
    conn = sqlite3.connect('/home/pi/Desktop/car_data.db')
    c = conn.cursor()

    #Select all data from db
    data_all = c.execute("SELECT sensor_id,time,data,flagged,session_id FROM data")

    f = open(flash_drive_path + '/car_data_all.csv', 'w')

    writer = csv.writer(f, deliminter=',')
    #writer.writerows(['Sensor_id', 'Time', 'Data Value', 'Flagged?'])
    writer.writerows(data_all)

    f.close()

    #Select data from db from the most recent session
    data_session = c.execute("SELECT sensor_id,time,data,flagged FROM data WHERE session_id={} AND csv_out = 1".format(session))

    g = open(flash_drive_path + '/car_data_session_{}.csv'.format(session), 'w')

    writer = csv.writer(g, deliminter=',')
    #writer.writerows(['Sensor_id', 'Time', 'Data Value', 'Flagged?'])
    writer.writerows(data_session)

    g.close()
    export_log()
    

#Exports data from db to csv files in case of a system failure
#Exports data from previous session
def export_csv_previous(session):
    session = session - 1
    print (session)
    if session >= 0:
        #Search for text file on fash drive. Get path
        flash_drive_path = search_flash_drive()
        if flash_drive_path == '':
            if not os.path.exists("../VSCADA_CSV_FILES/"):
                os.makedirs("../VSCADA_CSV_FILES/")
            flash_drive_path = "/home/pi/Desktop/VSCADA_CSV_FILES/"

        #Connect to database
        conn = sqlite3.connect('/home/pi/Desktop/car_data.db')
        c = conn.cursor()

        #Select data from db from the most recent session
        data_session = c.execute("SELECT sensor_id,time,data,flagged FROM data WHERE session_id={} AND csv_out = 1".format(session))

        g = open(flash_drive_path + '/car_data_recovery_session_{}.csv'.format(session), 'w')

        writer = csv.writer(g, deliminter=',')
        writer.writerows(['Sensor_id', 'Time', 'Data Value', 'Flagged?'])
        writer.writerows(data_session)

        g.close()  

        print('Recovered data to: ' + flash_drive_path)
        export_log()

#Exports data from previous session
def export_log():
    session = session - 1
    print (session)
    if session >= 0:
        #Search for text file on fash drive. Get path
        flash_drive_path = search_flash_drive()
        if flash_drive_path == '':
            if not os.path.exists("../VSCADA_CSV_FILES/"):
                os.makedirs("../VSCADA_CSV_FILES/")
            flash_drive_path = "/home/pi/Desktop/VSCADA_CSV_FILES/"

    copyfile("/home/pi/Desktop/VSCADA/log.log", flash_drive_path)

#Searches for a USB flash drive that contains the correct text file. If it doesnt return empty str
def search_flash_drive():
    for root, dirs, files in os.walk("/media/pi"):
        for file in files:
            if file.startswith("lafayetteSCADA"):
                #print(root)
                return root
    return ''
