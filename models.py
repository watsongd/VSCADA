import datetime #For sensor readings
import csv, sys, sqlite3

# Import from peewee
from peewee import *
from playhouse.dataset import DataSet

#Connect  to sqlite3 database
db = SqliteDatabase('../car_data.db')

#Table for Pack1 Data
class Data(Model):
    sensorName = CharField()
    data       = CharField()
    time       = DateTimeField()
    system     = CharField(max_length = 6)
    pack       = CharField(max_length = 6, null = True)
    flagged    = BooleanField()
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
    conn = sqlite3.connect('../car_data.db')
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
    #Connect to database
    conn = sqlite3.connect('../car_data.db')
    c = conn.cursor()

    #Select all data from db
    data_all = c.execute("SELECT * FROM data")

    f = open('/media/pi/9BEE-5C4F/car_data_all.csv', 'wb')

    writer = csv.writer(f, delimiter=';')
    writer.writerows(data_all)

    f.close()

    #Select data from db from the most recent session
    data_session = c.execute("SELECT * FROM data WHERE session_id={}".format(session))

    g = open('/media/pi/9BEE-5C4F/car_data_session_{}.csv'.format(session), 'wb')

    writer = csv.writer(g, delimiter=';')
    writer.writerows(data_session)

    g.close()
