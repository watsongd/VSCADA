import datetime #For sensor readings

# Import from peewee
from peewee import *

#Connect  to sqlite3 database
db = SqliteDatabase('car_data.db')

#Base Model class that other models will extend
class NewBaseModel(Model):
    class Meta:
        database = db

#Table with sensor details
class SensorLookup(NewBaseModel):
    sensorName = CharField(unique=True)
    address    = IntegerField()
    offset     = IntegerField()
    byteLength = IntegerField()
    system     = CharField()
    units      = CharField()

#Table for Pack1 Data
class Data(NewBaseModel):
    sensorName = CharField()
    data       = IntegerField()
    time       = TimeField()
    pack       = CharField(max_length = 4)

db.connect()
db.create_tables([SensorLookup,Data])
