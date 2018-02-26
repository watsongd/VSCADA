import can
import time
import queue
import logging
import config
import models
import datetime

class Datapoint(object):

	def __init__(self):
	    sensor_name = ""
	    data = 0
	    system = ""
	    sampleTime = 15
	    pack = None

listOfViewableData = [{"address": 0x100, "offset": 0, "byteLength": 1, "system": "TSV", "pack": 1, "sampleTime": 15, "description": "State"},
					  {"address": 0x100, "offset": 1, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 15, "description": "Voltage"},
					  {"address": 0x100, "offset": 3, "byteLength": 4, "system": "TSV", "pack": 1, "sampleTime": 1,  "description": "Current"},
					  {"address": 0x100, "offset": 7, "byteLength": 1, "system": "TSV", "pack": 1, "sampleTime": 15, "description": "SOC"},
					  {"address": 0x101, "offset": 0, "byteLength": 4, "system": "TSV", "pack": 1, "sampleTime": 15, "description": "Columbs"},

					  {"address": 0x101, "offset": 4, "byteLength": 1, "system": "TSV", "pack": 1, "sampleTime": 15, "description": "Cell 1 Status"},
					  {"address": 0x101, "offset": 5, "byteLength": 1, "system": "TSV", "pack": 1, "sampleTime": 15, "description": "Cell 2 Status"},
					  {"address": 0x101, "offset": 6, "byteLength": 1, "system": "TSV", "pack": 1, "sampleTime": 15, "description": "Cell 3 Status"},
					  {"address": 0x101, "offset": 7, "byteLength": 1, "system": "TSV", "pack": 1, "sampleTime": 15, "description": "Cell 4 Status"},
					  {"address": 0x102, "offset": 0, "byteLength": 1, "system": "TSV", "pack": 1, "sampleTime": 15, "description": "Cell 5 Status"},
					  {"address": 0x102, "offset": 1, "byteLength": 1, "system": "TSV", "pack": 1, "sampleTime": 15, "description": "Cell 6 Status"},
					  {"address": 0x102, "offset": 2, "byteLength": 1, "system": "TSV", "pack": 1, "sampleTime": 15, "description": "Cell 7 Status"},

					  {"address": 0x102, "offset": 3, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 15, "description": "Cell 1 Voltage"},
					  {"address": 0x102, "offset": 5, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 15, "description": "Cell 1 Voltage"},
					  {"address": 0x102, "offset": 3, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 15, "description": "Cell 2 Voltage"},
					  {"address": 0x103, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 15, "description": "Cell 3 Voltage"},
					  {"address": 0x103, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 15, "description": "Cell 4 Voltage"},
					  {"address": 0x103, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 15, "description": "Cell 5 Voltage"},
					  {"address": 0x103, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 15, "description": "Cell 6 Voltage"},
					  {"address": 0x104, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 15, "description": "Cell 7 Voltage"},

					  {"address": 0x104, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 15, "description": "Cell 1 Temp"},
					  {"address": 0x104, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 15, "description": "Cell 2 Temp"},
					  {"address": 0x104, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 15, "description": "Cell 3 Temp"},
					  {"address": 0x105, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 15, "description": "Cell 4 Temp"},
					  {"address": 0x105, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 15, "description": "Cell 5 Temp"},
					  {"address": 0x105, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 15, "description": "Cell 6 Temp"},
					  {"address": 0x105, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "description": "Cell 7 Temp"},


					  {"address": 0x200, "offset": 0, "byteLength": 1, "system": "TSV", "pack": 2, "sampleTime": 15, "description": "State"},
					  {"address": 0x200, "offset": 1, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "description": "Voltage"},
					  {"address": 0x200, "offset": 3, "byteLength": 4, "system": "TSV", "pack": 2, "sampleTime": 1,  "description": "Current"},
					  {"address": 0x200, "offset": 7, "byteLength": 1, "system": "TSV", "pack": 2, "sampleTime": 15, "description": "SOC"},
					  {"address": 0x201, "offset": 0, "byteLength": 4, "system": "TSV", "pack": 2, "sampleTime": 15, "description": "Columbs"},

					  {"address": 0x201, "offset": 4, "byteLength": 1, "system": "TSV", "pack": 2, "sampleTime": 15, "description": "Cell 1 Status"},
					  {"address": 0x201, "offset": 5, "byteLength": 1, "system": "TSV", "pack": 2, "sampleTime": 15, "description": "Cell 2 Status"},
					  {"address": 0x201, "offset": 6, "byteLength": 1, "system": "TSV", "pack": 2, "sampleTime": 15, "description": "Cell 3 Status"},
					  {"address": 0x201, "offset": 7, "byteLength": 1, "system": "TSV", "pack": 2, "sampleTime": 15, "description": "Cell 4 Status"},
					  {"address": 0x202, "offset": 0, "byteLength": 1, "system": "TSV", "pack": 2, "sampleTime": 15, "description": "Cell 5 Status"},
					  {"address": 0x202, "offset": 1, "byteLength": 1, "system": "TSV", "pack": 2, "sampleTime": 15, "description": "Cell 6 Status"},
					  {"address": 0x202, "offset": 2, "byteLength": 1, "system": "TSV", "pack": 2, "sampleTime": 15, "description": "Cell 7 Status"},

					  {"address": 0x202, "offset": 3, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "description": "Cell 1 Voltage"},
					  {"address": 0x202, "offset": 5, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "description": "Cell 1 Voltage"},
					  {"address": 0x202, "offset": 3, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "description": "Cell 2 Voltage"},
					  {"address": 0x203, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "description": "Cell 3 Voltage"},
					  {"address": 0x203, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "description": "Cell 4 Voltage"},
					  {"address": 0x203, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "description": "Cell 5 Voltage"},
					  {"address": 0x203, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "description": "Cell 6 Voltage"},
					  {"address": 0x204, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "description": "Cell 7 Voltage"},

					  {"address": 0x204, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "description": "Cell 1 Temp"},
					  {"address": 0x204, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "description": "Cell 2 Temp"},
					  {"address": 0x204, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "description": "Cell 3 Temp"},
					  {"address": 0x205, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "description": "Cell 4 Temp"},
					  {"address": 0x205, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "description": "Cell 5 Temp"},
					  {"address": 0x205, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "description": "Cell 6 Temp"},
					  {"address": 0x205, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "description": "Cell 7 Temp"},


					  {"address": 0x300, "offset": 0, "byteLength": 1, "system": "TSV", "pack": 3, "sampleTime": 15, "description": "State"},
					  {"address": 0x300, "offset": 1, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 15, "description": "Voltage"},
					  {"address": 0x300, "offset": 3, "byteLength": 4, "system": "TSV", "pack": 3, "sampleTime": 1,  "description": "Current"},
					  {"address": 0x300, "offset": 7, "byteLength": 1, "system": "TSV", "pack": 3, "sampleTime": 15, "description": "SOC"},
					  {"address": 0x301, "offset": 0, "byteLength": 4, "system": "TSV", "pack": 3, "sampleTime": 15, "description": "Columbs"},

					  {"address": 0x301, "offset": 4, "byteLength": 1, "system": "TSV", "pack": 3, "sampleTime": 15, "description": "Cell 1 Status"},
					  {"address": 0x301, "offset": 5, "byteLength": 1, "system": "TSV", "pack": 3, "sampleTime": 15, "description": "Cell 2 Status"},
					  {"address": 0x301, "offset": 6, "byteLength": 1, "system": "TSV", "pack": 3, "sampleTime": 15, "description": "Cell 3 Status"},
					  {"address": 0x301, "offset": 7, "byteLength": 1, "system": "TSV", "pack": 3, "sampleTime": 15, "description": "Cell 4 Status"},
					  {"address": 0x302, "offset": 0, "byteLength": 1, "system": "TSV", "pack": 3, "sampleTime": 15, "description": "Cell 5 Status"},
					  {"address": 0x302, "offset": 1, "byteLength": 1, "system": "TSV", "pack": 3, "sampleTime": 15, "description": "Cell 6 Status"},
					  {"address": 0x302, "offset": 2, "byteLength": 1, "system": "TSV", "pack": 3, "sampleTime": 15, "description": "Cell 7 Status"},

					  {"address": 0x302, "offset": 3, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 15, "description": "Cell 1 Voltage"},
					  {"address": 0x302, "offset": 5, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 15, "description": "Cell 1 Voltage"},
					  {"address": 0x302, "offset": 3, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 15, "description": "Cell 2 Voltage"},
					  {"address": 0x303, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 15, "description": "Cell 3 Voltage"},
					  {"address": 0x303, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 15, "description": "Cell 4 Voltage"},
					  {"address": 0x303, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 15, "description": "Cell 5 Voltage"},
					  {"address": 0x303, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 15, "description": "Cell 6 Voltage"},
					  {"address": 0x304, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 15, "description": "Cell 7 Voltage"},

					  {"address": 0x304, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 15, "description": "Cell 1 Temp"},
					  {"address": 0x304, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 15, "description": "Cell 2 Temp"},
					  {"address": 0x304, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 15, "description": "Cell 3 Temp"},
					  {"address": 0x305, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 15, "description": "Cell 4 Temp"},
					  {"address": 0x305, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 15, "description": "Cell 5 Temp"},
					  {"address": 0x305, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 15, "description": "Cell 6 Temp"},
					  {"address": 0x305, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 15, "description": "Cell 7 Temp"},


					  {"address": 0x400, "offset": 0, "byteLength": 1, "system": "TSV", "pack": 4, "sampleTime": 15, "description": "State"},
					  {"address": 0x400, "offset": 1, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 15, "description": "Voltage"},
					  {"address": 0x400, "offset": 3, "byteLength": 4, "system": "TSV", "pack": 4, "sampleTime": 1,  "description": "Current"},
					  {"address": 0x400, "offset": 7, "byteLength": 1, "system": "TSV", "pack": 4, "sampleTime": 15, "description": "SOC"},
					  {"address": 0x401, "offset": 0, "byteLength": 4, "system": "TSV", "pack": 4, "sampleTime": 15, "description": "Columbs"},

					  {"address": 0x401, "offset": 4, "byteLength": 1, "system": "TSV", "pack": 4, "sampleTime": 15, "description": "Cell 1 Status"},
					  {"address": 0x401, "offset": 5, "byteLength": 1, "system": "TSV", "pack": 4, "sampleTime": 15, "description": "Cell 2 Status"},
					  {"address": 0x401, "offset": 6, "byteLength": 1, "system": "TSV", "pack": 4, "sampleTime": 15, "description": "Cell 3 Status"},
					  {"address": 0x401, "offset": 7, "byteLength": 1, "system": "TSV", "pack": 4, "sampleTime": 15, "description": "Cell 4 Status"},
					  {"address": 0x402, "offset": 0, "byteLength": 1, "system": "TSV", "pack": 4, "sampleTime": 15, "description": "Cell 5 Status"},
					  {"address": 0x402, "offset": 1, "byteLength": 1, "system": "TSV", "pack": 4, "sampleTime": 15, "description": "Cell 6 Status"},
					  {"address": 0x402, "offset": 2, "byteLength": 1, "system": "TSV", "pack": 4, "sampleTime": 15, "description": "Cell 7 Status"},

					  {"address": 0x402, "offset": 3, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 15, "description": "Cell 1 Voltage"},
					  {"address": 0x402, "offset": 5, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 15, "description": "Cell 1 Voltage"},
					  {"address": 0x402, "offset": 3, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 15, "description": "Cell 2 Voltage"},
					  {"address": 0x403, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 15, "description": "Cell 3 Voltage"},
					  {"address": 0x403, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 15, "description": "Cell 4 Voltage"},
					  {"address": 0x403, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 15, "description": "Cell 5 Voltage"},
					  {"address": 0x403, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 15, "description": "Cell 6 Voltage"},
					  {"address": 0x404, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 15, "description": "Cell 7 Voltage"},

					  {"address": 0x404, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 15, "description": "Cell 1 Temp"},
					  {"address": 0x404, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 15, "description": "Cell 2 Temp"},
					  {"address": 0x404, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 15, "description": "Cell 3 Temp"},
					  {"address": 0x405, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 15, "description": "Cell 4 Temp"},
					  {"address": 0x405, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 15, "description": "Cell 5 Temp"},
					  {"address": 0x405, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 15, "description": "Cell 6 Temp"},
					  {"address": 0x405, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 15, "description": "Cell 7 Temp"},


					  {"address": 0x601, "offset": 0, "byteLength": 2, "system": "MC", "pack": 0, "sampleTime": 15, "description": "Motor RPM"},
					  {"address": 0x601, "offset": 2, "byteLength": 1, "system": "MC", "pack": 0, "sampleTime": 15, "description": "Motor Temp"},
					  {"address": 0x601, "offset": 3, "byteLength": 1, "system": "MC", "pack": 0, "sampleTime": 15, "description": "Controller Temp"},
					  {"address": 0x601, "offset": 4, "byteLength": 2, "system": "MC", "pack": 0, "sampleTime": 1, "description": "RMS Current"},
					  {"address": 0x601, "offset": 6, "byteLength": 2, "system": "MC", "pack": 0, "sampleTime": 15, "description": "Capacitor Voltage"},
					  {"address": 0x602, "offset": 0, "byteLength": 2, "system": "MC", "pack": 0, "sampleTime": 15, "description": "Stator Frequency"},
					  {"address": 0x602, "offset": 2, "byteLength": 1, "system": "MC", "pack": 0, "sampleTime": 15, "description": "Controller Fault Primary"},
					  {"address": 0x602, "offset": 3, "byteLength": 1, "system": "MC", "pack": 0, "sampleTime": 15, "description": "Controller Fault Secondary"},
					  {"address": 0x602, "offset": 4, "byteLength": 1, "system": "MC", "pack": 0, "sampleTime": 15, "description": "Throttle Input"},
					  {"address": 0x602, "offset": 5, "byteLength": 1, "system": "MC", "pack": 0, "sampleTime": 15, "description": "Brake Input"},


					  {"address": 0x0F2, "offset": 0, "byteLength": 1, "system": "TSI", "pack": 0, "sampleTime": 15, "description": "TSI State"},
					  {"address": 0x0F2, "offset": 2, "byteLength": 2, "system": "TSI", "pack": 0, "sampleTime": 15, "description": "IMD"},
					  {"address": 0x0F2, "offset": 4, "byteLength": 1, "system": "TSI", "pack": 0, "sampleTime": 15, "description": "Brake"},
					  {"address": 0x0F3, "offset": 0, "byteLength": 2, "system": "TSI", "pack": 0, "sampleTime": 15, "description": "TSV Voltage"},
					  {"address": 0x0F3, "offset": 2, "byteLength": 2, "system": "TSI", "pack": 0, "sampleTime": 15, "description": "TSV Current"},
					  {"address": 0x0F3, "offset": 4, "byteLength": 2, "system": "TSI", "pack": 0, "sampleTime": 15, "description": "TSI Temp"}]

TSVPackState = {0: "Boot", 1: "Charging", 2: "Charged", 3: "Low Current Output", 4: "Fault", 5: "Dead", 6: "Ready"}
TSIPackState = {0: "Idle", 1: "Setup Drive", 2: "Drive", 3: "Setup Idle"}

displayDict = {"Voltage 1": 0, "Voltage 2": 0, "Voltage 3": 0, "Voltage 4": 0, "Current 1": 0, "Current 2": 0, "Current 3": 0, "Current 4": 0,
"TSI State": 0, "IMD": 0, "Brake": 0, "TSV Voltage": 0, "TSV Current": 0, "TSI Temp": 0, "Motor RPM": 0, "Motor Temp": 0}

#Variables for storing
record_button = True
#Session is just an int that keeps track of when recording starts. If recording stops, the current session is exported and the session increments
global session 

def main():
	models.build_db()
	session = models.get_session()
	logging.basicConfig(filename='log.log', level=logging.WARNING)
	print(session)

	while (True):
		parse()
		#CHECK BUTTON STATE
def timer():
   now = time.localtime(time.time())
   return now[5]

def send_throttle_control(throttleControl):
	bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
	msg = msg = can.Message(arbitration_id=0x010, data=[throttleControl], extended_id=False)
	bus.send(msg)

def parse():
	check_record_button()
	bus = can.interface.Bus(channel='can0', bustype='socketcan_native')

	for msg in bus:

		# Set the address, data, and data length for each message
		address = hex(msg.arbitration_id)
		data = msg.data
		dataLength = msg.dlc

		# Iterate through the possible data points
		for item in listOfViewableData:

			#if the data point's address equals the one of the message, make a new datapoint
			if hex(item['address']) == address:

				newDataPoint = Datapoint()
				newDataPoint.sensor_name = item['description']
				newDataPoint.system = item['system']
				newDataPoint.sampleTime = item['sampleTime']
				newDataPoint.pack = item['pack']
				offset = int(item['offset'])

				# Handle the byte length on data points
				if item['byteLength'] > 1:

					formattedData = data[offset]

					# for the length of byte, append to formatted data
					for i in range(int(item['byteLength'])):
						if i == (item['byteLength'] - 1):
							break
						else:
							# NUM * 2^8 --> SHIFT LEFT 8
							formattedData = ((formattedData * 2**8) + data[offset + (i + 1)])

					newDataPoint.data = formattedData
				else:
					newDataPoint.data = data[offset]

				# Based on the description, shift the decimal point as necessary
				if "Voltage" in newDataPoint.sensor_name:
					if "Cell" in newDataPoint.sensor_name:
						# mV --> V
						newDataPoint.data = newDataPoint.data / 1000 
					else:
						newDataPoint.data = newDataPoint.data / 10

				if "Current" in newDataPoint.sensor_name:
					# mA --> A
					newDataPoint.data = newDataPoint.data / 1000

				if "Temp" in newDataPoint.sensor_name:
					if "Cell" in newDataPoint.sensor_name:
						newDataPoint.data = newDataPoint.data / 10

				if "State" in newDataPoint.sensor_name:
					if "TSI" in newDataPoint.sensor_name:
						newDataPoint.data = TSIPackState[newDataPoint.data]
					else:
						newDataPoint.data = TSVPackState[newDataPoint.data]
					

				# Add to the queue based on the sample time of the object
				if timer() % item['sampleTime'] == 0:
					log_data(newDataPoint)
					update_display_dict(newDataPoint)
					print(newDataPoint.sensor_name + ": " + str(newDataPoint.data))

def log_data(datapoint):
	
	data = datapoint.data
	sensor_name = datapoint.sensor_name
	pack = datapoint.pack
	system = datapoint.system

	#Time
	now = datetime.datetime.now().strftime('%H:%M:%S')
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
					logging.warning('%s : %s has exceeded the given threshold. Value: %s', now, sensor_name, data)
				if sensor_info.drop_out == 1:
					#DROP OUT CALL HERE
					logging.critical('%s : %s has exceeded the given threshold. Value: %s', now, sensor_name, data)
					send_throttle_control()
			if record_button is True:
				models.Data.create(sensorName=sensor_name, data=data, time=now, system=system, pack=pack, flagged=flag, session_id=session)

def update_display_dict(datapoint):
	if datapoint.pack > 0:
		name = datapoint.sensor_name + " " + str(datapoint.pack)
	else:
		name = datapoint.sensor_name
	if name in displayDict:
		displayDict[name] = datapoint.data

	print(displayDict)


# test sending	
def test_sending():
	while(1):
		print("TIMER: " + str(timer()))
		if timer() % 1 == 0:
			send_throttle_control(0x01)
			print("MESSAGE SENT")

def check_record_button():
	#set record_button
	exported = False
	record_button = False
	if (record_button == False and exported == False):
		models.export_csv(session)
		session = session + 1
		exported = True
		print("Exported Data")

if __name__ == "__main__":
	main()
    
