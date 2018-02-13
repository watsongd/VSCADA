import can

class Datapoint(object):

	def __init__(self):
	    sensor_name = ""
	    data = 0
	    system = ""
	    sampleTime = 15
	    pack = ""

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

					  {"address": 0x601, "offset": 0, "byteLength": 2, "system": "DYNO", "pack": None, "sampleTime": 15, "description": "Motor RPM"},
					  {"address": 0x601, "offset": 2, "byteLength": 1, "system": "DYNO", "pack": None, "sampleTime": 15, "description": "Motor Temp"},
					  {"address": 0x601, "offset": 3, "byteLength": 1, "system": "DYNO", "pack": None, "sampleTime": 15, "description": "Controller Temp"},
					  {"address": 0x601, "offset": 4, "byteLength": 2, "system": "DYNO", "pack": None, "sampleTime": 1, "description": "RMS Current"},
					  {"address": 0x601, "offset": 6, "byteLength": 2, "system": "DYNO", "pack": None, "sampleTime": 15, "description": "Capacitor Voltage"},
					  {"address": 0x602, "offset": 0, "byteLength": 2, "system": "DYNO", "pack": None, "sampleTime": 15, "description": "Stator Frequency"},
					  {"address": 0x602, "offset": 2, "byteLength": 1, "system": "DYNO", "pack": None, "sampleTime": 15, "description": "Controller Fault Primary"},
					  {"address": 0x602, "offset": 3, "byteLength": 1, "system": "DYNO", "pack": None, "sampleTime": 15, "description": "Controller Fault Secondary"},
					  {"address": 0x602, "offset": 4, "byteLength": 1, "system": "DYNO", "pack": None, "sampleTime": 15, "description": "Throttle Input"},
					  {"address": 0x602, "offset": 5, "byteLength": 1, "system": "DYNO", "pack": None, "sampleTime": 15, "description": "Brake Input"},

					  {"address": 0xF0, "offset": 0, "byteLength": 2, "system": "COOLING", "pack": None, "sampleTime": 15, "description": "Cooling State"},
					  {"address": 0xF0, "offset": 2, "byteLength": 4, "system": "COOLING", "pack": None, "sampleTime": 15, "description": "Outlet Fluid Temp"},
					  {"address": 0xF1, "offset": 0, "byteLength": 4, "system": "COOLING", "pack": None, "sampleTime": 15, "description": "Fluid Flow Rate"},
					  {"address": 0xF1, "offset": 4, "byteLength": 4, "system": "COOLING", "pack": None, "sampleTime": 15, "description": "Inlet Fluid Temp"},

					  {"address": 0xF2, "offset": 0, "byteLength": 3, "system": "TSI", "pack": None, "sampleTime": 15, "description": "TSI State"},
					  {"address": 0xF2, "offset": 3, "byteLength": 4, "system": "TSI", "pack": None, "sampleTime": 15, "description": "IMD"},
					  {"address": 0xF3, "offset": 0, "byteLength": 5, "system": "TSI", "pack": None, "sampleTime": 15, "description": "Brake"},
					  {"address": 0xF4, "offset": 0, "byteLength": 6, "system": "TSI", "pack": None, "sampleTime": 15, "description": "Throttle Position"},
					  {"address": 0xF5, "offset": 0, "byteLength": 7, "system": "TSI", "pack": None, "sampleTime": 15, "description": "TSV Voltage"},
					  {"address": 0xF6, "offset": 0, "byteLength": 8, "system": "TSI", "pack": None, "sampleTime": 15, "description": "TSV Current"}]



def main():
	bus = can.interface.Bus(channel='can0', bustype='socketcan_native')

	for msg in bus:
		# Set the address, data, and data length for each message
		address = hex(msg.arbitration_id)
		data = msg.data
		data_length = msg.dlc
		# Iterate through the possible data points
		for item in listOfViewableData:
			#if the data point's address equals the one of the message, make a new datapoint
			if item.address == address:

				newDataPoint = Datapoint()
				newDataPoint.sensor_name = item.description
				newDataPoint.system = item.system
				newDataPoint.sampleTime = item.sampleTime
				newDataPoint.pack = item.pack

				# Handle the byte length on data points
				if item.byteLength > 1:
					print("byte length is greater than 1")
				else:
					print(newDataPoint.description + ": " data[newDataPoint.offset])

main()
