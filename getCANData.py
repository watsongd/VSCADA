import can

bus = can.interface.Bus(channel='can0', bustype='socketcan_native')

listOfViewableData = [{"address": 0x100, "offset": 0, "byteLength": 1, "system": "TSV", "description": "Pack 1 State"},
					  {"address": 0x100, "offset": 1, "byteLength": 2, "system": "TSV", "description": "Pack 1 Voltage"},
					  {"address": 0x100, "offset": 3, "byteLength": 4, "system": "TSV", "description": "Pack 1 Current"},
					  {"address": 0x100, "offset": 7, "byteLength": 1, "system": "TSV", "description": "Pack 1 SOC"},
					  {"address": 0x101, "offset": 0, "byteLength": 4, "system": "TSV", "description": "Pack 1 Columbs"},
					  {"address": 0x101, "offset": 4, "byteLength": 1, "system": "TSV", "description": "Pack 1 Cell 1 Status"},
					  {"address": 0x101, "offset": 5, "byteLength": 1, "system": "TSV", "description": "Pack 1 Cell 2 Status"},
					  {"address": 0x101, "offset": 6, "byteLength": 1, "system": "TSV", "description": "Pack 1 Cell 3 Status"},
					  {"address": 0x101, "offset": 7, "byteLength": 1, "system": "TSV", "description": "Pack 1 Cell 4 Status"}]
msg = bus.recv()
address = hex(msg.arbitration_id)
data = msg.data
data_length = msg.dlc
for dictOfMeasurables in listOfViewableData:
	print(dictOfMeasurables)
# notifier = can.Notifier(bus, [can.Printer()])